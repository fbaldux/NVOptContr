Tfin=56       # final time of the experiments
delta_t=0.16       # pi-pulse distance
integer N=$((T/delta_t))       # number of spins

tone=3       # type of signal
harmonic=0       # number of the harmonic for the monochromatic signal

annSteps=1e3       # number of steps in the temperature ramp
MCsteps=1e2       # number of MC steps at each ramp level
T0=0.1       # initial temperature
#K=0.002       # ferromagnetic coupling
Reps=10       # number of states to sample

if make SA;
then
    
    for K in 5e-4 2e-4 1e-4;
    do
        ./SA $N $tone $harmonic $annSteps $MCsteps $T0 $K $Reps &
        echo "N $N tone $tone harm $harmonic annSteps $annSteps MCsteps $MCsteps T0 $T0 K $K Reps $Reps --> pid $!" >> log.txt
        #wait
    done
fi