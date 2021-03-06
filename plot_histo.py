import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

Tfin = float( sys.argv[1] )
Delta_t = float( sys.argv[2] )
tone = int( sys.argv[3] )
harmonic = 0
reps_sig = int( sys.argv[4] )


dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')
cols = cm.get_cmap('Set1', 10)

title = ["Naive", "Spher", "AnnNaive", "AnnSpher", "Bound"]
labs = ["gCPMG", "spherical", r"gCPMG $\to$ SA", r"spherical $\to$ SA", "bound"]

plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 16})


fig, ax = plt.subplots()

for x in range(4):
    
    #filename = "Analysis/eta" + title[x] + "_dt%.4f_t%d_av%d.txt" % (Delta_t,tone,reps_sig)
    filename = "Analysis/etaRel" + title[x] + "_T%.4f_dt%.4f_t%d_av%d.txt" % (Tfin,Delta_t,tone,reps_sig)
    bins, histo = np.loadtxt(filename).T

    ax.plot(bins, histo, '-', marker=dots[x], ms=4, label=labs[x], c=cols(x))


#ax.set_xlabel(r"$1/\eta$")
ax.set_xlabel(r"$\eta_{\mathrm{bound}}/\eta$")
ax.set_ylabel(r"$P(\eta_{\mathrm{bound}}/\eta)$")

#ax.set_xscale('log')

#ax.set_title(r"$T_{\mathrm{fin}}$=%.1f, $\Delta t$=%.3f, $N_{\mathrm{freq}}$=%d" % (Tfin,Delta_t,tone))
ax.set_title(r"$T_{\mathrm{fin}}$=%.1f, $N_{\mathrm{freq}}$=%d" % (Tfin,tone))

ax.legend(fontsize=14)

plt.savefig("plot.pdf", bbox_inches='tight')
plt.show()