#  ---------------------------------------------------------------------------------------------  #
#
#   Some trials for the unstable data.
#
#  ---------------------------------------------------------------------------------------------  #


import numpy as np
from matplotlib import pyplot as plt


bella = np.loadtxt("Best/s_3tone_955spins_152us.txt")
brutta = np.loadtxt("Best/s_3tone_950spins_152us.txt")

#brutta = np.append(brutta, np.ones(5), axis=0)

#print(np.sum((bella-brutta)**2))


T = 152
deltat = 0.16
tone = 3

L = int(T/deltat)

def filename_all():
    if tone==3:
        return "Results/3tone_%dspins_%dus_K0.0050.txt" % (L,T)

dists = np.zeros(101)
etas = np.zeros(101)
etas[0] = 96.0145

filename = "Configurations/s_3tone_%dspins_%dus_K0.0050_r%d.txt" % (L,T,0)
conf0 = np.loadtxt(filename)

for r in range(100):
    
    filename = "Configurations/s_3tone_%dspins_%dus_K0.0050_r%d.txt" % (L,T,r)
    conf = np.loadtxt(filename)
    
    dists[r+1] = 0.25 * np.sum((conf-brutta)**2) / L
    #dists[r+1] = 0.25 * np.sum((conf-conf0)**2) / L
    
    
data = np.loadtxt(filename_all()).T

pipulse = data[0]

#dists[0] = 0.25 * np.sum((conf0-brutta)**2) / L
etas[1:] = data[1]


print(np.argsort(-etas)-1)



plt.plot(etas[0], np.minimum(dists[0],1-dists[0]), '.')
plt.plot(etas[1:], np.minimum(dists[1:], 1-dists[1:]), '.')

#plt.plot(etas[0], 48, '.')
#plt.plot(etas[1:], pipulse, '.')

plt.xlabel(r"1/$\eta$")
plt.ylabel("Hamming distance")
#plt.ylabel("pi pulses")



#plt.legend()
plt.show()