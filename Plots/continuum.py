#  ---------------------------------------------------------------------------------------------  #
#
#   ...
#
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import convolve
from matplotlib import pyplot as plt
from matplotlib import cm


tone = 3
harmonic = 0

plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 14})
#plt.rcParams.update({"text.usetex": True})
#plt.rcParams["figure.figsize"] = [5,5]
fig, ax = plt.subplots()

cols = cm.get_cmap("inferno_r", 40)

#####################  IMPORT  #####################

Tfin = np.arange(10,500,10)
maxEtaInv = np.zeros(len(Tfin))

for iT in range(len(Tfin)):
    T = Tfin[iT]
    
    filename = "Results/cont_T%.10f.txt" % (T)
    data = np.loadtxt(filename).T
    #ax.plot(data[0], data[3], '-', label=T, c=cols(iT))
    
    maxEtaInv[iT] = np.max(data[3])
    
ax.plot(Tfin, maxEtaInv, '.')
#ax.plot(Tfin[::3], maxEtaInv[::3], '-')

data = np.loadtxt("bound.txt").T
ax.plot(data[0], data[1],'-')
#np.savetxt("bound.txt", np.stack((Tfin[::3], maxEtaInv[::3])).T, fmt="%f")


#####################  CONVOLVE  #####################

s = 3
f = lambda x: np.exp(-0.5*(x/s)**2) / np.sqrt(2*np.pi*s**2)
sm = f( np.arange(-len(Tfin)//2, len(Tfin)//2) )

maxEtaInv2 = convolve(sm, maxEtaInv, mode='same')

#ax.plot(Tfin, maxEtaInv2, '.')


#####################  INTERPOLATE  #####################

f = interp1d(Tfin[::3], maxEtaInv2[::3], kind='cubic')

x = np.linspace(Tfin[0], Tfin[-1], 100)
y = f(x)

#ax.plot(x, y, '-')


#np.savetxt("bound.txt", np.stack((x,y)).T, fmt="%f")


#####################  FIT  #####################

from scipy.optimize import curve_fit


def fitfunc(x,a,b,c):
    return -a + b/(np.exp(-c*x)+1)
    #return -a + 2*a/(np.exp(-b*x)+1)


fit = (70,200,0.01)
fit, cov = curve_fit(fitfunc, Tfin, maxEtaInv, p0=fit)
#fiterr = np.sqrt(np.diag(cov))
print(fit)
plt.plot(x, fitfunc(x,*fit), '--')

#####################  PLOT  #####################


ax.set_xlabel(r"$T_{\mathit{fin}}$")
ax.set_ylabel(r"$\eta^{-1}$")

ax.set_title("Theoretical upper bound")

#ax.set_xscale('log')

#ax.legend(fontsize=12, ncol=2)
plt.show()