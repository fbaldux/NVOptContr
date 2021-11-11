#  ---------------------------------------------------------------------------------------------  #
#
#   Some trials for the unstable data.
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
from matplotlib import pyplot as plt
import numba as nb

gyro = 28025

bella = np.loadtxt("Best/s_3tone_955spins_152us.txt")
brutta = np.loadtxt("Best/s_3tone_950spins_152us.txt")

#brutta = np.append(brutta, np.ones(5), axis=0)

#print(np.sum((bella-brutta)**2))

T = 152
deltat = 0.16
tone = 3

L = int(T/deltat)

Js = np.loadtxt("Init/J_%dspins_%dus.txt" % (L, T)).reshape(L,L)
hs = np.loadtxt("Init/h_3tone_%dspins_%dus.txt" % (L, T))
K = 0.005

Js += 0.01 * np.random.uniform(-1,1,size=(L,L))*Js
Js += Js.T

@nb.jit
def H(s):
    Eh = 0.
    EJ = 0.
    EK = 0.
    
    for i in range(L):
        Eh += hs[i]*s[i]
        
        for j in range(i):
            EJ += 2.*Js[i,j]*s[i]*s[j]
        
        EJ += Js[i,i]
    
    
    for i in range(1,L):
        EK += K*s[i-1]*s[i]


    return EJ - np.log(np.abs(Eh)) #- EK

def etaInv(epsilon):
    return 1./np.exp(epsilon - np.log(gyro)-0.5*np.log(L*0.16*1e-6))


def filename_all():
    if tone==3:
        return "Results/3tone_%dspins_%dus_K0.0050.txt" % (L,T)


dists = np.zeros(101)
etas = np.zeros(101)
etas[0] = 96.0145

data = np.loadtxt(filename_all()).T
etas[1:] = data[1]

etas_new = np.zeros(101)
etas_new[0] = etaInv(H(brutta))

#print("originale", etaInv(H(brutta)), etas[0])

for r in range(100):
    
    filename = "Configurations/s_3tone_%dspins_%dus_K0.0050_r%d.txt" % (L,T,r)
    conf = np.loadtxt(filename)
    
    #print(r, etaInv(H(conf)), etas[r+1])
    etas_new[r+1] = etaInv(H(conf))
    #dists[r+1] = 0.25 * np.sum((conf-brutta)**2) / L
    
    
plt.plot(etas[0], etas_new[0], '.')
plt.plot(etas[1:], etas_new[1:], '.')

"""
plt.plot(etas[0], dists[0], '.')
plt.plot(etas[1:], np.minimum(dists[1:], 1-dists[1:]), '.')

plt.ylabel("Hamming distance")
plt.xlabel(r"1/$\eta$")

"""

plt.xlabel("eta old")
plt.ylabel("eta new")

plt.legend()
plt.show()