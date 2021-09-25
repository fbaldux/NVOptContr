import numpy as np
from scipy.integrate import quad
import os

# input
instring = input("").split(' ')

T = float( instring[0] )
deltat = float( instring[1] )  
tone = int( instring[2] ) 
harmonic = int( instring[3] ) 

L = int(T/deltat)


# -------------------------------------------------------------------------------------------------------
#  compute h (3tone)
if tone==3:

    #if os.path.exists("Init/h_3tone_%dspins_%dus.txt" % (L, T)):
    #    exit(0)
        
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

    #print("h fields done")

    np.savetxt("Init/h_3tone_%dspins_%dus.txt" % (L, T), htT)


# -------------------------------------------------------------------------------------------------------
#  compute h (1tone, certain harmonic)

elif tone==1:
    
    if os.path.exists("Init/h_1tone_%dharm_%dspins_%dus.txt" % (harmonic, L, T)):
        exit(0)
    
    w0 = 0.4322 / (2*harmonic+1); # MHz (central freq of the noise-spectral-density)
    A = 1; fi1 = 0;
    ac_params_lf=(A,w0,fi1)
    
    def target_signal_lf(t1):
        return A*np.cos(2*np.pi*w0*t1 + fi1*np.pi/180)

    #Integrated signal:
    def integrated_target_signal_lf(t1):
        return (1/2/np.pi)*(A*np.sin(2*w0*np.pi*t1)/w0)


    ii = np.arange(L)+1
    htT = (integrated_target_signal_lf(ii*deltat) - integrated_target_signal_lf((ii-1)*deltat))/T

    #print("h fields done")

    np.savetxt("Init/h_1tone_%dharm_%dspins_%dus.txt" % (harmonic, L, T), htT)

















