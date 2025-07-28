''' Mesh sensitivity study at the scale of an sve '''
''' Notes:
    Here, I will be studying six microstructure classes,
    covering the extreme volume fraction and spatial statistics
    within the classes considered here.
    
    Based on Craig's 2010 study, I will base the cutoff
    on a <5% deviation in the extreme MP stress. We generally
    want coarsest resolution possible.

    I believe the ratio of smallest feature size / domain size should be <= 1/3.

    Importantly, when you change the mesh resolution, the physical length you are representing changes.
    I.e., 75 pixels=112um, so 25 pixels=37um. Hence, the physical domain size is changing. As a result,
    you need to revert back to the baseline physical domain size (i.e., 112x112 um^2 = 75x75 pixel^2).
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from classes import *
import os

out_path='mesh_sensitivity_results'

if not os.path.exists(out_path):
    os.makedirs(out_path)

# load in classes of interest
patts=['F30', 'FAAA30', 'FCCC30', 'FAAA50', 'FCCC50']
resolutions=['25','50','75','100','125','150','175','200','225','256']
percentile=99

avg_mp_stress=[]
for p in patts:
    for res in resolutions:
        path=f'mesh_sensitivity_stresses/{p}'
        filename = f'arr_{res}_maxprincipal_0001.csv'
        x = extract_mp_field(path, filename,int(res))
        val = np.percentile(x, percentile, interpolation='lower')
        x_top = x[x >= val]
        x_mean = np.mean(x_top)
        avg_mp_stress.append(x_mean)
avg_mp_stress=np.array(avg_mp_stress)
print(avg_mp_stress.shape)

x=np.linspace(25,256,10)
plt.figure()
plt.plot(x,avg_mp_stress[:10],marker='o', linestyle='-', color='b', label='F30')
plt.plot(x,avg_mp_stress[10:20],marker='o', linestyle='-', color='g', label='FAAA30')
plt.plot(x,avg_mp_stress[20:30],marker='o', linestyle='-',color='r',label='FCCC30')
plt.plot(x,avg_mp_stress[30:40],marker='o', linestyle='-',color='c',label='FAAA50')
plt.plot(x,avg_mp_stress[40:50],marker='o', linestyle='-',color='m',label='FCCC50')
plt.legend()
plt.grid()
plt.title('Mesh Sensitivity Study')
plt.xlabel('Num Mesh Elements Along Edge')
plt.ylabel(r'$\mathbb{E}[\sigma_{top1\%}]$')
plt.savefig('mesh_sensitivity_results/mesh_sensitivity.png')

f30_avg_mp_stresses=avg_mp_stress[:10]
faaa30_avg_mp_stresses=avg_mp_stress[10:20]
fccc30_avg_mp_stresses=avg_mp_stress[20:30]
faaa50_avg_mp_stresses=avg_mp_stress[30:40]
fccc50_avg_mp_stresses=avg_mp_stress[40:50]

print('For FAAA50...')
for i in range(9):
    dat=faaa50_avg_mp_stresses
    diff=np.abs(dat[i]-dat[i+1])
    # print('difference:', diff)
    percent_change=(diff/dat[i]) * 100
    if i==8:
        print(percent_change)

# look at the mp stress field for FAAA50 at resolution 100 and at 225.
res='256'
patt='FAAA50'
path=f'mesh_sensitivity_stresses/{patt}'
filename =f'arr_{res}_maxprincipal_0001.csv'
field=extract_mp_field(path, filename,int(res))
val=np.percentile(field, percentile, interpolation='lower')
# use masking to remove everything below the threshold
field=np.ma.masked_where((val > field),field)
cmap = plt.cm.viridis.copy()
cmap.set_bad(color='gray') 
plt.figure()
plt.imshow(field, cmap=cmap)
plt.colorbar(label='MP Stress (Pa)', orientation='horizontal',fraction=0.046, pad=0.07)
plt.title(f'Top 1% MP Stress Field for {patt} at resolution {res}')
plt.savefig(f'mesh_sensitivity_results/{patt}_{res}_field_1%.png')
