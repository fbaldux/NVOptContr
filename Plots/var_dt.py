#  ---------------------------------------------------------------------------------------------  #
#
#   Given the final time and tone, the program plots the sensitivities for all the
#   values of K found in Results/
#
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

Tfin = 160
Delta_t = np.array((1.6,0.963855421686747,0.5755395683453237,0.3448275862068966,0.20671834625322996,\
                    0.12393493415956623,0.07428040854224698,0.044531032563317564,0.02669336002669336,0.016))
tone = 3
harmonic = 0


plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 14})
#plt.rcParams.update({"text.usetex": True})
plt.rcParams["figure.figsize"] = [5,5]
fig, ax = plt.subplots()

#cols = cm.get_cmap("inferno_r", len(Ks)+1)

    

for it in range(len(Delta_t)):
    dt = Delta_t[it]
    
    filename = "Results/T%.4f_dt%.4f_t%d_h%d_K%.4f.txt" % (Tfin,dt,tone,harmonic,0)
    data = np.loadtxt(filename).T
    
    #lab = r"$N = %d$" % int(Tfin/dt)
    ax.plot(int(Tfin/dt), data[1], marker='o', ms=4, c='black')
    
ax.set_xlabel(r"$N$")
ax.set_ylabel(r"$\eta^{-1}$")

ax.set_xscale('log')

#ax.legend(fontsize=12)
plt.show()