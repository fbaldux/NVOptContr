function mytime() {
    perl -MTime::HiRes=time -e 'printf "%.9f\n", time' 
    #echo "from time import time; print(time())"| python
}

Tfin=160.       # final time of the experiments
Delta_t=0.16       # pi-pulse distance

tone=3       # monochromatic or trichromatic
harmonic=0       # number of the harmonic (only for the monochromatic signal)

annSteps=1e3       # number of steps in the temperature ramp
MCsteps=1e2       # number of MC steps at each ramp level
T0=0.1       # initial temperature
K=0.002       # ferromagnetic coupling
Reps=50       # number of states to sample

time0=$(mytime)

if g++ -o J J_experiment.cpp -lm
then
    ./J $Tfin $Delta_t
    echo "J done" $( echo "$(mytime) - $time0" | bc -l )
fi


if g++ -o h h_experiment.cpp -lm
#if g++ -o h h_random.cpp -lm
then
    ./h $Tfin $Delta_t $tone $harmonic
    echo "h done" $( echo "$(mytime) - $time0" | bc -l )
fi


if g++ -o SA SA.cpp -lm -std=c++11
then
    for K in 0.00010000000000000009 0.00016237767391887224 0.0002636650898730362 0.0004281332398719398 0.0006951927961775608 0.0011288378916846896 0.0018329807108324375 0.0029763514416313187 0.004832930238571755 0.007847599703514618 0.01274274985703134 0.020691380811147905 0.03359818286283785 0.0545559478116852 0.0885866790410083 0.14384498882876626 0.23357214690901223 0.37926901907322474 0.6158482110660267 1.0
    do
        ./SA $Tfin $Delta_t $tone $harmonic $annSteps $MCsteps $T0 $K $Reps &
    done
    wait 
    echo "SA done" $( echo "$(mytime) - $time0" | bc -l )
fi
rm J h SA

python3 Trials/scatter.py $Tfin $Delta_t $tone $harmonic &




