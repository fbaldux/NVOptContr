#  ---------------------------------------------------------------------------------------------  #
#
#   Given the final time and tone, the program plots the sensitivities for all the
#   values of K found in Results/
#
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
from matplotlib import pyplot as plt
from glob import glob

T = float( sys.argv[1] )
deltat = float( sys.argv[2] )
tone = int( sys.argv[3] )
harmonic = int( sys.argv[4] )

L = int(T/deltat)

def filename_func():
    return "Results/T%.4f_dt%.4f_t%d_h%d_K?.????.txt" % (T, deltat, tone, harmonic)

files = glob(filename_func())
Ks = np.array([float(f[-10:-4]) for f in files])

ordr = np.argsort(Ks)

for k in range(len(files)):
    
    data = np.loadtxt(files[ordr[k]]).T
    plt.plot(data[0], data[1], 'o', ms=2, label="K=%.1e"%Ks[ordr[k]])

plt.xlabel("# of pulses")
plt.ylabel(r"1/$\eta$")

plt.title(r"$T=%.2f \mu$s, monochromatic signal" % T)

plt.legend()
plt.show()