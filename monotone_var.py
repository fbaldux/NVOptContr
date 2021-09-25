import numpy as np
from matplotlib import pyplot as plt
from glob import glob
from os import system

Ts_list = [20.8, 40.48, 100,  101.76, 219.84, 266.08, 323.84, 340.16, 392]
Ks_list = [1e-2, 1e-2,  1e-2, 1e-3,   1e-3,   5e-3,   5e-3,   5e-3,   5e-3]
deltat = 0.16
harmonics = [1,2,5,5,9,11,17,24,34]

intvec = np.vectorize(int)


def filename_in(harm,L,T,K,r):
    return "Configurations/s_1tone_%dharm_%dspins_%dus_K%.4f_r%d.txt" % (harm,L,T,K,r)

def filename_out(harm,L,T):
    return "Best/s_3tone_%dharm_%dspins_%dus.txt" % (harm,L,T)

Ts = np.loadtxt("best_var_monotone.txt")[:,0]
Ks = np.loadtxt("best_var_monotone.txt")[:,1]
best = np.loadtxt("best_var_monotone.txt")[:,2]
etas = np.loadtxt("best_var_monotone.txt")[:,3]



for i in range(len(Ts_list)):  
    harm = harmonics[i]
    L = int(Ts_list[i]/deltat)
    if L==1662:
        L=1663
    
    Ks_now = Ks[Ts==Ts_list[i]]
    best_now = best[Ts==Ts_list[i]]
    eta_now = etas[Ts==Ts_list[i]]
    
    r = int( best_now[np.where(Ks_now==Ks_list[i])[0][0]] )
    eta = eta_now[np.where(Ks_now==Ks_list[i])[0][0]]
    
    system("cp " + filename_in(harm,L,Ts_list[i],Ks_list[i],r) + " " + filename_out(harm,L,Ts_list[i]))
    
    print("%f %f" % (Ts_list[i], eta))
