# OptControl-SimAnneal

Simulated annealing schedule for the optimal control problem of NV centers in diamond.


---
### anneal.sh

This shell runs the codes to

- compute the vectors `h[i]` and `J[i,j]`
- perform many annealing cycles with `SA.cpp`, starting at high temperature from a random state. By default, it uses several values of K (the ferromagnetic coupling) parallelizing to different CPUs.


---
### compute\_h.cpp

The program computes the field h for the spin glass Hamiltonian. The field represents the signal to be detected.  
Currently, the supported options are monochromatic and trichromatic signal (as in the experiments).


---
### compute\_J.cpp

The program computes the couplings J for the spin glass Hamiltonian. The couplings represent the noise to be filtered out.


---
### exact+anneal.sh

This shell runs the codes to

- compute the vectors `h[i]` and `J[i,j]`
- find the exact solution with `spherical.py`
- perform many annealing cycles with `SA_loadInit.cpp`, starting at medium temperature from the spherical solution. Here the value of the ferromagnetic coupling K is inessential (only domain wall moves allowed) so it is set to 0.


---
### SA.cpp

The program anneals a random configuration of Ising spins s[i]=+/-1, according to the cost function

        H = sum_ij J[i,j] s[i] s[j] - log |sum_i h[i] s[i]| - K sum_i s[i] s[i+1]

- The variables J[i,j] and h[i] are loaded from Init/
- The MC moves are only spin flips.
- The energy is computed efficiently at each step.
- The configurations found are saved to Configurations/, with the # of pulses and 1/eta in the header.
- The # of pulses and 1/eta for each configuration are saved to a file in Results/


---
### SA\_loadInit.cpp

The program anneals a random configuration of Ising spins s[i]=+/-1, according to the cost function

        H = sum_ij J[i,j] s[i] s[j] - log |sum_i h[i] s[i]| - K sum_i s[i] s[i+1]

- The variables J[i,j] and h[i] are loaded from Init/
- The initial configuration is given by the output of spherical.py, i.e. the spherical model solution.
- The only allowed MC moves are domain wall shifts.
- The energy is computed efficiently at each step.
- The configurations found are saved to Configurations/, with the # of pulses and 1/eta in the header.
- The # of pulses and 1/eta for each configuration are saved to a file in Results/


---
### scatter.py

Given the final time and tone, the program plots the sensitivities for all the values of K found in Results/


---
### spherical.py

The program finds the configuration of _continuous_ spins `s[i]` that minimezes the cost function
   
      H = sum_ij J[i,j] s[i] s[j] - log |sum_i h[i] s[i]| - lamda ( sum_i s[i]**2 - N )

- The variables `J[i,j]` and `h[i]` are loaded from Init/
- From the continuous spins are generated _Ising_ spins `s_Ising[i] = sign(s[i])`, that are then saved to Configurations/, with the # of pulses and 1/eta in the header.


---
### spherical\_diag.py

The program finds the configuration of _continuous_ spins `s[i]` that minimezes the cost function
   
      H = sum_ij J[i,j] s[i] s[j] - log |sum_i h[i] s[i]| - lamda ( sum_i s[i]**2 - N )

- The variables `J[i,j]` and `h[i]` are loaded from Init/
- Exact diagonalization is used instead of the FFT.
- From the continuous spins are generated _Ising_ spins `s_Ising[i] = sign(s[i])`, that are then saved to Configurations/, with the # of pulses and 1/eta in the header.
















