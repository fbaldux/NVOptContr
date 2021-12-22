function mytime() {
    perl -MTime::HiRes=time -e 'printf "%.9f\n", time' 
    #echo "from time import time; print(time())"| python
}

Tfin=100.       # final time of the experiments
Delta_ts=(0.5 0.2 0.1 0.05 0.02 0.01)       # pi-pulse distance

tone=3       # monochromatic or trichromatic
harmonic=0       # number of the harmonic (only for the monochromatic signal)

annSteps=1e3       # number of steps in the temperature ramp
MCsteps=1       # number of MC steps at each ramp level
T0=0.01       # initial temperature
Reps=10       # number of states to sample

time0=$(mytime)

make J_experiment
make h_experiment
#g++ -o SA_loadInit SA_loadInit.cpp -lm  -std=c++11

for i in {1..6}
do
    Delta_t=$Delta_ts[$i]
        
    ./J_experiment $Tfin $Delta_t
    ./h_experiment $Tfin $Delta_t $tone $harmonic
    
    python3 spherical.py $Tfin $Delta_t $tone $harmonic
    
    #./SA_loadInit $Tfin $Delta_t $tone $harmonic $annSteps $MCsteps $T0 $Reps
    
done

#rm J_experiment h_experiment SA_loadInit





