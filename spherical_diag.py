#  ---------------------------------------------------------------------------------------------  #
#   
#   The program finds the configuration of continuous spins s[i] that minimezes the cost function
#       
#       H = 0.5 sum_ij J[i,j] s[i] s[j] - log |sum_i h[i] s[i]| - sum_i s[i]**2
#
#   - The variables `J[i,j]` and `h[i]` are loaded from Init/
#   - Exact diagonalization is used instead of the FFT.
#   - From the continuous spins are generated Ising spins s_Ising[i] = sign(s[i]), that are 
#     then saved to Configurations/sSpher\_{...}, with the # of pulses and 1/eta in the header.
#
#  ---------------------------------------------------------------------------------------------  #


import sys
import numpy as np
from scipy.linalg import toeplitz,eigh
from scipy.fft import fft,ifft
from scipy.optimize import brentq
from matplotlib import pyplot as plt


Tfin = float( sys.argv[1] )
Delta_t = float( sys.argv[2] )
tone = int( sys.argv[3] )
harmonic = int( sys.argv[4] )
rep = int( sys.argv[5] )

N = int( Tfin / Delta_t )


if tone > 1:
    harmonic = 0


#  ------------------------------------------  import  -----------------------------------------  #

J = np.loadtxt("Init/J_T%.4f_dt%.4f.txt" % (Tfin,Delta_t))
Jmat = toeplitz(J)


h = np.loadtxt("Init/h_T%.4f_dt%.4f_t%d_h%d_r%d.txt" % (Tfin,Delta_t,tone,harmonic,rep))


#  ------------------------------------  Fourier transform  ------------------------------------  #

JD, U = eigh(Jmat)

hD = np.dot( np.conj(U.T), h ) 


#  ---------------------------------  functions for S.P. eqs.  ---------------------------------  #

# l.h.s. of the equation
def lhsTemp(lamda):
    return np.sum( ( hD / (JD + lamda) )**2 )
lhs = np.vectorize(lhsTemp)

# r.h.s. of the equation
def rhsTemp(lamda):
    return N * np.abs( np.sum( hD**2 / (JD + lamda) ) )
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

C = np.sqrt( np.sum( hD**2/(JD+lamda) ) )
sD = hD / ( C*(JD+lamda) )

s = np.dot(U,sD).real

s_Ising = np.sign(s).astype(np.int_)


#  -------------------------------------  naive solutions  -------------------------------------  #

# this is not quite correct
#s_naive = np.sign(h)

# here it really changes sign with the signal
hData = np.loadtxt("Init/hData_T%.4f_dt%.4f_t%d_h%d_r%d.txt" % (Tfin,Delta_t,tone,harmonic,rep)).T

ht = np.zeros(N)
for i in range(N):
    ht[i] = np.sum( hData[0] * np.cos(2*np.pi*hData[1]*(i+0.5)*Delta_t + hData[2]) )

s_naive = np.sign(ht)


#  -------------------------------------------  plot  ------------------------------------------  #

"""
s_ann = np.loadtxt("Configurations/s_T%.4f_dt%.4f_t%d_h%d_K0.0050_r0.txt" % (Tfin,Delta_t,tone,harmonic))


plt.plot(np.arange(N), s, '-', c='black', label=r"$s_i \in \mathbb{R}$")
plt.plot(np.arange(N), s_Ising, '--', c='firebrick', label=r"$s_i = \pm 1$")
plt.plot(np.arange(N), s_ann, ':', c='darkgreen', label=r"sim. anneal.")

plt.xlabel(r"$i$")
plt.ylabel(r"$s_i$")

plt.title(r"solution for $N=%d$ spins, $T_f = %.1f$" % (N,N*0.16))

plt.legend()
plt.show()
exit(0)
"""

#  ------------------------------------  sensitivity & co.  ------------------------------------  #

def energy(s):
    return 0.5*np.einsum("a,ab,b", s, Jmat, s) - np.log( np.abs( np.dot(h,s) ) )

def domain_walls(s):
    #return (N - np.dot(s[:-1],s[1:]) - 1) // 2
    return np.sum( np.abs(np.diff(s)) ) // 2

def etaInv(epsilon):
    #return 1. / np.exp( epsilon - np.log(28025) - 0.5*np.log(Tfin*1e-6) )
    return 28025 * np.sqrt(Tfin) * 1e-3 * np.exp(-epsilon)


#  ---------------------------------------  save to file  --------------------------------------  #

filename = "Results/theor_T%.4f_dt%.4f_t%d_h%d_r%d.txt" % (Tfin,Delta_t,tone,harmonic,rep)
f = open(filename, 'w')
f.write("# pulses 1/eta\n")
f.write("# naive:\n%d %e\n" % (domain_walls(s_naive), etaInv(energy(s_naive))))
f.write("# bound:\n%d %e\n" % (domain_walls(s), etaInv(energy(s))))
f.write("# spher:\n%d %e\n" % (domain_walls(s_Ising), etaInv(energy(s_Ising))))
f.close()


filename = "Configurations/sSpher_T%.4f_dt%.4f_t%d_h%d_r%d.txt" % (Tfin,Delta_t,tone,harmonic,rep)
head = "pulses=%d, 1/eta=%f" % (domain_walls(s_Ising), etaInv(energy(s_Ising)))
np.savetxt(filename, s_Ising, header=head, fmt='%d')

filename = "Configurations/sGCP_T%.4f_dt%.4f_t%d_h%d_r%d.txt" % (Tfin,Delta_t,tone,harmonic,rep)
head = "pulses=%d, 1/eta=%f" % (domain_walls(s_naive), etaInv(energy(s_naive)))
np.savetxt(filename, s_naive, header=head, fmt='%d')




















