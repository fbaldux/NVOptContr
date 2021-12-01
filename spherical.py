import numpy as np
from scipy.linalg import toeplitz
from scipy.fft import fft,ifft,fftshift
from scipy.optimize import fsolve,brentq
from matplotlib import pyplot as plt


#  ------------------------------------------  import  -----------------------------------------  #

#h = np.loadtxt("h_T160.0000_dt0.1600_h5.txt")
h = np.loadtxt("h_3tone_1000spins_160us.txt")
N = len(h)
#print("N =", N)

J = np.loadtxt("J_T160.0000_dt0.1600.txt")
# to have decay both for positive and negative indices
J[N//2+1:] = np.flip(J[1:N//2])
#J = fftshift( np.loadtxt("J_T16.0000_dt0.1600.txt") )

"""
plt.plot(np.arange(N), h, '-')
plt.plot(np.arange(N), J, '-')
plt.show()
exit(0)
"""
#  ------------------------------------  Fourier transform  ------------------------------------  #

hF = fft(h)
JF = fft(J)
"""
plt.plot(np.arange(N), hF, '-')
plt.plot(np.arange(N), JF, '-')
plt.show()
exit(0)
"""
#  ---------------------------------  functions for S.P. eqs.  ---------------------------------  #

# l.h.s. of the equation
def lhsTemp(lamda):
    return np.sum( np.abs( hF / (JF + lamda) )**2 )
lhs = np.vectorize(lhsTemp)

# r.h.s. of the equation
def rhsTemp(lamda):
    return N * np.abs( np.sum( np.abs(hF)**2 / (JF + lamda) ) )
rhs = np.vectorize(rhsTemp)

# combined equation
def eqLamda(lamda):
    return lhs(lamda) - rhs(lamda)
    

l = np.linspace(0,0.01,1000)
plt.plot(l, lhs(l), '-')
plt.plot(l, rhs(l), '-')
plt.yscale("log")
plt.show()
#exit(0)

#  -------------------------------------  solve S.P. eqs.  -------------------------------------  #

#lamda = fsolve(eqLamda, 1e-3)[0]
lamda = brentq(eqLamda, 0, 1e-2)

print("lamda:", lamda)


#  -------------------------------  transform back to real space  ------------------------------  #

C = np.sqrt( N * np.sum(hF*hF.conj()/(JF+lamda)) )
#C = np.sqrt( np.sum(np.abs(hF/(JF+lamda))**2) )

sF = N*hF / (C*(JF+lamda))

s = ifft(sF)

#s_ann = np.loadtxt("s_T16.0000_dt0.1600_h5_K0.0001_r0.txt")
#s_ann = np.loadtxt("s_T160.0000_dt0.1600_h5_K0.0100_r0.txt")
s_ann = np.loadtxt("s_3tone_1000spins_160us_K0.0050_r9.txt")


plt.plot(np.arange(N), s.real, '-', c='black', label=r"$s_i \in \mathbb{R}$")
plt.plot(np.arange(N), np.sign(s.real), '--', c='firebrick', label=r"$s_i = \pm 1$")
plt.plot(np.arange(N), -s_ann, ':', c='darkgreen', label=r"sim. anneal.")
#plt.plot(np.arange(N), s.imag, '--', c='black')

plt.xlabel(r"$i$")
plt.ylabel(r"$s_i$")

plt.title(r"solution for $N=%d$ spins, $T_f = %.1f$" % (N,N*0.16))

plt.legend()
plt.show()
#exit(0)


#  ---------------------------------------  sensitivity  ---------------------------------------  #

print("norm:", np.sum(np.abs(s.real)**2))

Jmat = toeplitz(J)
#s = np.sign(s)

def etaInv(epsilon):
    return 1./np.exp(epsilon - np.log(28025)-0.5*np.log(N*0.16e-6));

def energy(s):
    return np.dot(np.dot(s,Jmat),s) - np.log( np.abs( np.dot(h,s) ) )

E_sph = energy(s.real)
E_Is = energy(np.sign(s.real))

print("E Ising:", E_Is)
print("E spherical:", E_sph)


print("etaInv Ising:", etaInv(E_Is))
print("etaInv spherical:", etaInv(E_sph))


























