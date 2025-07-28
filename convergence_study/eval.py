''' Plotting Functions for Evaluating Fitted Gumbel Parameters'''
import os
import numpy as np
from scipy.stats import gumbel_r
import matplotlib.pyplot as plt
import pandas as pd
from helpers import *
from rich.progress import track
import json
import pickle

# Global Variables
patterns=['F30','FA30', 'FAAA30', 'FC30', 'FCCC30', 'F40', 'FA40', 'FAAA40', 'FC40', 'FCCC40',
          'F50', 'FA50', 'FAAA50', 'FC50', 'FCCC50']
res=256
percentile=99

path=f'convergence_plots/{res}/{percentile}'
if not os.path.exists(path):
    os.makedirs(path)

# load in dictionaries, where entries are accessible via pattern name
with open(f'params/{res}/params.pkl', 'rb') as f:
    params = pickle.load(f)
with open(f'rvs/{res}/rvs.pkl', 'rb') as f:
    rvs = pickle.load(f)

# grab the statistics of the location parameter (mean and std)
mu_std={}
mu_mean={}
# loc parameter is stored in column 2, i.e., params[n,1]
for patt in patterns:
    mu_mean[patt]=[]
    mu_std[patt]=[]
    for i in drange(0,65,15): 
        params[patt]=np.array(params[patt])
        mean = np.mean(params[patt][:i, 1])
        std = np.std(params[patt][:i, 1])
        mu_mean[patt].append(mean)
        mu_std[patt].append(std)
    
    mu_mean[patt]=np.array(mu_mean[patt])
    mu_std[patt]=np.array(mu_std[patt])

# plot parameter progression for the location parameter 
n_sves=np.linspace(0,650,65)
for patt in patterns:
    # access the (5,) shaped mu_std array for each pattern
    # access the (65,) shaped location parameter in patt[:,1] for each pattern
    plt.figure()
    # plt.errorbar(n_sves,params[patt][:,1],yerr=mu_std[patt], linewidth=2, alpha=0.35, color='blue')
    plt.plot(n_sves,params[patt][:,1], linewidth=2, alpha=1)
    plt.title(f'Convergence Study at the {percentile}th Percentile \n for {patt} RVE')
    plt.grid()
    plt.xlabel('Num SVEs')
    plt.ylabel(r'$\mu$')
    plt.savefig(f'convergence_plots/{res}/{percentile}/loc_{patt}.png')


# grab the statistics of the location parameter (mean and std)
sc_mean={}
sc_std={}
for patt in patterns:
    sc_mean[patt]=[]
    sc_std[patt]=[]
    for i in drange(0,65,15):
        params[patt]=np.array(params[patt])   
        # compute the mean and std at increments of 150       
        mean=np.mean(params[patt][:i,2])
        std=np.std(params[patt][:i,2])
        sc_mean[patt].append(mean)
        sc_std[patt].append(std)
    
    sc_mean[patt]=np.array(sc_mean[patt])
    sc_std[patt]=np.array(sc_std[patt])
    
# plot parameter progression for the scale parameter
for patt in patterns:
    # access the (5,) shaped mu_std array for each pattern
    # access the (65,) shaped scale parameter in patt[:,1] for each pattern
    plt.figure()
    # plt.errorbar(n_sves,params[patt][:,2],yerr=sc_std[patt], linewidth=2, alpha=0.35, color='blue')
    plt.plot(n_sves,params[patt][:,2], linewidth=2, alpha=1)
    plt.title(f'Convergence Study at the {percentile}th Percentile \n for {patt} RVE')
    plt.grid()
    plt.xlabel('Num SVEs')
    plt.ylabel(r'$\sigma$')
    plt.savefig(f'convergence_plots/{res}/{percentile}/scale_{patt}.png')

# plotting the fitted Gumbel distribution
for patt in patterns:
    # use unnormalized variables
    x_dat=rvs[patt]
    # use j*10 th set of parameters (likely has converged)
    j=64

    plt.figure()
    x_lin=np.linspace(x_dat.min(), x_dat.max(), x_dat.shape[0])
    plt.hist(x_dat.flatten(), density=True, bins=30, alpha=0.7, edgecolor='black', label='data')
    plt.plot(x_lin,gumbel_r.pdf(x_lin,loc=params[patt][j,1],scale=params[patt][j,2]),'r-', lw=3, label=f'Gumbel pdf')
    plt.legend()
    plt.xlabel(f'MP Stress for {patt} RVE')
    plt.ylabel('Density')
    plt.title(f'Gumbel Distribution for {patt} at {percentile} percentile')
    plt.savefig(f'convergence_plots/{res}/{percentile}/hist_{patt}_unnormalized.png')


# check the relative change from 450 to 650
for patt in patterns:
    # print(f'location statistics for {patt} (percent change)')
    # rel_diff_mean=np.abs(mu_mean[patt][2]-mu_mean[patt][4]) / mu_mean[patt][2]
    # rel_diff_std=np.abs(mu_std[patt][2]-mu_std[patt][4]) / mu_std[patt][2]

    # print(f"{rel_diff_mean:.2e}")
    # print(f"{rel_diff_std:.2e}")

    print(f'scale statistics for {patt} (percent change)')
    # rel_diff_mean=np.abs(sc_mean[patt][2]-sc_mean[patt][4]) / sc_mean[patt][2]
    rel_diff_std=np.abs(sc_std[patt][2]-sc_std[patt][4]) / sc_std[patt][2]

    # print(f"{rel_diff_mean:.2e}")
    print(f"{rel_diff_std:.2e}")

print(f'finished evaluating all classes at resolution {res}')
