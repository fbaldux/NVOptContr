import numpy as np
import matplotlib.pyplot as plt

L = 625
T = 100

J = np.loadtxt("Init/J_3tone_%dspins_%dus.txt" % (L, T)).reshape(L,L)
h = np.loadtxt("Init/h_3tone_%dspins_%dus.txt" % (L, T))
s = np.loadtxt("49.txt")

for i in range(L):
    J[i,i] = 0

gamma = 28025


eps = np.einsum("a,ab,b", s, J, s) - np.log(abs(np.dot(h,s)))
eta_inv = 1./ (np.exp(eps)/gamma/np.sqrt(T*1e-6))


print(eta_inv)


#np.savetxt("Init/h_3tone_%dspins_%dus.txt" % (L, T), htT)

























