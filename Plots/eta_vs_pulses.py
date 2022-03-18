import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

Tfin = 100
Delta_t = 0.1
tone = 7
harmonic = 0


Ks = np.array((0.0001,0.0002,0.0003,0.0005,0.0008,0.0013,0.0022,0.0036,0.0060,0.0100))

plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 14})

#plt.rcParams["figure.figsize"] = [5,5]
fig, ax = plt.subplots()

cols = cm.get_cmap("inferno_r", len(Ks)+1)


def fexp(f):
    return int(np.floor(np.log10(abs(f)))) if f != 0 else 0

def fman(f):
    return f/10**fexp(f)
    
#  ----------------------------------------  vanilla SA  ---------------------------------------  #

for iK in range(1,len(Ks)):
    K = Ks[iK]
    
    filename = "Results4Plots/SA_T%.4f_dt%.4f_t%d_h%d_K%.4f_r%d.txt" % (Tfin,Delta_t,tone,harmonic,K,0)
    data = np.loadtxt(filename).T
    #ax.plot(data[0], data[1], 'o', ms=2, label="K=%.1e"%K, c=cols(iK))
    
    av_x = np.average(data[0])
    std_x = np.std(data[0])
    av_y = np.average(data[1])
    std_y = np.std(data[1])
    
    if iK%2==1:
        lab = r"$K = %.2f$$\times$$10^{%d}$" % (fman(K), fexp(K))
        ax.errorbar(av_x, av_y, xerr=std_x, yerr=std_y, marker='o', ms=4, label=lab, c=cols(iK+1))
    else:
        ax.errorbar(av_x, av_y, xerr=std_x, yerr=std_y, marker='o', ms=4, c=cols(iK+1))
        

#  -----------------------------------  spherical model + SA  ----------------------------------  #

filename = "Results4Plots/SAspher_T%.4f_dt%.4f_t%d_h%d_K%.4f_r%d.txt" % (Tfin,Delta_t,tone,harmonic,0,0)
data = np.loadtxt(filename).T

av_x = np.average(data[0])
std_x = np.std(data[0])
av_y = np.average(data[1])
std_y = np.std(data[1])

ax.errorbar(av_x, av_y, xerr=std_x, yerr=std_y, marker='s', ms=4, label=r"sign(SM)+SA", c='tab:green')

"""
#  -------------------------------------  spherical model  -------------------------------------  #

filename = "Results4Plots/theor_T%.4f_dt%.4f_t%d_h%d_r%d.txt" % (Tfin,Delta_t,tone,harmonic,0)
data = np.loadtxt(filename).T

lab = "SM"
ax.plot(data[0,2], data[1,2], 's', ms=4, label=r"sign(SM)", c='tab:blue')
"""

#  --------------------------------------  plot style etc  -------------------------------------  #

ax.set_xlabel(r"$\pi$ pulses")
ax.set_ylabel(r"$1/\eta$ [Hz$^{1/2}/\mu$T]")

#ax.set_xscale('log')

plt.text(0.01, 0.94, r"(b)", transform=ax.transAxes)


ax.legend(ncol=2, loc='lower right', handlelength=1)
plt.savefig("Plots/eta_vs_pulses.pdf", bbox_inches='tight')
plt.show()





