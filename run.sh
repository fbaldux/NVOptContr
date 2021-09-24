N=625       # number of spins
tone=3       # type of signal
annSteps=1e3       # number of steps in the temperature ramp
MCsteps=1e2       # number of MC steps at each ramp level
T0=0.1       # initial temperature
#K=0.002       # ferromagnetic coupling
Reps=100       # number of states to sample

if make SA;
then
    
    #for K in 0.05 0.02 0.01 0.005 0.002 0.001;
    for K in 0.0005 0.0002 0.0001;
    do
        ./SA $N $tone $annSteps $MCsteps $T0 $K $Reps &
        echo "$N $tone $annSteps $MCsteps $T0 $K $Reps --> pid $!" >> log.txt
        #wait
    done
fi