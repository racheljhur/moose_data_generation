#!/bin/bash
#SBATCH -J sweep_moose_{pattern}                  		
#SBATCH -N 1 -n 24 --mem-per-cpu 20gb
#SBATCH -t 5:00:00
#SBATCH -A gts-skalidindi7
#SBATCH --mail-type NONE                          
#SBATCH -o slurm_outputs/%j.out   

# conda activate moose

# make sure moose conda is loaded before launching the job
export PATH=/storage/coda1/p-skalidindi7/0/shared/MOOSE/miniforge/bin:$PATH

cd /storage/coda1/p-skalidindi7/0/shared/MOOSE/pmc_response/large_data_response/linear_elastic/inp_files

echo $SLURM_JOB_ID

pwd

# Add any cli overrides
# ./scripts/sweep_solvers.sh "$@"

# run python script
srun python run_all_{pattern}.py
