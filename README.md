<<<<<<< HEAD
# Underworld3 annulus model built with ChatGPT

This repository demonstrates how to set up [Underworld3](https://github.com/underworldcode/underworld3) with ChatGPT and run a small 2-D annulus convection model representing the Earth's mantle.

The example was developed through a sequence of natural-language prompts. ChatGPT installed and verified the Underworld3 runtime, installed Jupyter, created the model, ran the simulation, and produced the diagnostic figures stored in this repository.

## Model

The annulus spans from a 3480 km core–mantle boundary to a 6371 km surface and uses a temperature range of 0–2800 K. Its viscosity profile is:

- `10^21 Pa s` at the surface
- `10^19 Pa s` in the 100–250 km asthenosphere
- `10^21 Pa s` in the lower mantle below 660 km depth

The surface velocity has four equal angular sectors: slow divergence at 2 cm/yr, fast divergence at 6 cm/yr, and convergence in the two intervening sectors. The simulation runs for multiple timesteps and compares the initial and final temperature fields.

Velocity arrows in the figures are normalized for display only. The longest arrow is 5% of the plotted width; because the normalized annulus spans from -1 to 1, the displayed maximum length is 0.10 coordinate units.

## Contents

- [`earth_annulus_convection.ipynb`](earth_annulus_convection.ipynb) — self-contained executable notebook.
- [`test_annulus_convection.py`](test_annulus_convection.py) — command-line smoke/regression test.
- [`underworld3_chatgpt_build_guide.md`](underworld3_chatgpt_build_guide.md) — prompt-by-prompt setup explanation.
- [`images/initial_final_models.png`](images/initial_final_models.png) — initial and final model output.
- [`images/viscosity_profile.png`](images/viscosity_profile.png) — configured viscosity profile.

## Install Underworld3 with ChatGPT

In the original workflow, ChatGPT performed these installation commands in the shared workspace:

```bash
git clone https://github.com/underworldcode/underworld3.git
cd underworld3
./uw setup
./uw build
./uw doctor
```

The setup used the runtime environment, no AMR, and the platform-default MPICH implementation when prompted by `./uw setup`.

## Install Jupyter with ChatGPT

ChatGPT installed the notebook interface into the same Underworld3 runtime:

```bash
pixi run -e runtime pip install notebook
```

Using the same runtime for both Underworld3 and Jupyter avoids importing Underworld3 from the wrong Python environment.

## Run the notebook

From the Underworld3 checkout, launch the notebook with:

```bash
pixi run -e runtime jupyter notebook ../annulus_2D/earth_annulus_convection.ipynb
```

To execute it non-interactively and refresh its stored outputs:

```bash
pixi run -e runtime jupyter nbconvert \
  --to notebook \
  --execute ../annulus_2D/earth_annulus_convection.ipynb \
  --inplace \
  --ExecutePreprocessor.timeout=900
```

Run the smoke test with:

```bash
pixi run -e runtime python ../annulus_2D/test_annulus_convection.py --steps 20
```

The test checks the temperature endpoints, viscosity probes, Rayleigh number, four-sector surface velocity setup, and final normalized temperature range.

## Example output

![Initial and final temperature fields with normalized velocity vectors](images/initial_final_models.png)

![Configured radial viscosity profile](images/viscosity_profile.png)

The tested configuration reports `Earth annulus convection test: PASS` with slow and fast surface velocities of 2 and 6 cm/yr and viscosity probes of `[1.0, 0.01, 1.0] x 10^21 Pa s`.
=======
# UW3_GlobalConvection
Underworld3 global convection
>>>>>>> origin/main
