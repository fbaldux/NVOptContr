import numpy as np
from matplotlib import pyplot as plt
from glob import glob

# input
instring = input("").split(' ')

T = float( instring[0] )
deltat = float( instring[1] )  
tone = int( instring[2] ) 
harmonic = int( instring[3] ) 

L = int(T/deltat)


"""# import required module
import os
# assign directory
directory = 'files'
 
# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(f)"""

for filename in glob("Results/%dtone_%dspins_%dus_K?.????.txt" % (tone,L,T)):
    K = float( filename[-10:-4] )
    
    data = np.loadtxt(filename).T
    plt.plot(data[0], data[1], 'o', ms=2, label="K=%.1e"%K)

plt.xlabel("# of pulses")
plt.ylabel(r"1/$\eta$")

if tone==3:
    plt.title(r"$T=%d \mu$s, trichromatic signal" % T)
elif tone==1:
    plt.title(r"$T=%d \mu$s, monochromatic signal" % T)

plt.legend()
plt.show()