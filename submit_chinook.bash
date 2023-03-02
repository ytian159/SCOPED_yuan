#!/bin/bash

#SBATCH -p debug
#SBATCH --ntasks=4
#SBATCH -t 60
#SBATCH --output=%j.o
#SBATCH --job-name=go_solver

ulimit -s unlimited
ulimit -l unlimited

umask 022
NPROC=8
mpiexec -n $NPROC dsmti  <data/010109.inf
