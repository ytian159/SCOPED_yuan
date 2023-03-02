import os 
#import wget
import urllib.request
import requests
import tarfile
import fileinput
from pysep import recsec
from pysep.recsec import plotw_rs
from obspy import read, Stream,read_events
from glob import glob
import pandas as pd
from pysep.utils.io import read_stations
from obspy.geodetics import  kilometer2degrees
import numpy as np
mpi=1
num_cores=8

stations_path='../../STATIONS_FILTERED'
cmt_path='../../CMTSOLUTION_20160124103029557'
stas =pd.read_fwf(stations_path,header=None,index=None)
#source=read_specfem3d_cmtsolution_cartesian(cmt_path)
stations=read_stations(stations_path)
source=read_events(cmt_path, format="CMTSOLUTION")[0]
src_moment=source.focal_mechanisms[0].moment_tensor
sorce_origin=source.preferred_origin()
nexp0=np.round(np.log10(src_moment.scalar_moment))

in_para_file='./data/010109.inf'
out_dir_dsm='data/'
time_series_length, n_freqnency=128,512
ngrid_r,lmin,lmax=18000,0,16000
with open(in_para_file, "r") as fl:
        lines = fl.readlines() 
for i,line in enumerate(lines):
        if i==4:
                lines[i]=f'  {time_series_length:5.1f}{n_freqnency:5}  time_series_length, n_freqnency \n'
        if 'ngrid_r  lmin   lmax' in line:
                lines[i+2]=f'   {ngrid_r:5} {lmin:5}  {lmax:5} \n'
        if 'nexp,source_mt' in line:
                source_para=f'{int(nexp0+7):5}  {src_moment.tensor.m_rr/10**nexp0:2.4f} {src_moment.tensor.m_tt/10**nexp0:2.4f} \
{src_moment.tensor.m_pp/10**nexp0:2.4f} {src_moment.tensor.m_rt/10**nexp0:2.4f} \
{src_moment.tensor.m_rp/10**nexp0:2.4f} {src_moment.tensor.m_tp/10**nexp0:2.4f}'+'    nexp,source_mt \n'
                lines[i]=source_para
        if 'source_depth,source_lat,sourth_lon' in line:
                origin=f'{sorce_origin.depth/1000} {sorce_origin.latitude:.2f} {sorce_origin.longitude:.2f}'+'  source_depth,source_lat,sourth_lon \n'
                lines[i]=origin
        if 'number of stations' in line:
                i_sta=i
                lines[i+1]=f'{len(stas):d} n_station \n'

del lines[i_sta+3:]

for i in range(len(stas)):
        lines.append(f'{stas.loc[i,2]:f} {stas.loc[i,3]:f} {stas.loc[i,0]} \n')
lines.append('c --- output files \n')
for i in range(len(stas)):
        lines.append(out_dir_dsm+'010109.'+stas.loc[i,0]+'\n')
lines.append('c\n')
lines.append('end\n')

os.rename(in_para_file,in_para_file+'.bak')
with open(in_para_file, 'w') as f:
    for line in lines:
        f.write(f"{line}")

if mpi==1:
    os.system(f'mpirun -np {num_cores} dsmti  <data/010109.inf')
else:
    ! ./dsmti  <data/010109.inf

data_path='./data'
cpnt='bhz'
def get_obspy_st(data_path,cpnt):
    fids=glob(os.path.join(data_path, "*."+cpnt))
    st = Stream()
    for fid in fids:
        st += read(fid)
    for i,tr in enumerate(st):
        otime=tr.stats.starttime
        dist_deg = kilometer2degrees(tr.stats.sac.dist) 
        tr.stats.network='XX'
        tr.stats.station=fids[i].split(sep='.')[-2]
        tr.stats.channel=cpnt.upper()
        tr.stats.sac = {
                "iztype": 9,  # Ref time equivalence, IB (9): Begin time
                "b": tr.stats.sac.b,  # begin time
                "e": tr.stats.npts * tr.stats.delta,  # end time
                "evla": tr.stats.sac.evla,
                "evlo": tr.stats.sac.evlo,
                "stla": tr.stats.sac.stla,
                "stlo": tr.stats.sac.stlo,
                "stel": 0,  # elevation in km
                "kevnm": str(tr.stats.starttime),  # only take date code
                "nzyear": otime.year,
                "nzjday": otime.julday,
                "nzhour": otime.hour,
                "nzmin": otime.minute,
                "nzsec": otime.second,
                "nzmsec": otime.microsecond,
                "dist": tr.stats.sac.dist,
                "az": tr.stats.sac.az,  # degrees
                "baz": tr.stats.sac.baz,  # degrees
                "gcarc": dist_deg,  # degrees
                "lpspol": 0,  # 1 if left-hand polarity (usually no in passive seis)
                "lcalda": 1,  # 1 if DIST, AZ, BAZ, GCARC to be calc'd from metadata
            }
    return st
st=get_obspy_st(data_path,cpnt)

plotw_rs(st=st,overwrite=True,scale_by='global_norm',
            sort_by='distance',preprocess='st',xlim_s=[0,time_series_length])