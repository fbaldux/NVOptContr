
Tfin=16.       # final time of the experiments
Delta_t=0.16       # pi-pulse distance

tone=7       # monochromatic or trichromatic
harmonic=0       # number of the harmonic (only for the monochromatic signal)

annSteps=1e3       # number of steps in the temperature ramp
MCsteps=1       # number of MC steps at each ramp level
T0=0.01       # initial temperature
reps_each=1       # number of states to sample


function mytime() {
    perl -MTime::HiRes=time -e 'printf "%.9f\n", time' 
    #echo "from time import time; print(time())"| python
}


#rm Init/* Results/* Configurations/*

g++ -o J J_experiment.cpp -lm
g++ -o h h_random.cpp -lm
#g++ -o h h_random_load.cpp -lm
g++ -o SA SA_spherical.cpp -lm -std=c++11


time0=$(mytime)
function mytime_elap() {
    echo "$(mytime) - $time0" | bc -l
}

./J $Tfin $Delta_t
#echo "J done" $(mytime_elap)

for r in {22..22}
do

    #./h $Tfin $Delta_t $tone $harmonic
    ./h $Tfin $Delta_t $tone $r
    #echo "h done" $(mytime_elap)

    python3 spherical_diag.py $Tfin $Delta_t $tone $harmonic $r
    #echo "spherical done" $(mytime_elap)

    ./SA $Tfin $Delta_t $tone $harmonic $annSteps $MCsteps $T0 $r $reps_each
    #echo "SA done" $(mytime_elap)
done

rm J h SA





