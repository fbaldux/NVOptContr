import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

Delta_t = float( sys.argv[1] )
tone = int( sys.argv[2] )
harmonic = 0
reps_sig = int( sys.argv[3] )

plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 16})

dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')
cols = cm.get_cmap('magma', 12)

labs = ["gCPMG", "spherical", r"gCPMG $\to$ SA", r"spherical $\to$ SA"]

fig, ax = plt.subplots()

Ks = np.array((0.0001,0.0002,0.0003,0.0005,0.0008,0.0013,0.0022,0.0036,0.0060,0.0100))

for iK in range(len(Ks)): 
    K = Ks[iK]
    
    filename = "Analysis/finalT_dt%.4f_t%d_K%.4f_av%d.txt" % (Delta_t,tone,K,reps_sig)
    data = np.loadtxt(filename).T


    ax.plot(data[0], data[1], '-', c=cols(iK), ms=4, label=K)
    #ax.fill_between(data[0], data[2], data[3], color=cols(iK), alpha=0.2)

"""ax.plot(data[0], data[3], '-', marker=dots[1], c=cols(1), ms=4, label=labs[1])
ax.plot(data[0], data[5], '-', marker=dots[2], c=cols(2), ms=4, label=labs[2])
ax.plot(data[0], data[7], '-', marker=dots[3], c=cols(3), ms=4, label=labs[3])
"""

ax.set_xlabel(r"$T_{\mathrm{fin}}$")
ax.set_ylabel(r"$\langle \eta_{\mathrm{bound}}/\eta \rangle$")

#ax.set_xscale('log')

#ax.set_title(r"$\Delta t$=%.3f, $N_{\mathrm{freq}}$=%d" % (Delta_t,tone))
ax.set_title(r"$N_{\mathrm{freq}}$=%d" % (tone))

ax.legend(fontsize=14)

plt.savefig("plot.pdf", bbox_inches='tight')
plt.show()