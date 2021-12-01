import numpy as np
from scipy.linalg import toeplitz,eigh
from scipy.fft import fft,ifft,fftshift
from scipy.optimize import fsolve,brentq
from matplotlib import pyplot as plt
rng = np.random.default_rng()

N = 10


# MATRICE A

Avec = np.zeros(N)
Avec[0] = 2
Avec[1] = -1
Avec[-1] = -1
Avec[2] = 0.5
Avec[-2] = 0.5

#Avec = np.zeros(N)
#Avec[:N//2] = 1 - np.tanh(np.arange(N//2))
#Avec[N//2:] = np.flip(Avec[:N//2])

#Avec = 1 - np.tanh( np.abs( np.arange(-N//2,N//2) ) )
#Avec = fftshift(Avec)

A = toeplitz(Avec)
"""
plt.plot(np.arange(N), Avec, '.')
plt.show()
exit(0)
"""
AvecF = fft(Avec, norm='ortho')

print(A)
exit(0)

# VETTORE v
v = np.exp(-2j*np.pi * 1 * np.arange(N) / N )
#v = np.sin(np.arange(N))
vF = fft(v, norm='ortho')


# TEST

print("v norm:", np.real( np.einsum("a,a", v.conj(),v) ))

print("vF norm", np.real( np.einsum("a,a", vF.conj(),vF) ), "\n")


print("v* A v:", np.einsum("a,ab,b", v.conj(), A, v))
print("theor:", 2*(1-np.cos(2*np.pi/N)), "\n")


print("vF* AF vF:", np.sqrt(N)*np.einsum("a,a,a", vF.conj(), AvecF, vF))










