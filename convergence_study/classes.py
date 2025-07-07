''' dependencies to run convergence study '''
import os
import numpy as np
from scipy.stats import genextreme
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler

def extract_mp_field(path, filename):
    # mapping stress values based on (x,y) coords
    nx=256
    ny=256
    full_file = os.path.join(path, filename)
    df = pd.read_csv(full_file, usecols=[1, 2, 3])

    df_sorted = df.sort_values(by=['y','x'])
    field = df_sorted[f'maxprincipal'].values.reshape((nx,ny))
    field = np.array(field) # (nx,ny) array containing mp stresses

    return field


def mle(x_dat, percentile):
    val = np.percentile(x_dat, percentile, interpolation='lower')
    x = x_dat[x_dat>=val]
    params = genextreme.fit(x_dat)
    return params

def scale(x):
    inp_scaler = StandardScaler()
    x_scaled = inp_scaler.fit_transform(x)
    data_mean = inp_scaler.mean_
    data_std = inp_scaler.scale_
    
    return x_scaled, data_mean, data_std

def unscale(x, data_mean, data_std):
    x_unscaled=(x * data_std) + data_mean
    return x_unscaled

def drange(start, stop, step):
    while start < stop:
            yield start
            start += step
