#convert the dispersion data to the form matlab can read
import numpy as np
import math
import os
from scipy.io import savemat

# ===== read SurfMap.in =====

with open('SurfMap.in','r') as f:
    lines = []
    for line in f:
        line = line.strip()
        if len(line)==0 or line.startswith('#'):
            continue
        lines.append(line)
# model parameter
nx,ny,nz = map(int,lines[1].split())
# surfdisp parameter
ifunc,mode,nt = map(int,lines[4].split())
dT = float(lines[5])
# mat parameter
Tstart = float(lines[7])
xstart,ystart = map(float,lines[8].split())
dx,dy = map(float,lines[9].split())
ref = float(lines[10])

#phase v
with open('disp_all_phase.txt', 'r') as file:
    data = []
    for line in file:
        fields = line.split()
        if len(fields) == 2:
            data.append([float(fields[0]), float(fields[1])])
phasedata=np.array(data)
#nx=31;ny=21;nt=46
n=nx*ny
disp3D_phase=np.zeros((ny,nx,nt))
for i in range(nx):
    for j in range(ny):
        for k in range(nt):
            disp3D_phase[j,i,k]=phasedata[j*nx*nt+i*nt+k,1]
            
#group v
with open('disp_all_group.txt', 'r') as file:
    data = []
    for line in file:
        fields = line.split()
        if len(fields) == 2:
            data.append([float(fields[0]), float(fields[1])])
groupdata=np.array(data)

disp3D_group=np.zeros((ny,nx,nt))
for i in range(nx):
    for j in range(ny):
        for k in range(nt):
            disp3D_group[j,i,k]=groupdata[j*nx*nt+i*nt+k,1]
            
#period
disperT=np.zeros((ny,nx,nt))
for i in range(nx):
    for j in range(ny):
        for k in range(nt):
            disperT[j,i,k]=Tstart+dT*k
#latitude         
lat_m=np.zeros((ny,nx,nt))
for i in range(nx):
    for j in range(ny):
        for k in range(nt):
            lat_m[j,i,k]=ystart+dy*j
#longitude
long_m=np.zeros((ny,nx,nt))
for i in range(nx):
    for j in range(ny):
        for k in range(nt):
            long_m[j,i,k]=xstart+dx*i
#error range
ref_range=np.zeros((nt,2))
for j in range(nt):
    ref_range[j,0]=Tstart+dT*j
    ref_range[j,1]=ref

savemat('./OUTPUT/SurfDisp.mat', {'disperT_m': disperT,'lat_m': lat_m,'lon_m': long_m,'ref_range': ref_range,'disp3D_phase': disp3D_phase,'disp3D_group': disp3D_group})
