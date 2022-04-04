#  ---------------------------------------------------------------------------------------------  #
#   
#   The program finds the configuration of continuous spins s[i] that minimezes the cost function
#       
#       H = 0.5 sum_ij J[i,j] s[i] s[j] - log |sum_i h[i] s[i]| - sum_i lamda[i] (s[i]**2 - 1 )
#
#   - The variables `J[i,j]` and `h[i]` are loaded from Init/
#   - Exact diagonalization is used instead of the FFT.
#   - lambda can assume at most k different values.
#   - From the continuous spins are generated Ising spins s_Ising[i] = sign(s[i]), that are 
#     then saved to Configurations/sSpher\_{...}, with the # of pulses and 1/eta in the header.
# 
#
#  ---------------------------------------------------------------------------------------------  #


import sys
import numpy as np
from scipy.linalg import toeplitz, eigh, inv
from scipy.fft import fft,ifft
from scipy.optimize import fsolve, brentq
from matplotlib import pyplot as plt


Tfin = float( sys.argv[1] )
Delta_t = float( sys.argv[2] )
tone = int( sys.argv[3] )
harmonic = int( sys.argv[4] )
rep = int( sys.argv[5] )

k = int( sys.argv[6] )

if tone > 1:
    harmonic = 0


#  ------------------------------------------  import  -----------------------------------------  #

J = np.loadtxt("Init/J_T%.4f_dt%.4f.txt" % (Tfin,Delta_t))
Jmat = toeplitz(J)


h = np.loadtxt("Init/h_T%.4f_dt%.4f_t%d_h%d_r%d.txt" % (Tfin,Delta_t,tone,harmonic,rep))


#  -----------------------------------------  define N  ----------------------------------------  #

N = len(h)
g = N // k

if N % k != 0:
    raise RuntimeError("N not divisible by k!")


#  ------------------------------------  sensitivity & co.  ------------------------------------  #

def energy(s):
    return 0.5*np.einsum("a,ab,b", s, Jmat, s) - np.log( np.abs( np.dot(h,s) ) )

def domain_walls(s):
    #return (N - np.dot(s[:-1],s[1:]) - 1) // 2
    return np.sum( np.abs(np.diff(s)) ) // 2

def etaInv(epsilon):
    return 1. / np.exp( epsilon - np.log(28025) - 0.5*np.log(Tfin*1e-6) )


############################################  1 lambda  ###########################################

#  ---------------------------------------  diagonalize  ---------------------------------------  #

JD, U = eigh(Jmat)

hD = np.dot( np.conj(U.T), h ) 


#  -----------------------------  saddle-point equation (1 lambda)  ----------------------------  #

# combined equation
def SPeq_1lambda(lamda):
    return np.sum( ( hD / (JD + lamda) )**2 ) - N * np.abs( np.sum( hD**2 / (JD + lamda) ) )
 

#  ----------------------------------  solve SP eq (1 lambda)  ---------------------------------  #

# find interval [a,b] in which equation changes sign
a = 0
b = 0.1
sign0 = np.sign(SPeq_1lambda(a))

while np.sign(SPeq_1lambda(b)) == sign0:
    b += 0.1

# solve equation in [a,b]
lamda1 = brentq(SPeq_1lambda, a, b)


#  -------------------------  transform back to real space (1 lambda)  ------------------------  #

C = np.sqrt( np.sum( hD**2/(JD+lamda1) ) )
sD = hD / ( C*(JD+lamda1) )

s = np.dot(U,sD).real

print("lamda(1):", lamda1)
print("etaInv(1):", etaInv(energy(s)))


##########################################  more lambdas  #########################################

#  --------------------------  saddle-point equations (more lambdas)  --------------------------  #

def SPeq_moreLambdas(lamda):
    lamdaDiag = np.zeros(N)
    for i in range(k):
        lamdaDiag[i*g:(i+1)*g] = lamda[i]

    
    Jlamda_inv = np.linalg.inv( Jmat + np.diagflat(lamdaDiag) )
    
    temp = np.dot(Jlamda_inv, h)
    lhs = np.array( [np.sum(np.abs(temp[i*g:(i+1)*g])**2) for i in range(k)] )
    
    rhs = N/k * np.abs( np.einsum("a,ab,b", h, Jlamda_inv, h) )
    
    return lhs-rhs 
    

#  -------------------------------  solve SP eqs (more lambdas)  -------------------------------  #

lamda2 = fsolve(SPeq_moreLambdas, np.ones(k)*lamda1)


#  -----------------------  transform back to real space (more lambdas)  -----------------------  #

lamdaDiag = np.zeros(N)
for i in range(k):
    lamdaDiag[i*g:(i+1)*g] = lamda2[i]


Jlamda_inv = np.linalg.inv( Jmat + np.diagflat(lamdaDiag) )

s = np.einsum("ab,b->a", Jlamda_inv, h) / np.sqrt( np.abs( np.einsum("a,ab,b", h, Jlamda_inv, h) ) )

print("lamda(%d):" % k, lamda2)
print("etaInv(%d):" % k, etaInv(energy(s)))



f = open("moreLambdas.txt", "a")
f.write("%d %f\n" % (k, etaInv(energy(s))))
f.close()













