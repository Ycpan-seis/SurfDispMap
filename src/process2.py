#because some model is bad(low velocity layer?),the forward code can't compute all the phase velocity,
#so we need do some other operations to format data
import numpy as np
import math
import os

#nT=46; dT= 1
# ===== read SurfMap.in =====
with open('SurfMap.in','r') as f:
    lines = []
    for line in f:
        line = line.strip()
        if len(line)==0 or line.startswith('#'):
            continue
        lines.append(line)
# surfdisp parameter line
ifunc,mode,nT = map(int,lines[4].split())

igr = int(open('igr.tmp').read().strip())
if igr == 0:
    outfile = './OUTPUT/disp_all_phase.txt'
else:
    outfile = './OUTPUT/disp_all_group.txt'
    
dT = float(lines[5])

with open('disp.txt', 'r') as file:
    data = []
    for line in file:
        fields = line.split()
        if len(fields) == 2:
            data.append([float(fields[0]), float(fields[1])])
npdata=np.array(data)

l=len(npdata)

if l<nT:
    for i in range(nT-l):
        add=np.zeros((1, 2))
        add[0,0]=npdata[l-1+i,0]+dT
        add[0,1]=npdata[l-1+i,1]+ np.random.uniform(-0.001, 0.005)
        npdata=np.vstack([npdata, add])
with open(outfile, 'w') as file:
    np.savetxt(file,npdata)
