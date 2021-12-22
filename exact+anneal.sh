function mytime() {
    perl -MTime::HiRes=time -e 'printf "%.9f\n", time' 
    #echo "from time import time; print(time())"| python
}

Tfin=160.       # final time of the experiments
Delta_t=0.16       # pi-pulse distance

tone=3       # monochromatic or trichromatic
harmonic=5       # number of the harmonic (only for the monochromatic signal)

annSteps=1e3       # number of steps in the temperature ramp
MCsteps=1       # number of MC steps at each ramp level
T0=0.01       # initial temperature
Reps=1       # number of states to sample

time0=$(mytime)

if g++ -o J_experiment J_experiment.cpp -lm
then
    ./J_experiment $Tfin $Delta_t
    echo "J done" $( echo "$(mytime) - $time0" | bc -l )
fi


if g++ -o h_experiment h_experiment.cpp -lm
then
    ./h_experiment $Tfin $Delta_t $tone $harmonic
    echo "h done" $( echo "$(mytime) - $time0" | bc -l )
fi


python3 spherical_FFT.py $Tfin $Delta_t $tone $harmonic && echo "spherical done" $( echo "$(mytime) - $time0" | bc -l )


if g++ -o SA_from_spherical SA_from_spherical.cpp -lm -std=c++11
then
    ./SA_from_spherical $Tfin $Delta_t $tone $harmonic $annSteps $MCsteps $T0 $Reps &
    #echo Tf $Tfin, dt $Delta_t, tone $tone, harm $harmonic, annSt $annSteps, MCst $MCsteps, T0 $T0, rep $Reps, pid $! >> log.txt
    wait
    
    echo "SA done" $( echo "$(mytime) - $time0" | bc -l )
fi
rm J_experiment h_experiment SA_from_spherical

#python3 scatter.py $Tfin $Delta_t $tone $harmonic &




