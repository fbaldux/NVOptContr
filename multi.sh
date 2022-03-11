
Delta_t=0.1       # pi-pulse distance

tone=7       # monochromatic or trichromatic
harmonic=0       # number of the harmonic (only for the monochromatic signal)

reps_sig=1000       # sample size for signals

# guided SA
annSteps=1e3       # number of steps in the temperature ramp
MCsteps=1       # number of MC steps at each ramp level
T0=0.01       # initial temperature
reps_each=10       # number of states to sample

# "vanilla" SA
annSteps_VSA=1e3       # number of steps in the temperature ramp
MCsteps_VSA=1e2       # number of MC steps at each ramp level
T0_VSA=0.1       # initial temperature
reps_each_VSA=100       # number of states to sample


Ks=(0.0001 0.0002 0.0003 0.0005 0.0008 0.0013 0.0022 0.0036 0.0060 0.0100)

threads=1
thread_size=$(( $reps_sig / $threads ))

#rm Init/* Results/* Configurations/*

g++ -o h h_random.cpp -lm -std=c++11
g++ -o J J_larger.cpp -lm -std=c++11
g++ -o SA_spherical SA_spherical.cpp -lm -std=c++11
g++ -o SA_GCP SA_GCP.cpp -lm -std=c++11
g++ -o SA SA.cpp -lm -std=c++11


for Tfin in $(seq 10 10 120)
do
    (
    # compute J
    ./J $Tfin $Delta_t 1>>log 2>>err

    for (( r=0; r<$reps_sig; r++ ))
    do
        if [[ ! -f stop ]]
        then
            # extract h
            ./h $Tfin $Delta_t $tone $r 1>>log 2>>err
            
            # exact solution
            python spherical_diag.py $Tfin $Delta_t $tone $harmonic $r 1>>log 2>>err

            # annealing from exact solution 
            ./SA_spherical $Tfin $Delta_t $tone $harmonic $annSteps $MCsteps $T0 $r $reps_each 1>>log 2>>err
            ./SA_GCP $Tfin $Delta_t $tone $harmonic $annSteps $MCsteps $T0 $r $reps_each 1>>log 2>>err
            
            # annealing from infinite temperature
            for K in ${Ks[@]}
            do
                ./SA $Tfin $Delta_t $tone $harmonic $annSteps_VSA $MCsteps_VSA $T0_VSA $K $r $reps_each_VSA 1>>log 2>>err   
            done
        fi
    done

    # save histograms
    python histo_phi.py $Tfin $Delta_t $tone $reps_sig 1>>log 2>>err
    
    for K in ${Ks[@]}
    do
        python histo_phi_vanilla.py $Tfin $Delta_t $tone $K $reps_sig 1>>log 2>>err
    done
    
    )&
done

wait

