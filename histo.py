import numpy as np
from matplotlib import pyplot as plt


histoL,binsL = np.histogram(np.loadtxt("linear.txt"), bins=20, density=True)
binsL = 0.5 * (binsL[:-1] + binsL[1:])


histoE,binsE = np.histogram(np.loadtxt("exp.txt"), bins=20, density=True)
binsE = 0.5 * (binsE[:-1] + binsE[1:])
"""
histoE2,binsE2 = np.histogram(np.loadtxt("exp2.txt"), bins=20, density=True)
binsE2 = 0.5 * (binsE2[:-1] + binsE2[1:])
"""

plt.plot(binsL, histoL, '-', label="linear")
plt.plot(binsE, histoE, '-', label="exp")
#plt.plot(binsE2, histoE2, '-', label="exp2")

plt.legend()
plt.show()