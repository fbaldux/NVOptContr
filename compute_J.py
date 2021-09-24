import numpy as np
from scipy.integrate import quad


# input
instring = input("").split(' ')

T = float( instring[0] )
deltat = float( instring[1] )  

L = int(T/deltat)


# New NSD (see Lablog January 27, 2021)
y0 = 0.00119; # MHz
Gamma0 = 0.52; # MHz 
nu0N= 0.4322; # MHz 
tauc0  = 0.0042;  # MHz 

def G0(w):
    return Gamma0*np.exp(-0.5*((w-2*np.pi*nu0N)/(2*np.pi*tauc0)**2))
    
def S(w):
    return y0 + G0(w) 

# for the simulation with function chiCalc:
def funcNoise(x,y0,a,xc,w):
    return y0 + a*np.exp(-0.5*((x-2*np.pi*xc)/(2*np.pi*w))**2)



paraNSD = np.array([y0,Gamma0,nu0N,tauc0])
paraNSD_noOffset = np.array([0,Gamma0,nu0N,tauc0])

omegaLowLimit = 0.001 # rad MHz
omegaHighLimit = 6.5 # rad MHz


## Create matrix $J_{i,j}$ that depends on the NSD $S(\omega)$

omegaNSDLowLimit  = 2*np.pi*(nu0N - 10*tauc0) # rad MHz
omegaNSDHighLimit = 2*np.pi*(nu0N + 10*tauc0) # rad MHz


imj_abs = np.arange(L)

#res_err = [quad( lambda omega: funcNoise(omega,*paraNSD)*np.cos(imj*omega*deltat)*(1 - np.cos(omega*deltat))/omega**2, 
#                omegaLowLimit, omegaHighLimit, limit=100) for imj in imj_abs]
#res,err = (2/np.pi)*np.array(res_err).transpose()



res_err_0 = [quad( lambda omega: funcNoise(omega,*paraNSD_noOffset)*np.cos(imj*omega*deltat)*(1 - np.cos(omega*deltat))/omega**2, 
                  omegaNSDLowLimit, omegaNSDHighLimit, limit=100) for imj in imj_abs]
print('First integral done')
res_err_1 = [quad( lambda omega: np.cos(imj*omega*deltat)*(1 - np.cos(omega*deltat))/omega**2, 
                  omegaLowLimit,omegaHighLimit, limit=150) for imj in imj_abs]
print('Second integral done')
res_01,err_01 = (2/np.pi)*(np.array(res_err_0)+y0*np.array(res_err_1)).transpose()



i_index = np.tile(np.arange(L)+1,L)
j_index = np.repeat(np.arange(L)+1,L)
#Jt = np.reshape(res[abs(i_index-j_index)],[L,L])
Jt = np.reshape(res_01[abs(i_index-j_index)],[L,L])



np.savetxt("Init/J_%dspins_%dus.txt" % (L, T), Jt.reshape(L**2))
