#  ---------------------------------------------------------------------------------------------  #
#   
#   The program finds the configuration of continuous spins s[i] that minimezes the cost function
#       
#       H = 0.5 sum_ij J[i,j] s[i] s[j] - log |sum_i h[i] s[i]| - sum_i s[i]**2
#
#   - The variables `J[i,j]` and `h[i]` are loaded from Init/
#   - From the continuous spins are generated Ising spins s_Ising[i] = sign(s[i]), that are 
#     then saved to Configurations/, with the # of pulses and 1/eta in the header.
#
#  ---------------------------------------------------------------------------------------------  #


import sys
import numpy as np
from scipy.linalg import toeplitz
from scipy.fft import fft,ifft
from scipy.optimize import fsolve
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
Jmat = toeplitz(J)

# to have decay both for positive and negative indices
#J[N//2+1:] = np.flip(J[1:N//2])

h = np.loadtxt("Init/h_T%.4f_dt%.4f_t%d_h%d.txt" % (Tfin,Delta_t,tone,harmonic))


id1 = np.zeros((N,N))

#  ---------------------------------  functions for S.P. eqs.  ---------------------------------  #

# l.h.s. of the equation
def equation(lamda):
    lamdaDiag = np.zeros(N)
    lamdaDiag[:N//2] = lamda[0]
    lamdaDiag[N//2:] = lamda[1]
    
    Jlamda_inv = np.linalg.inv( Jmat + np.diagflat(lamdaDiag) )
    
    temp = np.dot(Jlamda_inv, h)
    lhs = np.array(( np.sum(np.abs(temp[:N//2])**2), np.sum(np.abs(temp[N//2:])**2) ))
    
    rhs = 0.5*N * np.abs( np.einsum("a,ab,b", h, Jlamda_inv, h) )
    
    return lhs-rhs 

#equation = np.vectorize(equationTemp)
    

#  -------------------------------------  solve S.P. eqs.  -------------------------------------  #

lamda = np.loadtxt("lambda.txt") 

# solve equation in [a,b]
lamda = fsolve(equation, np.ones(2)*lamda)


#  -------------------------------  transform back to real space  ------------------------------  #

lamdaDiag = np.zeros(N)
lamdaDiag[:N//2] = lamda[0]
lamdaDiag[N//2:] = lamda[1]

Jlamda_inv = np.linalg.inv( Jmat + np.diagflat(lamdaDiag) )

s = np.einsum("ab,b->a", Jlamda_inv, h) / np.sqrt( np.abs( np.einsum("a,ab,b", h, Jlamda_inv, h) ) )

s_Ising = np.sign(s).astype(np.int_)

print(lamda)

#  -------------------------------------------  plot  ------------------------------------------  #
"""
filename = "Configurations/sSpher_T%.4f_dt%.4f_t%d_h%d.txt" % (Tfin,Delta_t,tone,harmonic)
sTrue = np.loadtxt(filename)

plt.plot(np.arange(N), s, '-', c='black', label=r"2 lambda")
#plt.plot(np.arange(N), s_Ising, '--', c='firebrick', label=r"$s_i = \pm 1$")
plt.plot(np.arange(N), sTrue, ':', c='darkgreen', label=r"1 lambda")

plt.xlabel(r"$i$")
plt.ylabel(r"$s_i$")

#plt.title(r"solution for $N=%d$ spins, $T_f = %.1f$" % (N,N*0.16))

plt.legend()
plt.show()
#exit(0)
"""
#  ------------------------------------  sensitivity & co.  ------------------------------------  #

def energy(s):
    return 0.5*np.einsum("a,ab,b", s, Jmat, s) - np.log( np.abs( np.dot(h,s) ) )

def domain_walls(s):
    #return (N - np.dot(s[:-1],s[1:]) - 1) // 2
    return np.sum( np.abs(np.diff(s)) ) // 2

def etaInv(epsilon):
    return 1. / np.exp( epsilon - np.log(28025) - 0.5*np.log(Tfin*1e-6) )


#  ---------------------------------------  save to file  --------------------------------------  #
"""
filename = "Configurations/sSpher2_T%.4f_dt%.4f_t%d_h%d.txt" % (Tfin,Delta_t,tone,harmonic)
head = "pulses=%d, 1/eta=%f" % (domain_walls(s_Ising), etaInv(energy(s_Ising)))
np.savetxt(filename, s_Ising, header=head, fmt='%d')
"""

f = open("lambda2.txt", 'a')
f.write("%f %e\n" % (Tfin, etaInv(energy(s))) )
f.close()

















