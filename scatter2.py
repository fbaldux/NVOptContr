import numpy as np
from matplotlib import pyplot as plt
from glob import glob

"""
# tritone
Ts = [ 56.,  80., 104., 128., 152., 176., 200., 224., 248., 272., 296., 320., 344., 368., 392.]
deltat = 0.16
tone = 3

def filename_func(L,T):
    return "Results/3tone_%dspins_%dus_K?.????.txt" % (L,T)

"""

Ts = [ 16.,  32.,  48.,  64.,  80.,  96., 112., 128., 144., 160., 240., 320.]
deltat = 0.16
tone = 1
harm = 5

def filename_func(L,T):
    return "Results/3tone_%dspins_%dus_K?.????.txt" % (L,T)

for T in Ts:  
    L = int(T/deltat)
     
    files = glob(filename_func(L,T))
    Ks = np.array([float(f[-10:-4]) for f in files])

    ordr = np.argsort(Ks)

    for k in range(len(files)):
    
        data = np.loadtxt(files[ordr[k]]).T
        #plt.plot(data[0], data[1], 'o', ms=2, label="K=%.1e"%Ks[ordr[k]])

        print(T, Ks[ordr[k]], np.argmax(data[1]), np.max(data[1]))

    """plt.xlabel("# of pulses")
    plt.ylabel(r"1/$\eta$")

    if tone==3:
        plt.title(r"$T=%d \mu$s, trichromatic signal" % T)
    elif tone==1:
        plt.title(r"$T=%d \mu$s, monochromatic signal" % T)

    plt.legend()
    plt.show()"""