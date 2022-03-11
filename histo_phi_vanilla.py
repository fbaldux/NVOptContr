#  ---------------------------------------------------------------------------------------------  #
#   
#   The program saves to Analysis/phi{...} the histogram of `phi = eta\_bound / eta`, from the SA 
#   optimization starting at infinite temperature.  
#   It also saves to Analysis/finalT\_{...} the averages as a function of the total sensing time.
#
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np

Tfin = float( sys.argv[1] )
Delta_t = float( sys.argv[2] )
tone = int( sys.argv[3] )
harmonic = 0
K = float( sys.argv[4] )
reps_sig = int( sys.argv[5] )

N_bins = 20


#  ------------------------------------------  import  -----------------------------------------  #

pot = np.zeros(reps_sig) # naive spher ann_naive ann_spher

for r in range(reps_sig):
    
    if 1:#try:
        # ---------- theoretical part ---------- #
    
        filename = "Results/theor_T%.4f_dt%.4f_t%d_h%d_r%d.txt" % (Tfin,Delta_t,tone,harmonic,r)
        bound = np.loadtxt(filename)[1,1]

    
        # ---------- annealed part ---------- #
    
        filename = "Results/SA_T%.4f_dt%.4f_t%d_h%d_K%.4f_r%d.txt" % (Tfin,Delta_t,tone,harmonic,K,r)
        data = np.loadtxt(filename).T
        pot[r] = np.average(data[1]) / bound

    #except:
    #    pot[r] = 2
    #    print('ohibo')


#  ---------------------------------------  histo & save  --------------------------------------  #


goodData = pot
goodData = goodData[goodData<1]


# histogram
histo, bins = np.histogram(goodData, bins=N_bins, density=True)
bins = 0.5 * (bins[1:] + bins[:-1])

filename = "Analysis/phiSA_T%.4f_dt%.4f_t%d_K%.4f_av%d.txt" % (Tfin,Delta_t,tone,K,reps_sig)
np.savetxt(filename, np.stack((bins,histo)).T, header="bins histo")


# resumee
av = np.average(goodData)
low = np.percentile(goodData,20)
high = np.percentile(goodData,80)


with open("Analysis/finalT_dt%.4f_t%d_K%.4f_av%d.txt" % (Delta_t,tone,K,reps_sig), 'a') as f:
    f.write("%f %f %f %f\n" % (Tfin,av,low,high))
    

