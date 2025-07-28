import os
import numpy as np
from scipy.stats import genextreme
import matplotlib.pyplot as plt
import pandas as pd
from Helpers import *
from rich.progress import track

patt='FCCC50'
percentile=99.99
num_sve=64 # x10

path=f'convergence_plots/{patt}/{percentile}'
if not os.path.exists(path):
    os.makedirs(path)

params=np.load(f'params/{percentile}/params_{patt}.npy')
rvs=np.load(f'rvs/{patt}/rvs_{patt}_{percentile}.npy')

print(params.shape)
print(rvs.shape)

mu_std=[]
mu_mean=[]
rel_d=[]
for i in range(65):
    # for mean
    mean=np.mean(params[:i,1])
    std=np.std(params[:i,1])
    mu_mean.append(mean)
    mu_std.append(std)
    
    rel_dif=np.abs(mu_std[i-1]-mu_std[i])
    rel_dif_mean=np.abs(mu_mean[i-1]-mu_mean[i])
    rel_d.append(rel_dif)

    if i==64:
        print('absolute difference in std (across the past 100 sves):', np.abs(mu_std[64]-mu_std[54]))
        print('absolute difference in mean: (across the past 100 sves)', np.abs(mu_mean[64]-mu_mean[54]))
    
    
mu_mean=np.array(mu_mean)
mu_std=np.array(mu_std)
rel_d=np.array(rel_d)
print(r'$relative difference for \mu std:$',rel_d[num_sve]) 

# plot parameter progression
n_sves=np.linspace(0,650,65)
plt.figure()
plt.errorbar(n_sves,params[:,1],yerr=mu_std, linewidth=2, alpha=0.35, color='blue')
plt.plot(n_sves,params[:,1], linewidth=1, alpha=1)
plt.title(f'Convergence Study at the {percentile}th Percentile \n for {patt} RVE')
plt.grid()
plt.xlabel('Num SVEs')
plt.ylabel(r'$\mu$')
plt.savefig(f'convergence_plots/{patt}/{percentile}/mean.png')

sc_mean=[]
sc_std=[]
rel_d=[]
for i in range(65):
    # for scale
    mean=np.mean(params[:i,2])
    std=np.std(params[:i,2])
    sc_mean.append(mean)
    sc_std.append(std)
    

    rel_dif=np.abs(sc_std[i-1]-sc_std[i])
    rel_d.append(rel_dif)

    if i==64:
        print('absolute difference in std (across the past 100 sves):', np.abs(sc_std[64]-sc_std[54]))
        print('absolute difference in mean: (across the past 100 sves)', np.abs(sc_mean[64]-sc_mean[54]))

    
sc_mean=np.array(sc_mean)
sc_std=np.array(sc_std)
rel_d=np.array(rel_d)
print(r'$relative difference for \sigma std:$',rel_d[num_sve]) 
    

# plot parameter progression
n_sves=np.linspace(0,650,65)
plt.figure()
plt.errorbar(n_sves,params[:,2],yerr=sc_std, linewidth=2, alpha=0.35, color='blue')
plt.plot(n_sves,params[:,2], linewidth=1, alpha=1)
plt.title(f'Convergence Study at the {percentile}th Percentile \n for {patt} RVE')
plt.xlabel('Num SVEs')
plt.grid()
plt.ylabel(r'$\sigma$')
plt.savefig(f'convergence_plots/{patt}/{percentile}/scale.png')

k_mean=[]
k_std=[]
rel_d=[]
for i in range(65):
    # for shape
    mean=np.mean(params[:i,3])
    std=np.std(params[:i,3])
    k_mean.append(mean)
    k_std.append(std)
    

    rel_dif=np.abs(sc_std[i-1]-sc_std[i])
    rel_d.append(rel_dif)

    if i==64:
        print('absolute difference in std (across the past 100 sves):', np.abs(k_std[64]-k_std[54]))
        print('absolute difference in mean: (across the past 100 sves)', np.abs(k_mean[64]-k_mean[54]))
    
k_mean=np.array(k_mean)
k_std=np.array(k_std)
rel_d=np.array(rel_d)
print(r'$relative difference for \kappa std:$',rel_d[num_sve]) 

# plot parameter progression
n_sves=np.linspace(0,650,65)
plt.figure()
plt.errorbar(n_sves,params[:,3],yerr=k_std, linewidth=2, alpha=0.35, color='blue')
plt.plot(n_sves,params[:,3], linewidth=1, alpha=1)
plt.title(f'Convergence Study at the {percentile}th Percentile \n for {patt} RVE')
plt.xlabel('Num SVEs')
plt.grid()
plt.ylabel(r'$\kappa$')
plt.savefig(f'convergence_plots/{patt}/{percentile}/shape.png')


plt.figure()
x_lin=np.linspace(rvs.min(), rvs.max(), rvs.shape[0])
plt.hist(rvs.flatten(), density=True, bins=30, alpha=0.7, edgecolor='black', label='data')
# use j*10 th set of parameters in the order of shape, loc, scale
j = 64
plt.plot(x_lin,genextreme.pdf(x_lin,params[j,1],loc=params[j,2],scale=params[j,3]),'r-', lw=3, label=f'genextreme pdf')
plt.legend()
plt.xlabel(f'Normalized MP Stress for {patt} RVE')
plt.ylabel('Density')
plt.title(f'Fitted GEVD for {patt} at {percentile} percentile')
plt.savefig(f'convergence_plots/{patt}/{percentile}/hist.png')

print(f'done evaluating the {patt} class')
