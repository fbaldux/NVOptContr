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
Delta_t = 0.16
tone = 3
harmonic = 0
"""
Ks = np.array((0.00010000000000000009,0.00016237767391887224,0.0002636650898730362,0.0004281332398719398,0.0006951927961775608,\
               0.0011288378916846896,0.0018329807108324375,0.0029763514416313187,0.004832930238571755,0.007847599703514618,\
               0.01274274985703134,0.020691380811147905,0.03359818286283785,0.0545559478116852,0.0885866790410083,0.14384498882876626,\
               0.23357214690901223,0.37926901907322474,0.6158482110660267,1.0))
"""
Ks = np.array((0.0004281332398719398,0.0006951927961775608,\
               0.0011288378916846896,0.0018329807108324375,0.0029763514416313187,0.004832930238571755,\
               0.01274274985703134,0.03359818286283785))


plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 16})
#plt.rcParams.update({"text.usetex": True})
#plt.rcParams["figure.figsize"] = [5,5]
fig, ax = plt.subplots()

cols = cm.get_cmap("ocean", len(Ks)+2)


def fexp(f):
    return int(np.floor(np.log10(abs(f)))) if f != 0 else 0

def fman(f):
    return f/10**fexp(f)
    

###################  ONLY ANNEALING  ###################

for iK in range(len(Ks)):
    K = Ks[iK]
    
    filename = "Results/T%.4f_dt%.4f_t%d_h%d_K%.4f.txt" % (Tfin,Delta_t,tone,harmonic,K)
    data = np.loadtxt(filename).T
    #ax.plot(data[0], data[1], 'o', ms=2, label="K=%.1e"%K, c=cols(iK))
    
    av_x = np.average(data[0])
    std_x = np.std(data[0])
    av_y = np.average(data[1])
    std_y = np.std(data[1])
    
    lab = r"$%.2f$$\times$$10^{%d}$" % (fman(K), fexp(K))
    ax.errorbar(av_x, av_y, xerr=std_x, yerr=std_y, marker='o', ms=4, label=lab, c=cols(iK+1))


###################  EXACT -> ANNEALING  ###################

filename = "Results/T%.4f_dt%.4f_t%d_h%d_K%.4f.txt" % (Tfin,Delta_t,tone,harmonic,0)
data = np.loadtxt(filename).T

av_x = np.average(data[0])
std_x = np.std(data[0])
av_y = np.average(data[1])
std_y = np.std(data[1])

ax.errorbar(av_x, av_y, xerr=std_x, yerr=std_y, marker='s', ms=4, c='purple')
ax.plot(52, 81.56, marker='s', ms=4, c='red')


###################  PLOT  ###################

    
ax.set_xlabel(r"$\pi$-pulse number")
ax.set_ylabel(r"$1/\eta$")

#ax.text(0.01, 0.94, r"(a)", transform=ax.transAxes)

#ax.set_xscale('log')

ax.legend(fontsize=15, ncol=2, loc='lower right', title=r"$K$")
plt.savefig("Plots/eta_vs_pulses.pdf", bbox_inches='tight')
plt.show()