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


plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 16})
#plt.rcParams.update({"text.usetex": True})
#plt.rcParams["figure.figsize"] = [5,5]
fig, ax = plt.subplots()

intv = np.vectorize(int)

data = np.loadtxt("times_good.txt").T

Ns = intv(data[0]/0.16)

ax.plot(Ns, data[1], 'o', ms=4, label="schedule 1.")
ax.plot(Ns, data[2]+data[3], 's', ms=4, label="schedule 2.")

    
ax.set_xlabel(r"$N = T/\Delta t$")
ax.set_ylabel(r"CPU time [s]")

ax.text(0.01, 0.94, r"(b)", transform=ax.transAxes)

ax.set_yscale('log')

ax.legend(fontsize=15)
plt.savefig("Plots/runtime.pdf", bbox_inches='tight')
plt.show()