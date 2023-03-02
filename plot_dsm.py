import os 
import fileinput
from pysep import recsec
from pysep.recsec import plotw_rs
from obspy import read, Stream,read_events
from glob import glob
import pandas as pd
from pysep.utils.io import read_stations
from obspy.geodetics import  kilometer2degrees
import numpy as np

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
