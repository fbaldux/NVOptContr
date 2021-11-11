Tfin=152.       # final time of the experiments
delta_t=0.16       # pi-pulse distance
integer N=$((Tfin/delta_t))       # number of spins
echo $N
#N=955

tone=3       # type of signal
harmonic=5       # number of the harmonic for the monochromatic signal
annSteps=1e3       # number of steps in the temperature ramp
MCsteps=1e2       # number of MC steps at each ramp level
T0=0.1       # initial temperature
#K=0.002       # ferromagnetic coupling
Reps=100       # number of states to sample



echo $Tfin $delta_t | python3 compute_J.py &
echo $Tfin $delta_t $tone $harmonic | python3 compute_h.py &
wait
echo "h & J done"


make SA
for K in 0.0005; #1e-4 5e-4 1e-3 5e-3 1e-2;
do
    ./SA $N $tone $harmonic $annSteps $MCsteps $T0 $K $Reps &
    echo "N $N tone $tone harm $harmonic annSteps $annSteps MCsteps $MCsteps T0 $T0 K $K Reps $Reps --> pid $!" >> log.txt
done
wait 
echo "SA done"

    

echo $Tfin $delta_t $tone $harmonic | python3 scatter.py &
