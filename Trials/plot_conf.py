#  ---------------------------------------------------------------------------------------------  #
#   
#   ...
#
#  ---------------------------------------------------------------------------------------------  #


import sys
import numpy as np
from matplotlib import pyplot as plt


Tfin = float( sys.argv[1] )
Delta_t = float( sys.argv[2] )
tone = int( sys.argv[3] )
harmonic = int( sys.argv[4] )
K = float( sys.argv[5] )


N = int( Tfin / Delta_t )


if tone == 3:
    harmonic = 0
elif tone != 1:
    sys.stderr.write("\nError! Unrecognized tone value.\n\n")
    exit(-1)

plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 16})
fig, ax = plt.subplots()

#  ------------------------------------------  import  -----------------------------------------  #

def grep_header(filename):
    f = open(filename, 'r')
    line = f.readline()
    f.close()
    
    # EXAMPLE: pulses=44, 1/eta=93.7581
    start = line.find("=") + 1
    end = line.find(",")
    pulse = int(line[start:end])
    
    start = line.find("=",end) + 1
    eta = float(line[start:-1])
    
    return pulse, eta

pulses = []
etas = []

stop = False
r = 0
while not stop:
    
    try:
        filename = "Configurations/s_T%.4f_dt%.4f_t%d_h%d_K%.4f_r%d.txt" % (Tfin,Delta_t,tone,harmonic,K,r)
        s = np.loadtxt(filename)
        
        s_nz = np.nonzero(np.diff(s))[0]
        ax.plot(s_nz, (r+1)*np.ones(len(s_nz)), 'o', c='black', ms=4)
        
        r += 1
        
        # grep eta
        pulse, eta = grep_header(filename)
        pulses.append( pulse )
        etas.append( eta )
       
    except:
        stop = True



filename = "Configurations/sSpher_T%.4f_dt%.4f_t%d_h%d.txt" % (Tfin,Delta_t,tone,harmonic)
s = np.loadtxt(filename)

s_nz = np.nonzero(np.diff(s))[0]
ax.plot(s_nz, np.zeros(len(s_nz)), 'o', c='firebrick', ms=4)

# grep eta
pulse, eta = grep_header(filename)
pulses.insert( 0, pulse )
etas.insert( 0, eta )

ax.set_xlabel(r"$i$")
ax.set_yticks(np.arange(r+1), labels=[r"spher."]+[r"SA$_{%d}$"%(i+1) for i in range(r)])

ax2 = ax.twinx()
ax2.set_yticks(np.arange(r+1)+0.5, labels=["%.2f"%e for e in etas])

ax.text(1.03, 1.05, r"$1/\eta$", transform=ax.transAxes)

plt.show()




















