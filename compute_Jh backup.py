import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad


T = 400 # µs
deltat = 0.160 #µs
L = int(T/deltat)
print(L, "spins")


# -------------------------------------------------------------------------------------------------------
#  compute J

"""
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
#plt.plot(abs(i_index-j_index))
#Jt = np.reshape(res[abs(i_index-j_index)],[L,L])
Jt = np.reshape(res_01[abs(i_index-j_index)],[L,L])



np.savetxt("Init/J_%dspins_%dus.txt" % (L, T), Jt.reshape(L**2))

"""

# -------------------------------------------------------------------------------------------------------
#  compute h (3tone)
"""
# AC field (time dependent) formed by a tri-chromatic signal
A1 = 0.065*0.2+1/5; w0 =0.1150; fi1 = 0;
B1 = 0.237*0.2+1/5; wp1=0.2125; fi2 = 0;
C1 = 0.389*0.2+1/5; wm1=0.1450; fi3 = 0;
A = A1/(A1+B1+C1); 
B = B1/(A1+B1+C1);
C = C1/(A1+B1+C1);
ac_params_mf=(A,w0,fi1, B,wp1,fi2, C,wm1,fi3)
#
def target_signal_mf(t1):
    return A*np.cos(2*np.pi*w0*t1 + fi1*np.pi/180) + B*np.cos(2*np.pi*wp1*t1 + (fi1 + fi2)*np.pi/180) + C*np.cos(2*np.pi*wm1*t1 + (fi1 + fi3)*np.pi/180)

#Integrated signal:
def integrated_target_signal_mf(t1):
    return (1/2/np.pi)*(A*np.sin(2*w0*np.pi*t1)/w0 + C*np.sin(2*np.pi*wm1*t1)/wm1 + B*np.sin(2*np.pi*wp1*t1)/wp1)
    


ii = np.arange(L)+1
htT = (integrated_target_signal_mf(ii*deltat) - integrated_target_signal_mf((ii-1)*deltat))/T

print("h fields done")

np.savetxt("Init/h_3tone_%dspins_%dus.txt" % (L, T), htT)
"""



# -------------------------------------------------------------------------------------------------------
#  compute h (1tone, 5th armonic)


# AC field (time dependent) formed by a tri-chromatic signal
A = 1; w0 =0.03929; fi1 = 0;
ac_params_lf=(A,w0,fi1)
#
def target_signal_lf(t1):
    return A*np.cos(2*np.pi*w0*t1 + fi1*np.pi/180)

#Integrated signal:
def integrated_target_signal_lf(t1):
    return (1/2/np.pi)*(A*np.sin(2*w0*np.pi*t1)/w0)


ii = np.arange(L)+1
htT = (integrated_target_signal_lf(ii*deltat) - integrated_target_signal_lf((ii-1)*deltat))/T

print("h fields done")

np.savetxt("Init/h_1tone_%dspins_%dus.txt" % (L, T), htT)

















