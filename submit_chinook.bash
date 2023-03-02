#!/bin/bash

#SBATCH -p t1standard
#SBATCH --ntasks=64
#SBATCH -t 240
#SBATCH --output=%j.o
#SBATCH --job-name=DSM

ulimit -s unlimited
ulimit -l unlimited

umask 022
NPROC=64
mpiexec -n $NPROC dsmti  <data/010109.inf
