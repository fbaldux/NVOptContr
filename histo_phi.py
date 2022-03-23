#  ---------------------------------------------------------------------------------------------  #
#   
#   The program saves to Analysis/phi{...} the histogram of `phi = eta\_bound / eta`, from the SA 
#   optimization of the gCP and spherical model sequences.  
#   It also saves to Analysis/finalT\_{...} the averages as a function of the total sensing time.
#
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np

Tfin = float( sys.argv[1] )
Delta_t = float( sys.argv[2] )
tone = int( sys.argv[3] )
harmonic = 0
reps_sig = int( sys.argv[4] )

N_bins = 20

#  ------------------------------------------  import  -----------------------------------------  #

pot = np.zeros((4,reps_sig)) # gCP spher ann_gCP ann_spher

for r in range(reps_sig):
    
    try:
        # ---------- theoretical part ---------- #
    
        filename = "Results/theor_T%.4f_dt%.4f_t%d_h%d_r%d.txt" % (Tfin,Delta_t,tone,harmonic,r)
        data = np.loadtxt(filename)[:,1]

        pot[0,r] = data[0]/data[1]  # gCP
        pot[1,r] = data[2]/data[1]  # spherical


        # ---------- annealed part ---------- #
    
        filename = "Results/SAGCP_T%.4f_dt%.4f_t%d_h%d_r%d.txt" % (Tfin,Delta_t,tone,harmonic,r)
        data2 = np.loadtxt(filename).T
        pot[2,r] = np.average(data2[1]) / data[1]

        filename = "Results/SAspher_T%.4f_dt%.4f_t%d_h%d_r%d.txt" % (Tfin,Delta_t,tone,harmonic,r)
        data2 = np.loadtxt(filename).T
        pot[3,r] = np.average(data2[1]) / data[1]

    except:
        pot[:,r] = 2


#  ---------------------------------------  histo & save  --------------------------------------  #

title = ["GCP", "Spher", "GCPAnn", "SpherAnn"]

avs = np.zeros(4)
lows = np.zeros(4)
highs = np.zeros(4)

for x in range(4):
    
    goodData = pot[x]
    goodData = goodData[goodData<1]

    
    # histogram
    histo, bins = np.histogram(goodData, bins=N_bins, density=True)
    bins = 0.5 * (bins[1:] + bins[:-1])
    
    filename = "Analysis/phi" + title[x] + "_T%.4f_dt%.4f_t%d_av%d.txt" % (Tfin,Delta_t,tone,reps_sig)
    np.savetxt(filename, np.stack((bins,histo)).T, header="bins histo")
    
    
    # resumee
    avs[x] = np.average(goodData)
    lows[x] = np.percentile(goodData,20)
    highs[x] = np.percentile(goodData,80)
    

    
with open("Analysis/finalT_dt%.4f_t%d_av%d.txt" % (Delta_t,tone,reps_sig), 'a') as f:
    f.write("%f " % Tfin)
    f.write("%f %f %f "  % (avs[0],lows[0],highs[0])) # gCP 
    f.write("%f %f %f "  % (avs[1],lows[1],highs[1])) # spher 
    f.write("%f %f %f "  % (avs[2],lows[2],highs[2])) # ann_gCP
    f.write("%f %f %f\n" % (avs[3],lows[3],highs[3])) # ann_spher
   

