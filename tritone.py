#  ---------------------------------------------------------------------------------------------  #
#
#   The program copies in Best/ the best configurations found for the 3-chromatic case.
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
from matplotlib import pyplot as plt
from glob import glob
from os import system

Ts_list = [ 56,    80,  104, 128,  152,  176,  200,  224,  248,  272,  296,  320,  344,  368,  392 ]
Ks_list = [1e-2, 5e-3, 1e-3, 5e-3, 5e-3, 5e-3, 5e-3, 5e-3, 5e-3, 2e-3, 2e-3, 2e-3, 2e-3, 2e-3, 2e-3]
deltat = 0.16
#tone = 3

intvec = np.vectorize(int)


def filename_in(L,T,K,r):
    return "Configurations/s_3tone_%dspins_%dus_K%.4f_r%d.txt" % (L,T,K,r)

def filename_out(L,T):
    return "Best/s_3tone_%dspins_%dus.txt" % (L,T)

Ts = intvec(np.loadtxt("best_tritone.txt")[:,0])
Ks = np.loadtxt("best_tritone.txt")[:,1]
best = np.loadtxt("best_tritone.txt")[:,2]
etas = np.loadtxt("best_tritone.txt")[:,3]

for i in range(len(Ts_list)):  
    L = int(Ts_list[i]/deltat)
    
    Ks_now = Ks[Ts==Ts_list[i]]
    best_now = best[Ts==Ts_list[i]]
    eta_now = etas[Ts==Ts_list[i]]
    
    r = int( best_now[np.where(Ks_now==Ks_list[i])[0][0]] )
    eta = eta_now[np.where(Ks_now==Ks_list[i])[0][0]]
    
    system("cp " + filename_in(L,Ts_list[i],Ks_list[i],r) + " " + filename_out(L,Ts_list[i]))
    
    #print("%f %f" % (Ts_list[i], eta))
