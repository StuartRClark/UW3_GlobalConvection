# Global convection model: technical note

**UWTN [TODO: year-number]**

## Authors

`[TODO: Name]`

## Affiliations

`[TODO: Institution, department, and/or project]`

`[TODO: Additional authors and affiliations]`

`[TODO: Date]`

**Version:** `[TODO]`  
**DOI:** `[TODO: assigned at publication; leave blank while drafting]`

**Keywords:** global convection; mantle dynamics; Underworld3; `[TODO]`

```{admonition} Working document
:class: note

This is a fill-in skeleton for a global Underworld3 convection model. Replace bracketed fields, remove guidance text, and attach the final run record before treating the note as complete.
```

## Document control

| Field | Value |
| --- | --- |
| Project / model name | `[TODO]` |
| Technical note number | `[TODO]` |
| Version | `[TODO]` |
| Status | Draft / Review / Final |
| Authors | `[TODO]` |
| Date | `[TODO]` |
| Underworld3 version / commit | `[TODO]` |
| Repository and branch | `[TODO]` |
| Primary contact | `[TODO]` |

## Abstract

`[TODO: State the scientific question, model configuration, principal results, and the main limitations in 150–250 words.]`

## 1. Purpose and scientific objectives

### 1.1 Purpose

`[TODO: Explain why this global convection model is being developed and what decision, hypothesis, or scientific question it is intended to address.]`

### 1.2 Research questions

1. `[TODO]`
2. `[TODO]`
3. `[TODO]`

### 1.3 Success criteria

| Criterion | Measurement | Target / acceptance threshold |
| --- | --- | --- |
| Model builds | `./uw doctor`, import test | `[TODO]` |
| Numerical solve completes | Exit status and run log | `[TODO]` |
| Conservation | Thermal / mass / energy residual | `[TODO]` |
| Resolution sensitivity | Mesh refinement comparison | `[TODO]` |
| Physical plausibility | Diagnostic range / benchmark | `[TODO]` |

## 2. Model scope and assumptions

### 2.1 Scope

- Domain: `[TODO: full sphere / spherical shell / regional domain]`
- Dimension: `[TODO: 2-D axisymmetric / 3-D]`
- Model duration: `[TODO]`
- Intended use: `[TODO: exploratory / benchmark / production / teaching]`

### 2.2 Assumptions

| Assumption | Rationale | Consequence / limitation |
| --- | --- | --- |
| `[TODO]` | `[TODO]` | `[TODO]` |
| `[TODO]` | `[TODO]` | `[TODO]` |

### 2.3 Excluded physics

`[TODO: List processes deliberately omitted, such as compressibility, phase transitions, melting, chemical diffusion, elasticity, or self-gravitation.]`

## 3. Geometry, coordinates, and reference frame

### 3.1 Geometry

| Quantity | Symbol | Value | Units | Source / rationale |
| --- | --- | ---: | --- | --- |
| Planetary radius | `R_p` | `[TODO]` | km | `[TODO]` |
| Core radius | `R_c` | `[TODO]` | km | `[TODO]` |
| Lithosphere thickness | `d_l` | `[TODO]` | km | `[TODO]` |
| Domain thickness | `D` | `[TODO]` | km | `[TODO]` |

`[TODO: Describe the mesh topology, radial coordinate convention, longitude/latitude convention, and any symmetry or periodicity.]`

### 3.2 Reference frame

- Frame: `[TODO: mantle / surface / barycentric / rotating]`
- Rotation rate: `[TODO]`
- Gravity direction and sign convention: `[TODO]`
- Velocity sign convention: `[TODO]`

```{admonition} Coordinate convention
:class: tip

Write one explicit sentence defining positive radial, latitudinal, longitudinal, and vertical directions. Include a small diagram or link to one when the geometry is non-Cartesian.
```

## 4. Governing equations

### 4.1 Conservation of mass

`[TODO: State the incompressible or compressible continuity equation and define all symbols.]`

$$
\nabla \cdot \mathbf{u} = [TODO].
$$

### 4.2 Momentum balance

`[TODO: State the Stokes or inertial momentum equation, body forces, pressure convention, and buoyancy approximation.]`

$$
-\nabla \cdot \boldsymbol{\tau} + \nabla p = \rho\mathbf{g} + \mathbf{f},
\qquad
\boldsymbol{\tau} = [TODO].
$$

### 4.3 Thermal energy

`[TODO: State the thermal equation, including advection, diffusion, internal heating, and viscous dissipation if included.]`

$$
\rho C_p \left(\frac{\partial T}{\partial t} + \mathbf{u}\cdot\nabla T\right)
= \nabla\cdot(k\nabla T) + H + [TODO].
$$

### 4.4 Composition or phase fields

`[TODO: Add equations for composition, phase, damage, or other transported fields. Delete this section if not applicable.]`

## 5. Dimensional and nondimensional parameters

### 5.1 Reference scales

| Scale | Symbol | Value | Units |
| --- | --- | ---: | --- |
| Length | `D` | `[TODO]` | m |
| Velocity | `U` | `[TODO]` | m s⁻¹ |
| Time | `D/U` | `[TODO]` | s / Myr |
| Temperature | `ΔT` | `[TODO]` | K |
| Viscosity | `η_0` | `[TODO]` | Pa s |
| Density | `ρ_0` | `[TODO]` | kg m⁻³ |

### 5.2 Material and physical parameters

| Parameter | Symbol | Value | Units | Spatial / temporal dependence |
| --- | --- | ---: | --- | --- |
| Gravity | `g` | `[TODO]` | m s⁻² | `[TODO]` |
| Thermal expansivity | `α` | `[TODO]` | K⁻¹ | `[TODO]` |
| Heat capacity | `C_p` | `[TODO]` | J kg⁻¹ K⁻¹ | `[TODO]` |
| Thermal conductivity | `k` | `[TODO]` | W m⁻¹ K⁻¹ | `[TODO]` |
| Diffusivity | `κ` | `[TODO]` | m² s⁻¹ | `[TODO]` |
| Internal heating | `H` | `[TODO]` | W kg⁻¹ / W m⁻³ | `[TODO]` |

### 5.3 Dimensionless numbers

| Number | Definition | Value | Interpretation |
| --- | --- | ---: | --- |
| Rayleigh | `[TODO]` | `[TODO]` | `[TODO]` |
| Prandtl | `[TODO]` | `[TODO]` | `[TODO]` |
| Peclet | `[TODO]` | `[TODO]` | `[TODO]` |
| Reynolds | `[TODO]` | `[TODO]` | `[TODO]` |

## 6. Rheology and material model

### 6.1 Viscosity law

`[TODO: Give the complete viscosity equation, including temperature, pressure, stress, composition, depth, and strain-rate dependencies.]`

$$
\eta = [TODO].
$$

### 6.2 Radial and lateral structure

| Region / material | Depth or field criterion | Viscosity / rheology | Transition treatment |
| --- | --- | --- | --- |
| `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` |
| `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` |

`[TODO: State whether material interfaces are sharp, smoothed, advected, or determined by a phase/composition field.]`

### 6.3 Yielding, damage, or plasticity

`[TODO: Describe yield criterion, regularisation, plastic viscosity, stress cap, and parameter values. Delete if not applicable.]`

## 7. Initial and boundary conditions

### 7.1 Initial conditions

| Field | Initial condition | Perturbation / noise | Source |
| --- | --- | --- | --- |
| Temperature | `[TODO]` | `[TODO]` | `[TODO]` |
| Velocity | `[TODO]` | `[TODO]` | `[TODO]` |
| Composition | `[TODO]` | `[TODO]` | `[TODO]` |
| Phase | `[TODO]` | `[TODO]` | `[TODO]` |

### 7.2 Boundary conditions

| Boundary | Velocity | Temperature / heat flux | Composition / phase | Implementation |
| --- | --- | --- | --- | --- |
| Surface | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` |
| CMB | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` |
| Lateral / periodic | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` |

`[TODO: Explain how plate velocities, imposed surface motion, free slip, no slip, open boundaries, or moving meshes are represented in Underworld3.]`

## 8. Underworld3 implementation

### 8.1 Environment and installation

```bash
git clone https://github.com/underworldcode/underworld3.git
cd underworld3
./uw setup
./uw build
./uw doctor
```

Record the selected environment, Python version, PETSc version, MPI implementation, and any local modifications:

| Item | Value |
| --- | --- |
| Underworld3 commit | `[TODO]` |
| Environment | `[TODO]` |
| Python | `[TODO]` |
| PETSc | `[TODO]` |
| MPI | `[TODO]` |
| Jupyter package | `[TODO]` |

### 8.2 Model construction outline

```python
import underworld3 as uw

# 1. Define dimensional parameters and reference scales.
# 2. Create the spherical or annular mesh.
# 3. Create velocity, pressure, temperature, and optional swarm fields.
# 4. Define gravity, buoyancy, viscosity, and constitutive laws.
# 5. Apply initial and boundary conditions.
# 6. Construct Stokes and advection-diffusion systems.
# 7. Solve, diagnose, checkpoint, and write output.
```

### 8.3 Mesh and discretisation

| Item | Choice | Rationale |
| --- | --- | --- |
| Mesh type | `[TODO]` | `[TODO]` |
| Resolution | `[TODO]` | `[TODO]` |
| Velocity / pressure order | `[TODO]` | `[TODO]` |
| Temperature order | `[TODO]` | `[TODO]` |
| Swarm particles per cell | `[TODO]` | `[TODO]` |
| Refinement / remeshing | `[TODO]` | `[TODO]` |

### 8.4 Solvers and timestep control

| Component | Solver / preconditioner | Tolerance | Maximum iterations |
| --- | --- | ---: | ---: |
| Stokes | `[TODO]` | `[TODO]` | `[TODO]` |
| Thermal | `[TODO]` | `[TODO]` | `[TODO]` |
| Projection / swarm update | `[TODO]` | `[TODO]` | `[TODO]` |

- Timestep rule: `[TODO]`
- Initial timestep: `[TODO]`
- Minimum / maximum timestep: `[TODO]`
- Checkpoint interval: `[TODO]`
- Restart policy: `[TODO]`

## 9. Run procedure

### 9.1 Local workstation

```bash
pixi run -e runtime jupyter notebook ../global_convection_model.ipynb
```

### 9.2 Batch / HPC execution

```bash
# [TODO: Replace with the scheduler and launch command used by the project.]
mpirun -np [NPROCS] python global_convection_model.py \
  --resolution [TODO] \
  --steps [TODO] \
  --output [TODO]
```

Record the machine, processor count, wall time, memory, scheduler request, and environment lockfile for every production run.

### 9.3 Restart and checkpointing

`[TODO: Specify checkpoint files, restart command, output naming convention, and how partial or failed runs are recovered.]`

## 10. Diagnostics and outputs

### 10.1 Required diagnostics

- Temperature minimum, maximum, mean, and surface/CMB profiles.
- RMS, maximum, and representative velocity values.
- Surface heat flux and globally integrated heat flow.
- Viscosity range and representative material probes.
- Divergence or continuity residual.
- Linear/nonlinear solver iterations and convergence reason.
- Timestep, physical time, and wall-clock time.

### 10.2 Output catalogue

| Output | Format | Frequency | Location | Purpose |
| --- | --- | --- | --- | --- |
| Mesh / fields | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` |
| Swarm / particles | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` |
| Run log | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` |
| Summary diagnostics | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` |
| Figures | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` |

### 10.3 Figures to include

1. `[TODO: Initial temperature/composition structure]`
2. `[TODO: Final temperature/composition structure]`
3. `[TODO: Velocity field and plate boundary conditions]`
4. `[TODO: Radial or lateral viscosity profile]`
5. `[TODO: Heat flux / Nusselt / energy history]`
6. `[TODO: Resolution or timestep comparison]`

## 11. Verification, validation, and sensitivity

### 11.1 Code and setup verification

`[TODO: Record import tests, unit tests, dry runs, analytical solutions, and benchmark comparisons.]`

### 11.2 Resolution study

| Case | Resolution | Timesteps | Key observable | Difference from reference |
| --- | --- | ---: | --- | ---: |
| Coarse | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` |
| Reference | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` |
| Fine | `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` |

### 11.3 Timestep study

`[TODO: Demonstrate that reducing the timestep does not materially change the quantities of interest.]`

### 11.4 Physical sensitivity study

`[TODO: Identify uncertain parameters and the experiment matrix. State which conclusions are robust and which depend on calibration choices.]`

## 12. Results and interpretation

### 12.1 Main results

`[TODO: Summarise the results using the diagnostics defined above. Link each claim to a figure, table, or output file.]`

### 12.2 Interpretation

`[TODO: Explain the geodynamic interpretation, expected mechanisms, and alternative explanations.]`

### 12.3 Unexpected behaviour

`[TODO: Record numerical instabilities, nonphysical structures, solver failures, or features requiring further investigation.]`

## 13. Reproducibility and provenance

| Item | Value / link |
| --- | --- |
| Project repository | `[TODO]` |
| Model script / notebook | `[TODO]` |
| Underworld3 repository | `[TODO]` |
| Underworld3 commit | `[TODO]` |
| Environment lockfile | `[TODO]` |
| Input parameters | `[TODO]` |
| Output archive | `[TODO]` |
| Random seed | `[TODO]` |
| Hardware / MPI layout | `[TODO]` |
| Run date and operator | `[TODO]` |

```{admonition} Reproducibility checklist
:class: important

- [ ] A fresh environment can be built from the recorded commands.
- [ ] The exact code commit and input parameters are archived.
- [ ] The run can be restarted from a documented checkpoint.
- [ ] Figures can be regenerated without manual edits.
- [ ] The production run has a complete log and exit status.
- [ ] The model passes the stated verification and sensitivity checks.
```

## 14. Limitations and next steps

### 14.1 Current limitations

1. `[TODO]`
2. `[TODO]`
3. `[TODO]`

### 14.2 Planned improvements

1. `[TODO]`
2. `[TODO]`
3. `[TODO]`

## Appendix A. Complete parameter record

`[TODO: Include one machine-readable or copy-pasteable parameter block for the final run.]`

```yaml
model_name: "[TODO]"
underworld3_commit: "[TODO]"
dimension: "[TODO]"
geometry: "[TODO]"
resolution: "[TODO]"
steps: "[TODO]"
seed: "[TODO]"
```

## Appendix B. Run log excerpt

```text
[TODO: Paste the command, environment summary, solver convergence, timestep summary,
diagnostic checks, and final exit status here.]
```

## Appendix C. References

1. `[TODO: Underworld3 release / software paper]`
2. `[TODO: Physical parameter sources]`
3. `[TODO: Benchmark or validation reference]`
4. `[TODO: Data or plate reconstruction source]`
