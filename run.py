import numpy as np
from os import system

delta_t = 0.16

annSteps = 1e3
MCsteps = 1e2
T0 = 0.1

K = 0.01
Reps = 1000


#  -----------------------------------------  tritone  -----------------------------------------  #

Tfins = [ 56.,  80., 104., 128., 152., 176., 200., 224., 248., 272., 296., 320., 344., 368., 392.] # µs

for Tfin in Tfins:
    # comput the Js
    system("echo %f %f | python3 compute_J.py" % (Tfin, delta_t))
    
    # compute the hs
    system("echo %f %f %d %d | python3 compute_h.py" % (Tfin, delta_t, 3, 0))
    
    # run the simulated annealing
    L = int(Tfin/delta_t)
    system('if make SA; then echo "%d %d %d %d %d %f %e %d"; fi' % (N,3,0,annSteps,MCsteps,T0,K,Reps))
    




#  ----------------------------------------  monochrome  ---------------------------------------  #
