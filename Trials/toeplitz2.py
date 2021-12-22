import numpy as np
from scipy.linalg import toeplitz,eigh
from scipy.fft import fft,ifft,fftshift
from scipy.optimize import fsolve,brentq
from matplotlib import pyplot as plt
rng = np.random.default_rng()

N = 5

#  ------------------------------------------  costruisco A  -----------------------------------------  #

# OK, cosi' e' giusto
Amod = lambda x: np.exp(-x)
Avec = Amod(np.arange(N))
A = toeplitz(Avec)

"""
A = np.zeros((N,N))

for a in range(N):
    for b in range(N):
        A[a,b] = Amod(np.abs(a-b))
    
print(A)
print(toeplitz(Amod(np.arange(N))))
exit(0)
"""

#  ------------------------------------------  costruisco A in Fourier  -----------------------------------------  #
"""
AvecF = fft(Avec, norm='ortho')

AmatF = np.zeros((N,N), dtype=np.complex_)
for nk in range(N):
    for nl in range(N):
        for a in range(N):
            for b in range(N):
                AmatF[nk,nl] += A[a,b] * np.exp( -2j*np.pi*nk*a/N - 2j*np.pi*nl*b/N )

AmatF /= N
"""
#print(AvecF)
#print(AmatF)
"""
plt.imshow(np.log(np.abs(AmatF)), cmap='viridis')
plt.show()
exit(0)
"""

#  ------------------------------------------  costruisco A diagonalizzata veramente  -----------------------------------------  #

AF, U = eigh(A)

# CHECKATO: AF == U^+ @ A @ U
#           A == U @ AF @ U^+

AmatF = np.diag(AF)

#  ------------------------------------------  costruisco v  -----------------------------------------  #

v = np.sin( np.arange(N) )

#vF = fft(v, norm='ortho')

"""
# check di come fa la trasformata
vF2 = np.zeros(N, dtype=np.complex_)
for nk in range(N):
    for a in range(N):
        vF2[nk] += v[a] * np.exp( -2j*np.pi*nk*a/N )
vF2 /= np.sqrt(N)

print(vF)
print(vF2)
"""

vF = np.dot( np.conj(U.T), v ) 


#  ------------------------------------------  controllo i prodotti  -----------------------------------------  #

print(np.einsum("a,ab,b", v, A, v))
print(np.einsum("a,ab,b", vF.conj(), AmatF, vF))






