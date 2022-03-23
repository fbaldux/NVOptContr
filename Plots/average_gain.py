import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

Delta_t = 0.1
tone = 7
harmonic = 0
reps_sig = 1000

plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 14})

dots = ('D','^','v','s','o','P','h','X','>','<')
cols = cm.get_cmap('tab10', 10)
alpha = 0.1


#  ---------------------------------------  theoretical  ---------------------------------------  #

labs = [r"gCP", r"sign(SM)", r"gCP+SA", r"sign(SM)+SA"]

fig, ax = plt.subplots()


filename = "Analysis/finalT_dt%.4f_t%d_av%d.txt" % (Delta_t,tone,reps_sig)
data = np.loadtxt(filename).T


for x in range(4):
    ax.plot(data[0], data[1+3*x], '-', marker=dots[x], c=cols(x), ms=4, label=labs[x])
    ax.fill_between(data[0], data[2+3*x], data[3+3*x], color=cols(x), alpha=alpha)


#  ----------------------------------------  vanilla SA  ---------------------------------------  #

Ks = np.array((0.0001,0.0002,0.0003,0.0005,0.0008,0.0013,0.0022,0.0036,0.0060,0.0100))

best_SA = np.zeros(len(data[0]))
best_SA_low = np.zeros(len(data[0]))
best_SA_high = np.zeros(len(data[0]))

for iK in range(len(Ks)): 
    K = Ks[iK]
    
    filename = "Analysis/finalT_dt%.4f_t%d_K%.4f_av%d.txt" % (Delta_t,tone,K,reps_sig)
    data = np.loadtxt(filename).T

    best_SA = np.maximum(best_SA, data[1])
    best_SA_low = np.maximum(best_SA_low, data[2])
    best_SA_high = np.maximum(best_SA_high, data[3])
    
    
ax.plot(data[0], best_SA, '-', marker=dots[x+1], c=cols(x+1), ms=4, label=r"SA")
ax.fill_between(data[0], best_SA_low, best_SA_high, color=cols(x+1), alpha=alpha)


#  --------------------------------------  plot style etc  -------------------------------------  #

ax.set_xlabel(r"$T$ [$\mu$s]")
ax.set_ylabel(r"$\eta_{\mathrm{SM}}/\eta$")

#ax.set_xscale('log')

ax.set_ylim((0,1))

#ax.set_title(r"$\Delta t$=%.3f, $N_{\mathrm{freq}}$=%d" % (Delta_t,tone))
#ax.set_title(r"$N_{\mathrm{freq}}$=%d" % (tone))

plt.text(0.01, 0.94, r"(a)", transform=ax.transAxes)

ax.legend()
#plt.gca().tick_params(axis='both', which='major')
plt.savefig("Plots/average_gain.pdf", bbox_inches='tight')
plt.show()