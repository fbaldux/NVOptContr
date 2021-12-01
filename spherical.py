import sys
import numpy as np
from scipy.linalg import toeplitz
from scipy.fft import fft,ifft
from scipy.optimize import brentq
from matplotlib import pyplot as plt


Tfin = float( sys.argv[1] )
Delta_t = float( sys.argv[2] )
tone = int( sys.argv[3] )
harmonic = int( sys.argv[4] )

N = int( Tfin / Delta_t )


if tone == 3:
    harmonic = 0
elif tone != 1:
    sys.stderr.write("\nError! Unrecognized tone value.\n\n")
    exit(-1)

#  ------------------------------------------  import  -----------------------------------------  #

J = np.loadtxt("Init/J_T%.4f_dt%.4f.txt" % (Tfin,Delta_t))
# to have decay both for positive and negative indices
#J[N//2+1:] = np.flip(J[1:N//2])

h = np.loadtxt("Init/h_T%.4f_dt%.4f_t%d_h%d.txt" % (Tfin,Delta_t,tone,harmonic))


#  ------------------------------------  Fourier transform  ------------------------------------  #

hF = fft(h, norm='ortho')
JF = fft(J, norm='ortho')


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
def equation(lamda):
    return lhs(lamda) - rhs(lamda)
    

#  -------------------------------------  solve S.P. eqs.  -------------------------------------  #

# find interval [a,b] in which equation changes sign
a = 0
b = 0.1
sign0 = np.sign(lhs(a)-rhs(a))

while np.sign(lhs(b)-rhs(b)) == sign0:
    b += 0.1

# solve equation in [a,b]
lamda = brentq(equation, a, b)


#  -------------------------------  transform back to real space  ------------------------------  #

# non-ortho
#C = np.sqrt( N * np.sum( np.abs(hF)**2/(JF+lamda) ) )
#sF = N*hF / (C*(JF+lamda))

# ortho
C = np.sqrt( np.sum( np.abs(hF)**2/(JF+lamda) ) )
sF = hF / ( C*(JF+lamda) )

s = ifft(sF, norm='ortho')

s_Ising = np.sign(s.real)


#  -------------------------------------------  plot  ------------------------------------------  #

"""
plt.plot(np.arange(N), s.real, '-', c='black', label=r"$s_i \in \mathbb{R}$")
plt.plot(np.arange(N), np.sign(s.real), '--', c='firebrick', label=r"$s_i = \pm 1$")
#plt.plot(np.arange(N), -s_ann, ':', c='darkgreen', label=r"sim. anneal.")
#plt.plot(np.arange(N), s.imag, '--', c='black')

plt.xlabel(r"$i$")
plt.ylabel(r"$s_i$")

plt.title(r"solution for $N=%d$ spins, $T_f = %.1f$" % (N,N*0.16))

plt.legend()
plt.show()
#exit(0)

"""

#  ---------------------------------------  sensitivity  ---------------------------------------  #

Jmat = toeplitz(J)
def energy(s):
    return np.einsum("a,ab,b", s, Jmat, s) - np.log( np.abs( np.dot(h,s) ) )

def domain_walls(s):
    count = 0
    for i in range(1,N):
        count += s[i]*s[i-1]
    
    return (N-count-1)//2

def etaInv(epsilon):
    return 1. / np.exp( epsilon - np.log(28025) - 0.5*np.log(N*0.16e-6) )


#  ---------------------------------------  save to file  --------------------------------------  #

filename = "Configurations/sSpher_T%.4f_dt%.4f_t%d_h%d.txt" % (Tfin,Delta_t,tone,harmonic)
head = "pulses=%d, 1/eta=%f" % (domain_walls(s_Ising), etaInv(energy(s_Ising)))
np.savetxt(filename, s_Ising, header=head, fmt='%d')























