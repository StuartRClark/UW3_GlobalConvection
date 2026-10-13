---
title: "Global convection: from a physical question to an Underworld3 model"
authors:
  - name: Stuart Clark
    orcid: 0000-0002-0495-670X
    affiliations:
      - UNSW Civil and Environmental Engineering
date: "[TODO: publication date]"
doi: "[TODO: assigned when archived]"
keywords:
  - mantle convection
  - global geodynamics
  - Underworld3
  - numerical modelling
  
exports:
  - format: typst
    logo: ../../static/uwtn-logo.png
    series: "Underworld Technical Notes"
    origin_url: "[TODO]"
    template: ../../templates/pdf
    output: running_annulus_convection.pdf
    article_id: "[TODO]"
    software_version: underworld3 0.0.0
---


## Why build a global convection model?

Global convection models connect the thermal and mechanical evolution of a planetary interior to observable surface behaviour. They also combine several numerical decisions—geometry, discretisation, constitutive laws, boundary conditions, timestepping, and diagnostics—that should be documented together rather than treated as independent code settings.

This note is a working template for developing such a model in Underworld3. It begins with the scientific question, describes the physical and numerical representation, and ends with a reproducible run record. The small annulus model in this repository is the prototype used to exercise the workflow; the sections below identify what must be replaced or extended for a global spherical-shell calculation.

[TODO: Introduce the geodynamic problem in the style of a short paper. What part of the thermal, chemical, or mechanical evolution of the planet is being investigated? Why is a global model needed rather than a regional or Cartesian model?]

## Primary benchmarks for the model


## Geometry and reference frame

| Quantity | Symbol | Value | Units | Comment / source |
| --- | --- | ---: | --- | --- |
| Planetary radius | R_p | [TODO] | km | [TODO] |
| Core–mantle boundary radius | R_c | [TODO] | km | [TODO] |
| Domain thickness | D | [TODO] | km | [TODO] |
| Surface gravity | g_s | [TODO] | m s⁻² | [TODO] |
| Rotation rate | Ω | [TODO] | s⁻¹ | [TODO] |

[TODO: Define positive radial, latitudinal, and longitudinal directions. State whether the model is a full sphere, spherical shell, 2-D annulus, axisymmetric slice, or another geometry. Describe symmetry, periodicity, and the treatment of the poles.]

### Fields and materials

| Field or material | Role in the model | Initial state | Evolution |
| --- | --- | --- | --- |
| Temperature | Buoyancy and thermal structure | [TODO] | [TODO] |
| Velocity | Convective transport | [TODO] | Stokes / [TODO] |
| Pressure | Incompressibility constraint | [TODO] | Diagnostic / solve field |
| Composition | [TODO: if used] | [TODO] | [TODO] |
| Phase / damage | [TODO: if used] | [TODO] | [TODO] |

## From equations to a numerical model

### Conservation laws

[TODO: State the equations in the notation used throughout the note. Define every symbol and state which terms are retained or omitted.]

For an incompressible Boussinesq reference model, the equations may be written as

$$
\nabla \cdot \mathbf{u} = 0,
$$

$$
-\nabla \cdot \boldsymbol{\tau} + \nabla p
= \rho_0 \left(1 - \alpha (T-T_0)\right)\mathbf{g} + \mathbf{f},
\qquad
\boldsymbol{\tau}=2\eta\,\boldsymbol{\varepsilon}(\mathbf{u}),
$$

$$
\rho_0 C_p\left(\frac{\partial T}{\partial t} + \mathbf{u}\cdot\nabla T\right)
= \nabla\cdot(k\nabla T) + H + \Phi.
$$

Here \(\mathbf{u}\) is velocity, \(p\) is pressure, \(\eta\) is viscosity, \(T\) is temperature, \(H\) is internal heating, and \(\Phi\) is viscous dissipation. [TODO: Explain whether compressibility, adiabatic heating, latent heat, self-gravity, rotation, or chemical buoyancy are included.]

### Scales and dimensionless numbers

| Scale or number | Definition | Value | Purpose |
| --- | --- | ---: | --- |
| Length | D | [TODO] | [TODO] |
| Temperature difference | ΔT | [TODO] | [TODO] |
| Reference viscosity | η_0 | [TODO] | [TODO] |
| Time | [TODO] | [TODO] | [TODO] |
| Rayleigh number | [TODO] | [TODO] | Convective vigor |
| Peclet number | [TODO] | [TODO] | Advective versus diffusive transport |
| Reynolds number | [TODO] | [TODO] | Inertial importance |

[TODO: Give the formulae used to calculate the dimensionless numbers and state whether values are based on dimensional input parameters or nondimensionalised code parameters.]

### Rheology

[TODO: Describe the constitutive law in words before giving the implementation. Explain which material properties vary with depth, temperature, pressure, strain rate, composition, or phase.]

$$
\eta = [TODO: complete viscosity law].
$$

| Region / material | Depth or field criterion | Viscosity / rheology | Transition |
| --- | --- | --- | --- |
| Lithosphere / surface | [TODO] | [TODO] | [TODO] |
| Asthenosphere | [TODO] | [TODO] | [TODO] |
| Lower mantle | [TODO] | [TODO] | [TODO] |
| Core / excluded region | [TODO] | [TODO] | [TODO] |

[TODO: State whether interfaces are sharp, smoothed, advected, or defined by a phase or composition field. If yielding or damage is used, give the yield criterion and regularisation.]

## Boundary conditions are part of the model

Boundary conditions determine how the physical problem is driven. Describe them in physical language first, then explain how they are imposed in Underworld3.

### Initial conditions

| Field | Initial condition | Perturbation / noise | Justification |
| --- | --- | --- | --- |
| Temperature | [TODO] | [TODO] | [TODO] |
| Velocity | [TODO] | [TODO] | [TODO] |
| Composition | [TODO] | [TODO] | [TODO] |
| Phase / damage | [TODO] | [TODO] | [TODO] |

### Boundary conditions

| Boundary | Velocity | Temperature / heat flux | Composition / phase | Numerical implementation |
| --- | --- | --- | --- | --- |
| Surface | [TODO] | [TODO] | [TODO] | [TODO] |
| Core–mantle boundary | [TODO] | [TODO] | [TODO] | [TODO] |
| Lateral / periodic | [TODO] | [TODO] | [TODO] | [TODO] |

[TODO: Explain free slip, no slip, imposed plate or surface velocities, open boundaries, periodicity, and any moving or deforming boundaries.]

## A small model before the global model

The annulus experiment provides a controlled test of the workflow. It uses a temperature range of 0–2800 K, a radial viscosity profile, multiple timesteps, and four equal surface-velocity sectors. The displayed velocity arrows are normalised for visualisation and do not change the solved field.

~~~{figure} ../images/initial_final_models.png
:name: fig-annulus-prototype
:alt: Initial and final temperature fields for the annulus prototype.

**Figure 1:** Prototype annulus calculation showing the initial and final temperature fields and the normalised velocity vectors. [TODO: Replace or supplement this with the global model overview.]
~~~

This prototype is useful because it separates software and numerical questions from the larger scientific question: can the environment be built, can the fields and boundary conditions be represented, does the solver advance for several timesteps, and are the results written reproducibly?

## Building the Model with ChatGPT

### Construct the model in stages

The implementation should make the physical choices visible. A typical build function has the following shape:

~~~python
def build_global_convection_model(parameters):
    # 1. Define dimensional parameters and reference scales.
    # 2. Create the spherical-shell mesh and boundary labels.
    # 3. Create velocity, pressure, temperature, and optional swarm fields.
    # 4. Define gravity, buoyancy, viscosity, and constitutive laws.
    # 5. Apply initial and boundary conditions.
    # 6. Construct the Stokes and thermal systems.
    # 7. Return the model objects plus diagnostics and output configuration.
    pass
~~~

[TODO: Replace this outline with the actual function names and link to the implementation.]

### Mesh and discretisation choices

| Choice | Value | Why this choice? |
| --- | --- | --- |
| Mesh type | [TODO] | [TODO] |
| Domain resolution | [TODO] | [TODO] |
| Velocity / pressure spaces | [TODO] | [TODO] |
| Temperature space | [TODO] | [TODO] |
| Swarm particles per cell | [TODO] | [TODO] |
| Refinement / remeshing | [TODO] | [TODO] |

### Solvers and timestep control

| Component | Solver / preconditioner | Tolerance | Maximum iterations |
| --- | --- | ---: | ---: |
| Stokes | [TODO] | [TODO] | [TODO] |
| Thermal advection–diffusion | [TODO] | [TODO] | [TODO] |
| Projection / swarm update | [TODO] | [TODO] | [TODO] |

- Timestep rule: [TODO]
- Initial timestep: [TODO]
- Minimum and maximum timestep: [TODO]
- Checkpoint interval: [TODO]
- Restart policy: [TODO]

## Running the model

### Interactive notebook run

From the Underworld3 checkout:

~~~bash
pixi run -e runtime jupyter notebook ../earth_annulus_convection.ipynb
~~~

[TODO: Replace the prototype notebook with the global model notebook or script path.]

### Batch or HPC run

~~~bash
mpirun -np [NPROCS] python global_convection_model.py \
  --resolution [TODO] \
  --steps [TODO] \
  --output [TODO]
~~~

Record the host, processor count, wall time, memory, scheduler request, environment lockfile, command line, and exit status for every production run.

### Checkpoints and restart

[TODO: Describe checkpoint files, restart commands, output naming, and how an interrupted run is recovered.]

## What should be measured?

The model output is not just a collection of snapshots. Each diagnostic should connect to a question or a numerical check.

| Diagnostic | Definition / method | Output cadence | Scientific or numerical use |
| --- | --- | --- | --- |
| Temperature range | [TODO] | [TODO] | [TODO] |
| RMS velocity | [TODO] | [TODO] | [TODO] |
| Surface heat flux | [TODO] | [TODO] | [TODO] |
| CMB heat flux | [TODO] | [TODO] | [TODO] |
| Viscosity range | [TODO] | [TODO] | [TODO] |
| Divergence residual | [TODO] | [TODO] | [TODO] |
| Solver convergence | [TODO] | [TODO] | [TODO] |
| Physical time | [TODO] | [TODO] | [TODO] |

### Figures and tables

1. [TODO: Geometry, mesh, and boundary labels]
2. [TODO: Initial temperature and composition]
3. [TODO: Velocity field and surface boundary conditions]
4. [TODO: Viscosity structure]
5. [TODO: Heat flux, energy, and timestep histories]
6. [TODO: Final state and comparison with the initial state]
7. [TODO: Resolution and timestep sensitivity]

~~~{figure} ../images/viscosity_profile.png
:name: fig-prototype-viscosity
:alt: Radial viscosity profile for the annulus prototype.

**Figure 2:** Prototype viscosity profile. [TODO: Replace with the global radial and lateral rheology figure.]
~~~

## Verification, validation, and sensitivity

### Verification

[TODO: Record import tests, unit tests, conservation checks, analytical solutions, manufactured solutions, and benchmark comparisons.]

### Resolution and timestep studies

| Case | Resolution | Timestep | Observable | Difference from reference |
| --- | --- | --- | --- | --- |
| Coarse | [TODO] | [TODO] | [TODO] | [TODO] |
| Reference | [TODO] | [TODO] | [TODO] | [TODO] |
| Fine | [TODO] | [TODO] | [TODO] | [TODO] |

[TODO: State the tolerance used to decide whether a result is numerically converged.]

### Physical sensitivity

[TODO: Identify uncertain parameters and give the experiment matrix. State which conclusions are robust and which depend on calibration choices.]

## Results and interpretation

[TODO: Write this section as a short paper rather than a notebook transcript. Introduce the result, point to the relevant figure or table, explain the mechanism, and distinguish observation from interpretation.]

### Main results

[TODO]

### Unexpected behaviour

[TODO: Record instabilities, solver failures, nonphysical structures, and features requiring further investigation.]


## Directions to go



## Reproducibility

| Item | Value / link |
| --- | --- |
| Project repository | [TODO] |
| Model script / notebook | [TODO] |
| Underworld3 repository | [TODO] |
| Underworld3 commit | [TODO] |
| Environment lockfile | [TODO] |
| Input parameters | [TODO] |
| Output archive | [TODO] |
| Random seed | [TODO] |
| Hardware / MPI layout | [TODO] |
| Run date and operator | [TODO] |

The final note should allow a reader to answer five questions: what was modelled, which equations and parameters were used, how the run was performed, how the result was checked, and where the exact input and output can be found.

~~~{admonition} Reproducibility checklist
:class: important

- [ ] A fresh environment can be built from the recorded commands.
- [ ] The exact code commit and input parameters are archived.
- [ ] The run can be restarted from a documented checkpoint.
- [ ] Figures and tables can be regenerated without manual edits.
- [ ] The production run has a complete log and exit status.
- [ ] Verification and sensitivity checks are reported.
~~~

## Comments

Discussion of this note should happen alongside the source repository so that modelling decisions, code changes, and review comments remain connected.

[TODO: Add the project GitHub Discussions URL or issue link.]

## References

1. [TODO: Underworld3 software or release reference]
2. [TODO: Physical parameter sources]
3. [TODO: Convection benchmark or validation reference]
4. [TODO: Plate reconstruction, geochemical, or observational data source]

[TODO: Use DOI links where available and keep the bibliography in the format used by the final technical-note site.]
