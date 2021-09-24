import numpy as np
from matplotlib import pyplot as plt

N = 625
T = N*160/1000
#Ks = np.array((0., 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1))
Ks = np.array((0., 0.0001, 0.0002, 0.0005, 0.001, 0.005))
#Ks = np.array((0., 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005))

tone = 1

for iK in range(len(Ks)):
    try:
        data = np.loadtxt("Results/%dtone_%dspins_%dus_K%.4f.txt" % (tone, N,T,Ks[iK])).T
        plt.plot(data[0], data[1], 'o', ms=2, label="K=%.4f"%Ks[iK])
        
    except:
        None
        

plt.xlabel("# of pulses")
plt.ylabel(r"1/$\eta$")

if tone==3:
    plt.title(r"$T=%d \mu$s, trichromatic signal" % T)
elif tone==1:
    plt.title(r"$T=%d \mu$s, monochromatic signal" % T)

plt.legend()
plt.show()