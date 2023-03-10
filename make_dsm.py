import os 
#import wget
import urllib.request
import tarfile
import fileinput


mpi=1
if mpi==1:

    url_dsm='https://www.eri.u-tokyo.ac.jp/people/takeuchi/software/dsmti-2.2.10.tar'
    dsmti_file = urllib.request.urlretrieve(url_dsm,'dsmti-2.2.10.tar')
else:
    url_dsm ='https://www.eri.u-tokyo.ac.jp/people/takeuchi/software/dsmti-3.1.8.tar'
    dsmti_file = urllib.request.urlretrieve(url_dsm,'dsmti-3.1.8.tar')
#dsmti_file=wget.download(url_dsm)
work_dir='dsm_work'
# open file
file = tarfile.open(dsmti_file[0])
try:
    os.mkdir(work_dir)
except:
    print('skip mkdir')
# extracting file
file.extractall(work_dir)
file.close()
#os.remove(dsmti_file[0])

maxngrid_r=100000
maxlmax=25000
maxn_structure_zone = 12
max_nstation = 100
maxnfreq = 8192
os.chdir(work_dir+'/'+dsmti_file[0][:-4])
#os.chdir('./dsm_work/dsmti-3.1.8')
makefile='Makefile'
dsmtif='dsmti.f'
with fileinput.FileInput(makefile, 
                         inplace = True, backup ='.bak') as f:     
    for line in f:
        if "mpif77" in line and mpi==1:
            print(line.replace("mpif77",
                               "mpif77 -std=legacy"), end ='')
        
        elif "f77" in line and mpi!=1:
            print(line.replace("f77",
                               "gfortran -std=legacy"), end ='')
        else:
            print(line, end ='')
with fileinput.FileInput(dsmtif, 
                         inplace = True, backup ='.bak') as f:
      
    for line in f:
        if "parameter ( maxngrid_r" in line:
            print('	parameter ( maxngrid_r= '+str(maxngrid_r)+' )', end ='\n')
        elif "parameter ( maxlmax" in line:
            print('	parameter ( maxlmax= '+str(maxlmax)+' )', end ='\n')
        elif "parameter ( max_nstation" in line:
            print('	parameter ( max_nstation= '+str(max_nstation)+' )', end ='\n')
        elif "parameter ( maxn_structure_zone" in line:
            print('	parameter ( maxn_structure_zone= '+str(maxn_structure_zone)+' )', end ='\n')
        elif "parameter ( maxnfreq" in line:
            print('	parameter ( maxnfreq= '+str(maxnfreq)+' )', end ='\n')
        else:
            print(line, end ='')
os.system('make clean')
os.system('make')
