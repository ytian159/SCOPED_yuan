import os 
#import wget
import urllib.request
import requests
import shutil
import fileinput
from pysep import recsec
from pysep.recsec import plotw_rs
from obspy import read, Stream,read_events
from glob import glob
import pandas as pd
from pysep.utils.io import read_sem, read_sem_cartesian
from pysep.utils.io import read_stations
from obspy.geodetics import gps2dist_azimuth, kilometer2degrees
import numpy as np

def set_compile_paramters(makefile,dsmtif,maxngrid_r,maxlmax,max_nstation):
    with fileinput.FileInput(makefile, 
                            inplace = True, backup ='.bak') as f:     
        for line in f:
            if "mpif90" in line :
                print(line.replace("mpif90",
                                "mpif90 -std=legacy"), end ='')
            elif "ifort" in line:
                print(line.replace("ifort",
                               "gfortran"), end ='')
            else:
                print(line, end ='')
    with fileinput.FileInput(dsmtif, 
                            inplace = True, backup ='.bak') as f:
        
        for line in f:
            if "parameter ( maxnlay" in line:
                print('        parameter ( maxnlay= '+str(maxngrid_r)+' )', end ='\n')
            elif "parameter ( maxlmax" in line:
                print('        parameter ( maxlmax= '+str(maxlmax)+' )', end ='\n')
            elif "parameter ( maxnr" in line:
                print('        parameter ( maxnr= '+str(max_nstation)+' )', end ='\n')
            elif "parameter ( spcform" in line:
                print('        parameter ( spcform= 1 )  ! 0:binary, 1:ascii', end ='\n')
            else:
                print(line, end ='')

url_dsm='https://github.com/UT-GlobalSeismology/DSMsynTI-mpi/archive/refs/heads/master.zip'
dsmti_file = urllib.request.urlretrieve(url_dsm,'DSMsynTI-mpi-master.zip')
file = shutil.unpack_archive(dsmti_file[0],'./')
maxngrid_r=88300
maxlmax=80000
max_nstation = 1500
makefile='makefile'
use_own_data=1
dir_path=dsmti_file[0][:-4]
os.chdir(dir_path)
main_file='tish.f'
os.chdir('tish-mpi')
set_compile_paramters(makefile,main_file,maxngrid_r,maxlmax,max_nstation)
os.system('make')
os.system('./tish <examples/test1.inf')
os.chdir('../tipsv-mpi')
main_file='tipsv.f'
set_compile_paramters(makefile,main_file,maxngrid_r,maxlmax,max_nstation)
os.system('make')
os.system('./tipsv <examples/test1.inf')
os.chdir('../spcsac')
with fileinput.FileInput(makefile, 
                        inplace = True, backup ='.bak') as f:     
    for line in f:
        if "CC =" in line :
            print(line.replace("icx",
                            "gcc"), end ='')
        else:
            print(line, end ='')
os.system('make')
os.chdir('example')
if use_own_data==1:
    os.system('cp ../../tish-mpi/examples/*spc .')
    os.system('cp ../../tipsv-mpi/examples/*spc .')
os.system('../spcsac -l 8')

