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

pot = np.zeros((5,reps_sig)) # naive bound spher ann_naive ann_spher

for r in range(reps_sig):
    
    # ---------- theoretical part ---------- #
    
    filename = "Results/theor_T%.4f_dt%.4f_t%d_h%d_r%d.txt" % (Tfin,Delta_t,tone,harmonic,r)
    data = np.loadtxt(filename)[:,1]

    pot[0,r] = data[0]  # naive
    pot[1,r] = data[1]  # bound
    pot[2,r] = data[2]  # spherical


    # ---------- annealed part ---------- #
    
    filename = "Results/SAnaive_T%.4f_dt%.4f_t%d_h%d_K%.4f_r%d.txt" % (Tfin,Delta_t,tone,harmonic,0,r)
    data = np.loadtxt(filename).T
    pot[3,r] = np.average(data[1])

    filename = "Results/SAspher_T%.4f_dt%.4f_t%d_h%d_K%.4f_r%d.txt" % (Tfin,Delta_t,tone,harmonic,0,r)
    data = np.loadtxt(filename).T
    pot[4,r] = np.average(data[1])


#  ---------------------------------------  histo & save  --------------------------------------  #

title = ["Naive", "Bound", "Spher", "AnnNaive", "AnnSpher"]

for x in range(5):

    histo, bins = np.histogram(pot[x], bins=N_bins, density=True)
    bins = 0.5 * (bins[1:] + bins[:-1])


    filename = "Analysis/eta" + title[x] + "_dt%.4f_t%d_av%d.txt" % (Delta_t,tone,reps_sig)
    np.savetxt(filename, np.stack((bins,histo)).T, header="bins histo")



