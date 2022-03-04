
Tfin=80.       # final time of the experiments
Delta_t=0.16       # pi-pulse distance

tone=7       # monochromatic or trichromatic
harmonic=0       # number of the harmonic (only for the monochromatic signal)

annSteps=1e3       # number of steps in the temperature ramp
MCsteps=1       # number of MC steps at each ramp level
T0=0.01       # initial temperature
reps_sig=1000       # sample size for signals
reps_each=10       # number of states to sample

threads=5
thread_size=$(( $reps_sig / $threads ))

#rm Init/* Results/* Configurations/*

g++ -o h h_random.cpp -lm
g++ -o J J_experiment.cpp -lm
g++ -o SA_spherical SA_spherical.cpp -lm -std=c++11
g++ -o SA_naive SA_naive.cpp -lm -std=c++11

./J $Tfin $Delta_t


for (( R=0; R<$reps_sig; R+=$thread_size ))
do
    (
    for (( r=$R; r<$R+$thread_size; r++ ))
    do
        ./h $Tfin $Delta_t $tone $r
    
        #python spherical_FFT.py $Tfin $Delta_t $tone $harmonic $r
        python spherical_diag.py $Tfin $Delta_t $tone $harmonic $r
    
        ./SA_spherical $Tfin $Delta_t $tone $harmonic $annSteps $MCsteps $T0 $r $reps_each
        ./SA_naive $Tfin $Delta_t $tone $harmonic $annSteps $MCsteps $T0 $r $reps_each
    done
    )&
done
wait

rm J h SA_spherical SA_naive


python histo_eta.py $Tfin $Delta_t $tone $reps_sig
python histo_etaRel.py $Tfin $Delta_t $tone $reps_sig


