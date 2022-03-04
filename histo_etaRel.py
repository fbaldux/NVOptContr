import sys
import numpy as np

Tfin = float( sys.argv[1] )
Delta_t = float( sys.argv[2] )
tone = int( sys.argv[3] )
harmonic = 0
reps_sig = int( sys.argv[4] )

N_bins = 20

##############################################  ETA  ##############################################

#  ------------------------------------------  import  -----------------------------------------  #

pot = np.zeros((4,reps_sig)) # naive spher ann_naive ann_spher

for r in range(reps_sig):
    
    # ---------- theoretical part ---------- #
    
    filename = "Results/theor_T%.4f_dt%.4f_t%d_h%d_r%d.txt" % (Tfin,Delta_t,tone,harmonic,r)
    data = np.loadtxt(filename)[:,1]

    pot[0,r] = data[0]/data[1]  # naive
    pot[1,r] = data[2]/data[1]  # spherical


    # ---------- annealed part ---------- #
    
    filename = "Results/SAnaive_T%.4f_dt%.4f_t%d_h%d_K%.4f_r%d.txt" % (Tfin,Delta_t,tone,harmonic,0,r)
    data2 = np.loadtxt(filename).T
    pot[2,r] = np.average(data2[1]) / data[1]

    filename = "Results/SAspher_T%.4f_dt%.4f_t%d_h%d_K%.4f_r%d.txt" % (Tfin,Delta_t,tone,harmonic,0,r)
    data2 = np.loadtxt(filename).T
    pot[3,r] = np.average(data2[1]) / data[1]



#  ---------------------------------------  histo & save  --------------------------------------  #

title = ["Naive", "Spher", "AnnNaive", "AnnSpher"]

for x in range(4):
    
    goodData = pot[x]
    print(len(goodData[goodData>1]))
    goodData = goodData[goodData<1]
    

    histo, bins = np.histogram(goodData, bins=N_bins, density=True)
    bins = 0.5 * (bins[1:] + bins[:-1])
    
    print(title[x], np.average(goodData))

    filename = "Analysis/etaRel" + title[x] + "_dt%.4f_t%d_av%d.txt" % (Delta_t,tone,reps_sig)
    np.savetxt(filename, np.stack((bins,histo)).T, header="bins histo")
    


