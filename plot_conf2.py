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

#plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 16})
#plt.rcParams["figure.figsize"] = [5,5]
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

s = []
pulses = []
etas = []

stop = False
r = 0
while not stop:
    
    try:
        filename = "Configurations/s_T%.4f_dt%.4f_t%d_h%d_K%.4f_r%d.txt" % (Tfin,Delta_t,tone,harmonic,K,r)
        s.append( np.loadtxt(filename) )
        
        r += 1
        
        # grep eta
        pulse, eta = grep_header(filename)
        pulses.append( pulse )
        etas.append( eta )
       
    except:
        stop = True



filename = "Configurations/sSpher_T%.4f_dt%.4f_t%d_h%d.txt" % (Tfin,Delta_t,tone,harmonic)
s.insert( 0, np.loadtxt(filename) )

# grep eta
pulse, eta = grep_header(filename)
pulses.insert( 0, pulse )
etas.insert( 0, eta )


s = np.array(s)
scal = np.diag(np.ones(r+1))

for i in range(r+1):
    for j in range(i):
        scal[i,j] = np.dot(s[i],s[j]) / N
        scal[j,i] = scal[i,j]

ax.tick_params(axis='y', left='True', right='True')

im = ax.imshow(scal, cmap='inferno', aspect=1)
cbar = ax.figure.colorbar(im, ax=ax, pad=0.12)


labs = [r"Sph."]+[r"SA$_{%d}$"%(i+1) for i in range(r)]
ax.set_xticks(np.arange(r+1), labels=labs)
ax.set_yticks(np.arange(r+1), labels=labs)

ax2 = ax.twinx()
ax2.set_ylim(ax.get_ylim())
ax2.set_yticks(np.arange(r+1), labels=["%.2f"%e for e in etas[::-1]])

ax.text(1.03, 1.05, r"$1/\eta$", transform=ax.transAxes)

#cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

ax.set_title(r"scalar product $\vec{s} \cdot \vec{s}'$")

plt.show()




















