# SCOPED_yuan
This is a Python notebook run DSM. This notebook will need pysep environment to run. 
To install pysep, please refer to 'https://adjtomo.github.io/pysep/'
The commands goes: 

conda create -n pysep

conda activate pysep

conda install cartopy

pip install pysep-adjtomo

The notebook Run_DSM_simple.ipynb runs the default example with one core. 
The notebook Run_DSM_nenana.ipynb runs DSM with user's CMTSOLUTION and STATION files input and MPI.

To run DSM on UAF Chinook04 cluster
excute the following python scripy in pysep environment:

python make_dsm.py

python run_dsm_python.py

python plot_dsm.py

Yuan Tian 2023/02/28 @ UAF
