import numpy as np
from matplotlib import pyplot as plt
from glob import glob

# input
instring = input("").split(' ')

T = float( instring[0] )
deltat = float( instring[1] )  
tone = int( instring[2] ) 
harmonic = int( instring[3] ) 

L = int(T/deltat)

def filename_func():
    if tone==3:
        return "Results/3tone_%dspins_%dus_K?.????.txt" % (L,T)
    if tone==1:
        return "Results/1tone_%dharm_%dspins_%dus_K?.????.txt" % (harmonic,L,T)

files = glob(filename_func())
Ks = np.array([float(f[-10:-4]) for f in files])

ordr = np.argsort(Ks)

for k in range(len(files)):
    
    data = np.loadtxt(files[ordr[k]]).T
    plt.plot(data[0], data[1], 'o', ms=2, label="K=%.1e"%Ks[ordr[k]])

plt.xlabel("# of pulses")
plt.ylabel(r"1/$\eta$")

if tone==3:
    plt.title(r"$T=%.2f \mu$s, trichromatic signal" % T)
elif tone==1:
    plt.title(r"$T=%.2f \mu$s, monochromatic signal" % T)

plt.legend()
plt.show()