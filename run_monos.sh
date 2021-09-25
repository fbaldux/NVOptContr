#typeset -a Tfins
#typeset -a harmonics
Tfins=(20.8 40.48 100 101.76 219.84 266.08 323.84 340.16 392)  # final time of the experiments
delta_t=0.16       # pi-pulse distance

tone=1       # type of signal
harmonics=(1 2 5 5 9 11 17 24 34)       # number of the harmonic for the monochromatic signal
annSteps=1e3       # number of steps in the temperature ramp
MCsteps=1e2       # number of MC steps at each ramp level
T0=0.1       # initial temperature
#K=0.002       # ferromagnetic coupling
Reps=10       # number of states to sample


for i in $(seq 1 $#Tfins);
do
    Tfin=$Tfins[$i]
    harmonic=$harmonics[$i]
    integer N=$((Tfin/delta_t))       # number of spins
    
    echo $Tfin $delta_t | python3 compute_J.py &
    echo $Tfin $delta_t $tone $harmonic | python3 compute_h.py &
    wait
    echo "h & J done"

    make SA
    for K in 1e-4 5e-4 1e-3 5e-3 1e-2;
    do
        ./SA $N $tone $harmonic $annSteps $MCsteps $T0 $K $Reps &
        echo "N $N tone $tone harm $harmonic annSteps $annSteps MCsteps $MCsteps T0 $T0 K $K Reps $Reps --> pid $!" >> log.txt
    done
    wait 
    echo "SA done"
    
    echo $Tfin $delta_t $tone $harmonic | python3 scatter.py 

done