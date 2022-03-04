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
cols = cm.get_cmap('viridis', 6)

title = ["Naive", "Spher", "AnnNaive", "AnnSpher", "Bound"]
labs = ["naive", "spherical", "SA from naive", "SA from spher.", "bound"]

fig, ax = plt.subplots()

for x in range(5):
    
    filename = "Analysis/eta" + title[x] + "_dt%.4f_t%d_av%d.txt" % (Delta_t,tone,reps_sig)
    #filename = "Analysis/etaRel" + title[x] + "_dt%.4f_t%d_av%d.txt" % (Delta_t,tone,reps_sig)
    bins, histo = np.loadtxt(filename).T

    ax.plot(bins, histo, '-', marker=dots[x], ms=4, label=labs[x])


ax.set_xlabel(r"$1/\eta$")
#ax.set_xlabel(r"$\eta_{\mathrm{bound}}/\eta$")
ax.set_ylabel(r"prob")

#ax.set_xscale('log')

ax.set_title(r"$T_{\mathrm{fin}}$=%.1f, $\Delta t$=%.3f, $N_{\mathrm{freq}}$=%d" % (Tfin,Delta_t,tone))

ax.legend()
plt.show()