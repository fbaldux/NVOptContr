Tfin=160.       # final time of the experiments
Delta_t=0.16       # pi-pulse distance

tone=3       # monochromatic or trichromatic
harmonic=5       # number of the harmonic (only for the monochromatic signal)

annSteps=1e3       # number of steps in the temperature ramp
MCsteps=1       # number of MC steps at each ramp level
T0=0.01       # initial temperature
Reps=10       # number of states to sample

time0=$(date +%s.%N)

if g++ -o compute_J compute_J.cpp -lm
then
    ./compute_J $Tfin $Delta_t
    echo "J done" $( echo "$(date +%s.%N) - $time0" | bc -l )
fi


if g++ -o compute_h compute_h.cpp -lm
then
    ./compute_h $Tfin $Delta_t $tone $harmonic
    echo "h done" $( echo "$(date +%s.%N) - $time0" | bc -l )
fi


python3 spherical.py $Tfin $Delta_t $tone $harmonic && echo "spherical done" $( echo "$(date +%s.%N) - $time0" | bc -l )


if g++ -o SA_loadInit SA_loadInit.cpp -lm
then
    for K in 5e-3; #5e-4 1e-3 5e-3 1e-2;
    do
        ./SA_loadInit $Tfin $Delta_t $tone $harmonic $annSteps $MCsteps $T0 $Reps &
        echo Tf $Tfin, dt $Delta_t, tone $tone, harm $harmonic, annSt $annSteps, MCst $MCsteps, T0 $T0, rep $Reps, pid $! >> log.txt
    done
    wait 
    echo "SA done" $( echo "$(date +%s.%N) - $time0" | bc -l )
fi
#rm compute_J compute_h SA

#python3 scatter.py $Tfin $Delta_t $tone $harmonic &




