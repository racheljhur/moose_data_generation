''' Determining truncation threshold using evds '''

'''
Based on Talreja 1981 and Rockette 1974, I chose the Gumbel Distribution (i.e., log-Weibull with kappa=0)
for the parameteric convergence study. MLE is valid for Gumbel distributions (Rockette). This is just to 
determine a minimum SVE ensemble size, so I can compute the responses for the remaining RVEs.
'''

import numpy as np
from scipy.stats import gumbel_r
import matplotlib.pyplot as plt
import pandas as pd
from helpers import *
from rich.progress import track
import json
import pickle

# Do this over the 15 classes only.
patterns=['F30','FA30', 'FAAA30', 'FC30', 'FCCC30', 'F40', 'FA40', 'FAAA40', 'FC40', 'FCCC40',
          'F50', 'FA50', 'FAAA50', 'FC50', 'FCCC50']
percentile=99 # This will correspond to 56 values / SVE
res=256
dat_dir=f'../../complete_workflow/combined_model/data/mp_fields'

# Use a dictionary to access values with patterns
x_dat = {}
for patt in patterns:
    x_dat[patt] = []
    for i in track(range(650)):
        
        path=dat_dir + f'/{patt}'
        filename = f'arr_{i}_maxprincipal_0001.csv'
        x = extract_mp_field(path, filename, res)
        
        # You need to ensure that you're sampling the top 1% from the fixed physical domain determined from the prior study
        x = resample_to_75(x)
        val = np.percentile(x, percentile, interpolation='nearest')
        x_top = x[x > val]
        x_dat[patt].append(x_top)

    x_dat[patt]=np.array(x_dat[patt])
    print(x_dat[patt].shape)
print(f'finished loading mp stresses at resolution {res}')

x_dat_scaled={}
# Scale the datasets
for patt in patterns:
    x_dat_scaled[patt]=scale(x_dat[patt])[0]
    mean=scale(x_dat[patt])[1]
    std=scale(x_dat[patt])[2]
    print(mean)
    print(std)
    np.save(f'rvs/{res}/dat_mean_{patt}.npy',mean)
    np.save(f'rvs/{res}/dat_std_{patt}.npy',std)
    print(f'saved mean and std of x_dat for {patt}')

# fit gumbel distribution (i.e., fit log weibull loc and scale, keeping kappa=0)
params={}
for patt in patterns:
    params[patt]=[]
    for i in track(drange(0,650,10)):
        if i==0:
            x=x_dat[patt][i].flatten()
        else:
            x=x_dat[patt][:i].flatten()

        p = gumbel_r.fit(x)
        params[patt].append((i,*p))
            
        if i==649:
            num_dat=int(percentile*650*256*256)
            print(f'final shape of dataset used for mle (should be ({num_dat},)):',x_top.shape)

# write results
print('saving params and rvs...')

path = f'params/{res}'
if not os.path.exists(path):
    os.makedirs(path)
path = f'rvs/{res}'
if not os.path.exists(path):
    os.makedirs(path)

with open(f'params/{res}/params.pkl', 'wb') as f:
    pickle.dump(params, f)

with open(f'rvs/{res}/rvs_scaled.pkl', 'wb') as f:
    pickle.dump(x_dat_scaled, f)

with open(f'rvs/{res}/rvs.pkl', 'wb') as f:
    pickle.dump(x_dat, f)

print(f'Done for resolution {res}')
