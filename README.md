# OptControl-SimAnneal

Simulated annealing schedule for the optimal control problem of NV centers in diamond.


---
### compute\_h.py

The program computes the field h for the spin glass Hamiltonian. The field represents the signal to be detected.

- If the output file already exists, it just quits.
- It distinguishes between
   - 3-chromatic signal (`tone=3`)
   - mono-chromatic signal (`tone=1`), and in this case also the harmonic has to be specified


---
### compute\_J.py

The program computes the couplings J for the spin glass Hamiltonian. The couplings represent the noise to be filtered out.

- If the output file already exists, it just quits.
- If an output file for a larger system exists, it just crops it and saves.
- Otherwise, it computes it from scratch.


---
### run.sh

Shell to run the single instance.


---
### run\_monos.sh

Shell to run the sequence of all monochromatic signals, for the plot with the comparison with CPMG.


---
### SA.cpp

The program anneals a random configuration of Ising spins s[i]=+/-1, according to the cost function
   
   H = sum_ij J[i,j] s[i] s[j] - log |sum_i h[i] s[i]| - K sum_i s[i] s[i+1]

- The variables `J[i,j]` and `h[i]` are loaded from a file.
- The energy is computed efficiently at each step.
- The configurations found are saved to Configurations/, with the # of pulses and 1/eta in the header.
- The # of pulses and 1/eta for each configuration are saved to a file in Results/


---
### scatter.py

Given the final time and tone, the program plots the sensitivities for all the values of K found in Results/


---
### tritone.py

The program copies in Best/ the best configurations found for the 3-chromatic case.
