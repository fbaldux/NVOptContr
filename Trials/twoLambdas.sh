
Tfin=16.       # final time of the experiments
Delta_t=0.16       # pi-pulse distance

tone=3       # monochromatic or trichromatic
harmonic=0       # number of the harmonic (only for the monochromatic signal)

annSteps=1e3       # number of steps in the temperature ramp
MCsteps=1       # number of MC steps at each ramp level
T0=0.01       # initial temperature
Reps=1       # number of states to sample


g++ -o J_experiment J_experiment.cpp -lm
g++ -o h_experiment h_experiment.cpp -lm
   
   



for Tfin in $(seq 10 10 200)
do
    ./J_experiment $Tfin $Delta_t
    ./h_experiment $Tfin $Delta_t $tone $harmonic
    python spherical_FFT.py $Tfin $Delta_t $tone $harmonic

    python spherical_2lambda.py $Tfin $Delta_t $tone $harmonic
done

#rm J_experiment h_experiment 
