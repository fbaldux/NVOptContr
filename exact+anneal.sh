function mytime() {
    perl -MTime::HiRes=time -e 'printf "%.9f\n", time' 
    #echo "from time import time; print(time())"| python
}

Tfin=100.       # final time of the experiments
Delta_t=0.16       # pi-pulse distance

tone=3       # monochromatic or trichromatic
harmonic=0       # number of the harmonic (only for the monochromatic signal)

annSteps=1e3       # number of steps in the temperature ramp
MCsteps=1       # number of MC steps at each ramp level
T0=0.01       # initial temperature
Reps=10       # number of states to sample

time0=$(mytime)

#rm Init/* Results/* Configurations/*

if g++ -o J J_experiment.cpp -lm
then
    #./J $Tfin $Delta_t
    echo "J done" $( echo "$(mytime) - $time0" | bc -l )
fi


#if g++ -o h h_experiment.cpp -lm
if g++ -o h h_mio.cpp -lm
then
    #./h $Tfin $Delta_t $tone $harmonic
    echo "h done" $( echo "$(mytime) - $time0" | bc -l )
fi


python3 spherical_FFT.py $Tfin $Delta_t $tone $harmonic && echo "spherical done" $( echo "$(mytime) - $time0" | bc -l )


if g++ -o SA_spherical SA_spherical.cpp -lm -std=c++11
then
    ./SA_spherical $Tfin $Delta_t $tone $harmonic $annSteps $MCsteps $T0 $Reps &
    #echo Tf $Tfin, dt $Delta_t, tone $tone, harm $harmonic, annSt $annSteps, MCst $MCsteps, T0 $T0, rep $Reps, pid $! >> log.txt
    wait
    
    echo "SA done" $( echo "$(mytime) - $time0" | bc -l )
fi
rm J h SA_spherical





