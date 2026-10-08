#!/usr/bin/env python3
"""Small Earth-annulus thermal-convection regression test for Underworld3.

The calculation is nondimensionalised with the mantle thickness and a
4 cm/yr reference surface velocity.  The physical values are kept below as named
parameters so that the setup is easy to audit and change.

The outer boundary has a tangential velocity divided into four equal angular
sectors using:

    v_theta = A(theta) * sin(2*theta)

The divergence at theta=0 is slow (2 cm/yr on both sides) and the divergence
at theta=pi is fast (6 cm/yr on both sides). The two intervening sectors
converge. The inner and outer boundaries are otherwise impermeable; the inner
boundary uses a penalty free-slip condition.

Run from the Underworld3 checkout with, for example::

    pixi run -e runtime python ../annulus_2D/test_annulus_convection.py --steps 20

The default mesh and ten time steps are deliberately small enough for a
regression/smoke test.  Increase ``--steps`` and reduce ``--cell-size-km``
for a production experiment.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np
import sympy

import underworld3 as uw


@dataclass(frozen=True)
class EarthParameters:
    """Dimensional Earth-like parameters used to form the model scales."""

    surface_radius_km: float = 6371.0
    cmb_radius_km: float = 3480.0
    temperature_surface_k: float = 0.0
    temperature_cmb_k: float = 2800.0
    velocity_scale_cm_per_yr: float = 4.0
    slow_velocity_cm_per_yr: float = 2.0
    fast_velocity_cm_per_yr: float = 6.0
    surface_viscosity_pa_s: float = 1.0e21
    asthenosphere_viscosity_pa_s: float = 1.0e19
    lower_mantle_viscosity_pa_s: float = 1.0e21
    asthenosphere_top_depth_km: float = 100.0
    asthenosphere_base_depth_km: float = 250.0
    lower_mantle_top_depth_km: float = 660.0
    thermal_diffusivity_m2_s: float = 1.0e-6
    density_kg_m3: float = 3300.0
    gravity_m_s2: float = 9.81
    thermal_expansion_k_inv: float = 3.0e-5

    @property
    def thickness_km(self) -> float:
        return self.surface_radius_km - self.cmb_radius_km

    @property
    def radius_inner(self) -> float:
        return self.cmb_radius_km / self.surface_radius_km

    @property
    def velocity_m_s(self) -> float:
        return self.velocity_scale_cm_per_yr * 1.0e-2 / (365.25 * 86400.0)

    @property
    def thickness_m(self) -> float:
        return self.thickness_km * 1000.0

    @property
    def kappa_nd(self) -> float:
        """Thermal diffusivity in the D/V time scale."""

        return self.thermal_diffusivity_m2_s / (self.thickness_m * self.velocity_m_s)

    @property
    def buoyancy_coeff_nd(self) -> float:
        """Coefficient of Theta in the nondimensional radial buoyancy force."""

        delta_t = self.temperature_cmb_k - self.temperature_surface_k
        return (
            self.density_kg_m3
            * self.gravity_m_s2
            * self.thermal_expansion_k_inv
            * delta_t
            * self.thickness_m**2
            / (self.surface_viscosity_pa_s * self.velocity_m_s)
        )

    @property
    def rayleigh_number(self) -> float:
        delta_t = self.temperature_cmb_k - self.temperature_surface_k
        return (
            self.density_kg_m3
            * self.gravity_m_s2
            * self.thermal_expansion_k_inv
            * delta_t
            * self.thickness_m**3
            / (self.surface_viscosity_pa_s * self.thermal_diffusivity_m2_s)
        )


def make_viscosity_profile(mesh, params: EarthParameters):
    """Return a radial piecewise viscosity normalized by 1e21 Pa s."""

    x, y = mesh.X
    radius = sympy.sqrt(x**2 + y**2)
    r_surface = 1.0

    r_asthenosphere_top = r_surface - (
        params.asthenosphere_top_depth_km / params.surface_radius_km
    )
    r_asthenosphere_base = r_surface - (
        params.asthenosphere_base_depth_km / params.surface_radius_km
    )
    r_lower_mantle_top = r_surface - (
        params.lower_mantle_top_depth_km / params.surface_radius_km
    )

    eta_ref = params.surface_viscosity_pa_s
    eta_surface = params.surface_viscosity_pa_s / eta_ref
    eta_asthenosphere = params.asthenosphere_viscosity_pa_s / eta_ref
    eta_lower_mantle = params.lower_mantle_viscosity_pa_s / eta_ref

    profile = sympy.Piecewise(
        (
            eta_asthenosphere,
            (radius >= r_asthenosphere_base) & (radius <= r_asthenosphere_top),
        ),
        (eta_lower_mantle, radius <= r_lower_mantle_top),
        (eta_surface, True),
    )
    metadata = {
        "r_asthenosphere_top": r_asthenosphere_top,
        "r_asthenosphere_base": r_asthenosphere_base,
        "r_lower_mantle_top": r_lower_mantle_top,
        "eta_surface_nd": eta_surface,
        "eta_asthenosphere_nd": eta_asthenosphere,
        "eta_lower_mantle_nd": eta_lower_mantle,
    }
    return profile, metadata


def build_annulus_model(
    *,
    cell_size_km: float = 250.0,
    steps: int = 10,
    dt: float | None = None,
    return_state: bool = False,
):
    """Build and run the annulus model, returning fields and diagnostics."""

    if cell_size_km <= 0.0:
        raise ValueError("cell_size_km must be positive")
    if steps < 0:
        raise ValueError("steps must be non-negative")

    uw.reset_default_model()
    uw.use_strict_units(False)
    uw.use_nondimensional_scaling(False)

    params = EarthParameters()
    mesh = uw.meshing.Annulus(
        radiusOuter=1.0,
        radiusInner=params.radius_inner,
        cellSize=cell_size_km / params.surface_radius_km,
        qdegree=3,
    )

    velocity = uw.discretisation.MeshVariable(
        "U", mesh, mesh.dim, vtype=uw.VarType.VECTOR, degree=2
    )
    pressure = uw.discretisation.MeshVariable(
        "P", mesh, 1, vtype=uw.VarType.SCALAR, degree=1, continuous=True
    )
    temperature = uw.discretisation.MeshVariable("Theta", mesh, 1, degree=2)

    x, y = mesh.X
    radius = sympy.sqrt(x**2 + y**2)
    radial = sympy.Matrix([x / radius, y / radius])
    tangent = sympy.Matrix([-y / radius, x / radius])

    # The dimensionless temperature is Theta=(T-T_surface)/(T_CMB-T_surface).
    theta_linear = (1.0 - radius) / (1.0 - params.radius_inner)
    theta_perturbation = 0.02 * sympy.sin(2.0 * sympy.atan2(y, x)) * sympy.sin(
        sympy.pi * theta_linear
    )
    initial_theta = theta_linear + theta_perturbation
    temperature.array[...] = uw.function.evaluate(
        initial_theta, temperature.coords
    ).reshape(temperature.array.shape)

    viscosity, viscosity_metadata = make_viscosity_profile(mesh, params)

    stokes = uw.systems.Stokes(
        mesh, velocityField=velocity, pressureField=pressure, verbose=False
    )
    stokes.constitutive_model = uw.constitutive_models.ViscousFlowModel
    stokes.constitutive_model.Parameters.shear_viscosity_0 = viscosity
    stokes.saddle_preconditioner = 1.0 / viscosity

    # Four equal sectors: v_theta=A(theta)*sin(2 theta). The right half
    # (theta=0 divergence) is slow; the left half (theta=pi divergence) is fast.
    slow = params.slow_velocity_cm_per_yr / params.velocity_scale_cm_per_yr
    fast = params.fast_velocity_cm_per_yr / params.velocity_scale_cm_per_yr
    amplitude = sympy.Piecewise((slow, x >= 0.0), (fast, True))
    v_theta = amplitude * 2.0 * x * y / radius**2
    convergent_surface_velocity = v_theta * tangent
    stokes.add_dirichlet_bc(
        (convergent_surface_velocity[0], convergent_surface_velocity[1]), "Upper"
    )
    stokes.add_natural_bc(
        1.0e4 * radial.dot(velocity.sym) * radial,
        "Lower",
    )
    stokes.bodyforce = params.buoyancy_coeff_nd * temperature.sym[0] * radial

    adv_diff = uw.systems.AdvDiffusionSLCN(
        mesh, u_Field=temperature, V_fn=velocity.sym, monotone_mode="clamp"
    )
    adv_diff.constitutive_model = uw.constitutive_models.DiffusionModel
    adv_diff.constitutive_model.Parameters.diffusivity = params.kappa_nd
    adv_diff.theta = 0.5
    adv_diff.add_dirichlet_bc(1.0, "Lower")
    adv_diff.add_dirichlet_bc(0.0, "Upper")

    # A conservative time step for the default mesh.  It may be overridden by
    # --dt in model time units.
    timestep = dt if dt is not None else 0.25 * cell_size_km / params.surface_radius_km

    stokes.solve(zero_init_guess=True)
    for _ in range(steps):
        adv_diff.solve(timestep=timestep, zero_init_guess=True)
        stokes.solve(zero_init_guess=False)

    eta_probe_radius = np.array(
        [
            1.0 - 50.0 / params.surface_radius_km,
            1.0 - 150.0 / params.surface_radius_km,
            1.0 - 1000.0 / params.surface_radius_km,
        ]
    )
    eta_probe_points = np.column_stack((eta_probe_radius, np.zeros(3)))
    eta_probe = np.asarray(
        uw.function.evaluate(viscosity, eta_probe_points), dtype=float
    ).reshape(-1)

    temperature_values = np.asarray(temperature.data[:, 0], dtype=float)
    diagnostics = {
        "temperature_min_nd": float(temperature_values.min()),
        "temperature_max_nd": float(temperature_values.max()),
        "eta_probe_nd": eta_probe.tolist(),
        "rayleigh": params.rayleigh_number,
        "kappa_nd": params.kappa_nd,
        "buoyancy_coeff_nd": params.buoyancy_coeff_nd,
        "dt_nd": timestep,
        "steps": steps,
        "mesh_vertices": int(temperature.coords.shape[0]),
        "viscosity_metadata": viscosity_metadata,
    }

    # The profile and the thermal field are the regression contract.
    assert np.allclose(eta_probe, [1.0, 0.01, 1.0], rtol=0.0, atol=1.0e-12)
    assert np.isfinite(temperature_values).all()
    assert diagnostics["temperature_min_nd"] > -0.05
    assert diagnostics["temperature_max_nd"] < 1.05
    assert math.isclose(
        params.temperature_surface_k, 0.0, rel_tol=0.0, abs_tol=1.0e-12
    )
    assert math.isclose(params.temperature_cmb_k, 2800.0)

    if return_state:
        diagnostics["state"] = {
            "mesh": mesh,
            "velocity": velocity,
            "pressure": pressure,
            "temperature": temperature,
            "viscosity": viscosity,
            "params": params,
        }
    return diagnostics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cell-size-km",
        type=float,
        default=250.0,
        help="Target annulus element size in km (default: 250)",
    )
    parser.add_argument(
        "--steps", type=int, default=10, help="Number of thermal steps (default: 10)"
    )
    parser.add_argument(
        "--dt",
        type=float,
        default=None,
        help="Thermal timestep in model time units; default is 0.25*cell_size/R_surface",
    )
    return parser.parse_args()


def test_earth_annulus_convection_smoke() -> None:
    """Pytest entry point using a coarser, one-step CI-sized configuration."""

    diagnostics = build_annulus_model(cell_size_km=500.0, steps=1)
    assert diagnostics["steps"] == 1
    assert diagnostics["eta_probe_nd"] == [1.0, 0.01, 1.0]


def main() -> None:
    args = parse_args()
    diagnostics = build_annulus_model(
        cell_size_km=args.cell_size_km, steps=args.steps, dt=args.dt
    )
    params = EarthParameters()
    print("Earth annulus convection test: PASS")
    print(f"  mesh vertices: {diagnostics['mesh_vertices']}")
    print(f"  steps / dt: {diagnostics['steps']} / {diagnostics['dt_nd']:.3e}")
    print(f"  T endpoints: {params.temperature_surface_k:g} -> {params.temperature_cmb_k:g} K")
    print(
        "  surface velocities: "
        f"slow={params.slow_velocity_cm_per_yr:g}, "
        f"fast={params.fast_velocity_cm_per_yr:g} cm/yr"
    )
    print(
        "  viscosity probes (surface/asthenosphere/lower mantle): "
        f"{diagnostics['eta_probe_nd']} x 1e21 Pa s"
    )
    print(f"  Rayleigh number: {diagnostics['rayleigh']:.3e}")
    print(
        "  final Theta range: "
        f"[{diagnostics['temperature_min_nd']:.4f}, {diagnostics['temperature_max_nd']:.4f}]"
    )


if __name__ == "__main__":
    main()
