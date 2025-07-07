'''evaluating statistics of fitted params'''
import numpy as np
from scipy.stats import genextreme
import matplotlib.pyplot as plt
import pandas as pd
from classes import *
from rich.progress import track

patt='F30'
percentile=99.99
num_sve=40

params=np.load(f'params/{percentile}/params_{patt}.npy')
rvs=np.load(f'rvs/{patt}/rvs_{patt}_{percentile}.npy')

print(params.shape)
print(rvs.shape)

m_stats=[]
mu_stats=[]
rel_d=[]
for i in range(65):
    # for mean
    mean=np.mean(params[:i,1])
    std=np.std(params[:i,1])
    mu_stats.append(mean)
    m_stats.append(std)
    
    # note: change rel_dif depending on what statistic you're assessing (mean or variance of parameter)
    rel_dif=np.abs(mu_stats[i-1]-mu_stats[i])
    rel_d.append(rel_dif)
    
    
m_stats=np.array(m_stats)
mu_stats=np.array(mu_stats)
rel_d=np.array(rel_d)
print(r'$relative difference for \mu mean:$',rel_d[num_sve]) 

# plot parameter progression
n_sves=np.linspace(0,650,65)
plt.figure()
plt.errorbar(n_sves,params[:,1],yerr=m_stats, linewidth=2, alpha=0.35, color='blue')
plt.plot(n_sves,params[:,1], linewidth=1, alpha=1)
plt.title(f'Convergence Study at the {percentile}th Percentile \n for {patt} RVE')
plt.grid()
plt.xlabel('Num SVEs')
plt.ylabel(r'$\mu$')
plt.savefig(f'convergence_plots/{patt}/{percentile}/mean.png')

mu_stats=[]
sc_stats=[]
rel_d=[]
for i in range(65):
    # for scale
    mean=np.mean(params[:i,2])
    std=np.std(params[:i,2])
    mu_stats.append(mean)
    sc_stats.append(std)
    

    rel_dif=np.abs(mu_stats[i-1]-mu_stats[i])
    rel_d.append(rel_dif)
    
mu_stats=np.array(mu_stats)
sc_stats=np.array(sc_stats)
rel_d=np.array(rel_d)
print(r'$relative difference for \sigma mean:$',rel_d[num_sve]) 
    

# plot parameter progression
n_sves=np.linspace(0,650,65)
plt.figure()
plt.errorbar(n_sves,params[:,2],yerr=sc_stats, linewidth=2, alpha=0.35, color='blue')
plt.plot(n_sves,params[:,2], linewidth=1, alpha=1)
plt.title(f'Convergence Study at the {percentile}th Percentile \n for {patt} RVE')
plt.xlabel('Num SVEs')
plt.grid()
plt.ylabel(r'$\sigma$')
plt.savefig(f'convergence_plots/{patt}/{percentile}/scale.png')

mu_stats=[]
k_stats=[]
rel_d=[]
for i in range(65):
    # for shape
    mean=np.mean(params[:i,3])
    std=np.std(params[:i,3])
    k_stats.append(std)
    mu_stats.append(mean)
    
    rel_dif=np.abs(mu_stats[i-1]-mu_stats[i])
    rel_d.append(rel_dif)
    
mu_stats=np.array(mu_stats)
k_stats=np.array(k_stats)
rel_d=np.array(rel_d)
print(r'$relative difference for \kappa mean:$',rel_d[num_sve]) 


# plot parameter progression
n_sves=np.linspace(0,650,65)
plt.figure()
plt.errorbar(n_sves,params[:,3],yerr=k_stats, linewidth=2, alpha=0.35, color='blue')
plt.plot(n_sves,params[:,3], linewidth=1, alpha=1)
plt.title(f'Convergence Study at the {percentile}th Percentile \n for {patt} RVE')
plt.xlabel('Num SVEs')
plt.grid()
plt.ylabel(r'$\kappa$')
plt.savefig(f'convergence_plots/{patt}/{percentile}/shape.png')


plt.figure()
x_lin=np.linspace(rvs.min(), rvs.max(), rvs.shape[0])
plt.hist(rvs, density=True, bins=30, alpha=0.7, edgecolor='black', label='data')
# use j*10 th set of parameters in the order of shape, loc, scale
j = 30
plt.plot(x_lin,genextreme.pdf(x_lin,params[j,1],loc=params[j,2],scale=params[j,3]),'r-', lw=3, label=f'genextreme pdf')
plt.legend()
plt.xlabel(f'Normalized MP Stress for {patt} RVE')
plt.ylabel('Density')
plt.title(f'Fitted GEVD for {patt} at {percentile} percentile')
plt.savefig(f'convergence_plots/{patt}/{percentile}/hist.png')

print('done')
