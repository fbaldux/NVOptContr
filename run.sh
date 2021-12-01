Tfin=160.       # final time of the experiments
Delta_t=0.16       # pi-pulse distance
#integer N=$((Tfin/delta_t))       # number of spins
#echo $N
#N=955

tone=3       # monochromatic or trichromatic
harmonic=5       # number of the harmonic (only for the monochromatic signal)

annSteps=1e3       # number of steps in the temperature ramp
MCsteps=5e2       # number of MC steps at each ramp level
T0=0.1       # initial temperature
#K=0.002       # ferromagnetic coupling
Reps=10       # number of states to sample


if g++ -o compute_J compute_J.cpp -lm
then
    ./compute_J $Tfin $Delta_t
    echo "J done"
fi


if g++ -o compute_h compute_h.cpp -lm
then
    ./compute_h $Tfin $Delta_t $tone $harmonic
    echo "h done"    
fi


if g++ -o SA SA.cpp -lm
then
    for K in 5e-4 1e-3 5e-3 1e-2;
    do
        ./SA $Tfin $Delta_t $tone $harmonic $annSteps $MCsteps $T0 $K $Reps &
        echo "N $N tone $tone harm $harmonic annSteps $annSteps MCsteps $MCsteps T0 $T0 K $K Reps $Reps --> pid $!" >> log.txt
    done
    wait 
    echo "SA done"  
fi
    

#echo $Tfin $delta_t $tone $harmonic | python3 scatter.py &
