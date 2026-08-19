#!/bin/bash
#SBATCH --job-name=sierpinski_binary
#SBATCH --partition=comp3710
#SBATCH --account=comp3710
#SBATCH --gres=gpu:1
#SBATCH --time=00:05:00
#SBATCH --output=outputs/sierpinski_%j.out
#SBATCH --error=outputs/sierpinski_%j.err

cd "$SLURM_SUBMIT_DIR"

echo "hostname: $(hostname)"
echo "Slurm job ID: $SLURM_JOB_ID"
echo "Slurm submit directory: $SLURM_SUBMIT_DIR"

echo "nvidia-smi output:"
nvidia-smi

source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda activate torch

export MPLBACKEND=Agg

python src/sierpinski.py
