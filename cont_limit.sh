tone=3       # monochromatic or trichromatic
harmonic=0       # number of the harmonic (only for the monochromatic signal)

make J_experiment
make h_experiment

for (( Tfin=10.; Tfin<50.; Tfin+=10. )) 
do
    echo "# dt E E_Ising 1/eta 1/eta_Ising"  > Results/cont_T$Tfin.txt
    
    for N in $(seq 100 100 1000)
    do
        Delta_t=$(( $Tfin/$N ))
        
        ./J_experiment $Tfin $Delta_t
        ./h_experiment $Tfin $Delta_t $tone $harmonic
        
        python3 spherical_FFT.py $Tfin $Delta_t $tone $harmonic >> Results/cont_T$Tfin.txt
    done
    
    echo "$Tfin done"
done
rm J_experiment h_experiment





