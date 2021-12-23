function mytime() {
    perl -MTime::HiRes=time -e 'printf "%.9f\n", time' 
    #echo "from time import time; print(time())"| python
}

Tfin=160.       # final time of the experiments
#Delta_ts=(0.5 0.2 0.1 0.05 0.02 0.01)       # pi-pulse distance
Delta_ts=(1.6 0.963855421686747 0.5755395683453237 0.3448275862068966 0.20671834625322996 0.12393493415956623 0.07428040854224698 0.044531032563317564 0.02669336002669336 0.016)
tone=3       # monochromatic or trichromatic
harmonic=0       # number of the harmonic (only for the monochromatic signal)

annSteps=0       # number of steps in the temperature ramp
MCsteps=1       # number of MC steps at each ramp level
T0=0.01       # initial temperature
Reps=1       # number of states to sample

time0=$(mytime)

make J_experiment
make h_experiment
g++ -o SA SA_from_spherical.cpp -lm  -std=c++11

for i in {1..10}
do
    Delta_t=$Delta_ts[$i]
        
    ./J_experiment $Tfin $Delta_t
    ./h_experiment $Tfin $Delta_t $tone $harmonic
    
    python3 spherical_FFT.py $Tfin $Delta_t $tone $harmonic
    
    #./SA $Tfin $Delta_t $tone $harmonic $annSteps $MCsteps $T0 $Reps
    
done

rm J_experiment h_experiment SA





