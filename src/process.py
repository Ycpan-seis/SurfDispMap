#python script of process.ipynb to be used in formatdata.sh
#read 1D Vs of each point from model
import numpy as np
#import matplotlib.pyplot as plt
import os
import sys

#model_in='USTClithoTB.txt'
model_out='ref_v.mdl'
#read data
#nx=31;ny=21;nz=12;depth=150;thick=1; 

with open('SurfMap.in','r') as f:
    lines = []
    for line in f:
        line = line.strip()
        # skip blank and comment
        if len(line)==0 or line.startswith('#'):
            continue
        lines.append(line)
model_in = lines[0]
nx,ny,nz = map(int,lines[1].split())
depth = float(lines[2])
thick = float(lines[3])

n=nx*ny
with open(model_in, 'r') as file:
    data = []
    for line in file:
        fields = line.split()
        if len(fields) == 4:
            data.append([float(fields[0]), float(fields[1]), float(fields[2]), float(fields[3])])
refdata=np.array(data)

#extract 1D Vs of each point from the model
nlayer=int(round(depth/thick))
Vs_h=np.zeros((nlayer+1, 10))
i=sys.argv[1]   #i means the i-th point,which is from .sh
i=int(i)

#modified 2024/4/12,the first row of the input model is thickness(not depth)
Vs_h[0,0]=refdata[i,0]
Vs_h[0,1]=refdata[i,1]
Vs_h[1:,8]=1.00
Vs_h[1:,9]=1.00
Vs_h[1:,0]=thick
for j in range(nz-1):
    z1 = refdata[j*n+i, 2]
    z2 = refdata[(j+1)*n+i, 2]
    vs1 = refdata[j*n+i, 3]
    vs2 = refdata[(j+1)*n+i, 3]
    sub = int(round((z2 - z1) / thick))
    start = int(round(z1 / thick))
    for k in range(sub):
        z = z1 + (k) * thick
        t = vs1 + (vs2 - vs1) * (z - z1) / (z2 - z1)
        Vs_h[start+k+1,2] = t
        Vs_h[start+k+1,1]=0.9409+2.0947*t-0.8206*t**2+0.2683*t**3-0.0251*t**4
        m=Vs_h[start+k+1,1]
        Vs_h[start+k+1,3]=1.6612*m-0.4721*m**2+0.0671*m**3-0.0043*m**4+0.000106*m**5
#    Vs_h[j+1,2]=refdata[j*n+i,3]
#    t=Vs_h[j+1,2]
#    Vs_h[j+1,1]=0.9409+2.0947*t-0.8206*t**2+0.2683*t**3-0.0251*t**4 #use Brocher function to compute Vp
#    m=Vs_h[j+1,1]
#    Vs_h[j+1,3]=1.6612*m-0.4721*m**2+0.0671*m**3-0.0043*m**4+0.000106*m**5
Vs_h[nlayer,0]=0

#write Vs_h for each point
with open(model_out, 'r') as file:
    lines = file.readlines()
with open(model_out, 'w') as file:
    file.writelines(lines[0:12])
    for row in Vs_h[1:]:
        row_str = " ".join(map(str, row))
        file.write(row_str + "\n")
