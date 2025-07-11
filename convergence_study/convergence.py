''' determining truncation threshold using evds '''
import numpy as np
from scipy.stats import genextreme
import matplotlib.pyplot as plt
import pandas as pd
from classes import *
from rich.progress import track

# do this over the 15 classes only.
patt='FCCC50'
percentile=99.99 # 99.9 is 67 per sve, 99.99 is 8 per sve, 99.999 is 2 per sve
path=f'../../complete_workflow/combined_model/data/mp_fields/{patt}'

x_dat=np.zeros((650,8))
for i in range(650):
    filename = f'arr_{i}_maxprincipal_0001.csv'
    x = extract_mp_field(path, filename)
    val = np.percentile(x, percentile, interpolation='lower')
    x_top = x[x >= val]
    x_dat[i]=x_top

print(x_dat.shape)

x_dat=scale(x_dat)[0] # you need to scale using the entire dataset
mean=scale(x_dat)[1]
std=scale(x_dat)[2]

params=[]
for i in track(drange(0,650,10)):
    if i==0:
        x=x_dat[i].flatten()
    else:
        x=x_dat[:i].flatten()

    p = genextreme.fit(x)
    params.append((i,*p))
        
    if i==649:
        num_dat=int(percentile*650*256*256)
        print(f'final shape of dataset used for mle (should be ({num_dat},)):',x_top.shape)

params=np.array(params)
val = np.percentile(x_dat, percentile, interpolation='lower')
# rvs = x_dat[x_dat>=val]
rvs=x_dat

path = f'rvs/{patt}'
if not os.path.exists(path):
    os.makedirs(path)

np.save(f'rvs/{patt}/rvs_{patt}_{percentile}.npy',rvs)
print('checking the shape of rvs...')
print('rvs shape:', rvs.shape)

print('checking parameter array shape and vals...')
print(params.shape)
print(params[:,0])

path = f'params/{percentile}'
if not os.path.exists(path):
    os.makedirs(path)

np.save(f'params/{percentile}/params_{patt}.npy', params)

print(f'...finished saving the {patt} class')
