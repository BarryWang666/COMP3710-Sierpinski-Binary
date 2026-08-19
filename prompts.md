# prompts.md

## Prompt 1: Initial Repository Structure

### User Prompt

Set up the initial repository structure for the UQ COMP3710 Part 3 fractal project, titled "Sierpinski Gasket by Binary Addresses", based on Section 2.10 of *Fractals for the Classroom*. Create AGENTS.md, prompts.md, .gitignore, src/, jobs/, outputs/, analysis/, and outputs/.gitkeep. Update README.md with only the current project description. Do not create any Python implementation yet.

### AI Assistance Summary

- Created the initial repository scaffolding.
- Added project rules to AGENTS.md.
- Added ignore rules while keeping PNG files trackable.
- Updated README.md to describe the project without claiming implementation or analysis is complete.
- Started this prompts.md log.

### Problems Encountered

- No problems encountered. The repository initially contained only README.md and Git metadata.

### Changes Made

- Added AGENTS.md.
- Added prompts.md.
- Added .gitignore.
- Added src/.
- Added jobs/.
- Added outputs/.
- Added outputs/.gitkeep.
- Added analysis/.
- Updated README.md.

## Prompt 2: Baseline Binary-Address Sierpinski Implementation

### User Prompt

Implement the first baseline version of the Sierpinski Gasket by Binary Addresses in src/sierpinski.py, using the Section 2.10 rule `(x AND (y - x)) == 0` for integer coordinates with `0 <= x <= y`. Use PyTorch tensors on CUDA if available, otherwise CPU; use size 1024; avoid Python loops over pixels; produce a centred raster using `pixel_x = 2*x + (size - 1 - y)`; save `outputs/sierpinski_binary.png`; print device, grid size, output shape, selected point count, and selected fraction. Do not add analysis, benchmarking, multiple resolutions, classes, Slurm jobs, README changes, or another Sierpinski algorithm.

### AI Assistance Summary

- Added a simple PyTorch implementation in src/sierpinski.py.
- Used vectorised tensor operations for coordinate generation, the triangular validity mask, the binary-address bitwise test, and raster placement.
- Selected CUDA automatically when available, otherwise CPU.
- Saved the final black-background and white-fractal image to outputs/sierpinski_binary.png.

### Problems Encountered

- The default `python` command was not available in the local shell.
- The default `python3` environment had PyTorch installed but was missing Matplotlib, so Matplotlib was installed with `python3 -m pip install --user matplotlib` before verification.

### Changes Made

- Added src/sierpinski.py.
- Updated prompts.md.
- Generated outputs/sierpinski_binary.png by running the script.

## Prompt 3: Rangpur Slurm Job Script

### User Prompt

Create jobs/sierpinski_job.sh for running src/sierpinski.py on UQ Rangpur. Use job name `sierpinski_binary`, partition/account `comp3710`, exactly one GPU, a five-minute time limit, stdout/stderr under outputs with the Slurm job ID, no memory request, `cd "$SLURM_SUBMIT_DIR"`, diagnostic prints for hostname, job ID, submit directory, and nvidia-smi, activate the `$HOME/miniconda3` conda environment `torch`, set `MPLBACKEND=Agg`, and run `python src/sierpinski.py`. Do not modify the Python implementation, README, benchmarking, or fractal dimension analysis.

### AI Assistance Summary

- Added a Slurm batch script for running the baseline Sierpinski binary-address implementation on UQ Rangpur.
- Included the requested GPU, partition, account, time, output, and error directives.
- Added diagnostic output and conda activation before running the Python script.
- Avoided any memory request because of the current Rangpur A100 Slurm memory reporting issue.

### Problems Encountered

- No problems encountered.

### Changes Made

- Added jobs/sierpinski_job.sh.
- Updated prompts.md.
