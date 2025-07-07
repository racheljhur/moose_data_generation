''' determining truncation threshold using evds '''
import numpy as np
from scipy.stats import genextreme
import matplotlib.pyplot as plt
import pandas as pd
from classes import *
from rich.progress import track

path='/home/user/inverse_design/moose/convergence_study/mp_str_fields/FCCC50'
patt='FCCC50'
percentile=99.99

x_dat=np.zeros((650,256,256))
for i in range(650):
    filename = f'arr_{i}_maxprincipal_0001.csv'
    x = extract_mp_field(path, filename)
    x=scale(x)[0]
    x_dat[i]=x

params=[]
for i in track(drange(0,650,10)):
    if i==0:
        x=x_dat[i].flatten()
    else:
        x=x_dat[:i].flatten()

    val = np.percentile(x, percentile, interpolation='lower')
    x_top = x[x >= val]

    p = genextreme.fit(x_top)
    params.append((i, *p))
        
    if i==649:
        num_dat=int(percentile*650*256*256)
        print(f'final shape of dataset used for mle (should be ({num_dat},)):',x_top.shape)

params=np.array(params)
val = np.percentile(x_dat, percentile, interpolation='lower')
rvs = x_dat[x_dat>=val]

np.save(f'rvs/F30/rvs_{patt}_{percentile}.npy',rvs)
print('rvs shape:', rvs.shape)

print('checking parameter array shape and vals')
print(params.shape)
print(params[:,0])

print('saving...')
np.save(f'params/{percentile}/params_{patt}.npy', params)
