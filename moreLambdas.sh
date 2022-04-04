
Tfin=16.       # final time of the experiments
Delta_t=0.1       # pi-pulse distance

tone=3       # monochromatic or trichromatic
harmonic=0       # number of the harmonic (only for the monochromatic signal)

annSteps=1e3       # number of steps in the temperature ramp
MCsteps=1       # number of MC steps at each ramp level
T0=0.01       # initial temperature
reps_each=1       # number of states to sample


g++ -o J J_experiment.cpp -lm
#g++ -o h h_experiment.cpp -lm
g++ -o h h_random.cpp -lm
g++ -o SA SA_spherical.cpp -lm -std=c++11


#./J $Tfin $Delta_t
#./h $Tfin $Delta_t $tone 0

#for Tfin in $(seq 10 10 10)
for k in {2..2}
do
    #python spherical_2lambda.py $Tfin $Delta_t $tone $harmonic 0
    #python spherical_moreLambdas.py $Tfin $Delta_t $tone $harmonic 0 $k
    
	python spherical_diag.py $Tfin $Delta_t $tone $harmonic 0 
    ./SA $Tfin $Delta_t $tone $harmonic $annSteps $MCsteps $T0 0 $reps_each
	
done

#rm J_experiment h_experiment 
