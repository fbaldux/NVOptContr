/*  -------------------------------------------------------------------------------------------  //

    The program computes the field h for the spin glass Hamiltonian. The field represents
    the signal to be detected.
    
    Currently, the supported options are monochromatic and trichromatic signal (as in the experiments).

//  -------------------------------------------------------------------------------------------  */


#include <iostream>
#include <cstdio>
#include <iomanip>
#include <fstream>
#include <cmath>
#include <random>

using namespace std;

// random number generator
random_device seed; // obtain a random number from hardware
mt19937 generator(seed()); // seed the generator (Mersenne twister)
//uniform_int_distribution<> randomBit(0,1);
uniform_real_distribution<> randomReal(0.0,1.0);


// global variables
int N, tone, rep;
double Tfin, Delta_t;


//  -------------------------------  functions for the integral  ------------------------------  //

// integrated monochromatic wave
double integ_mono(double A, double omega0, double t, double phi0) {
    return A * sin(omega0*t+phi0) / omega0;
}


//  ------------------------------------  save output data  -----------------------------------  //

void save_h(double *hs) {
    // create the output file
    char filename[100];
    snprintf(filename, 100, "Init/h_T%.4f_dt%.4f_t%d_h%d_r%d.txt", Tfin, Delta_t, tone, 0, rep);        
    ofstream outfile(filename);
    
    if ( ! outfile.is_open() ) {
        cerr << "\nError with the output file!\n\n" << endl;
        exit(-1);
    }

    outfile << scientific;
    for (int k=0; k<N; k++) {
        outfile << hs[k] << endl;
    }
    
    outfile.close();
}


//  ------------------------------------------  main  -----------------------------------------  //

int main( int argc, char *argv[] ) {
    
    // parameter acquisition
    if( argc != 5 ) {
        cerr << "\nError! Usage: ./h_experiment <Tfin> <Delta_t> <tone> <rep>\n\n";
        exit(-1);
    }
    Tfin = strtof(argv[1], NULL);
    Delta_t = strtof(argv[2], NULL);
    tone = strtod(argv[3], NULL);    
    rep = strtod(argv[4], NULL);
    
    
    // number of spins
    N = int(Tfin / Delta_t);
    
    
    // dynamic allocation
    double *hs = new double[N]();   
    if (hs==NULL) {
        cerr << "\nError! Memory allocation failed.\n\n";
        exit(-1);
    }
    

    double *A = new double[tone]();   
    double *omega = new double[tone]();   
    double *phi = new double[tone]();  
     
    // random signal extraction
    double Atot = 0.;
    for (int t=0; t<tone; t++) {
        A[t] = randomReal(generator);
        Atot += A[t];
        omega[t] = randomReal(generator) * 2*M_PI;
        phi[t] = randomReal(generator) * 2*M_PI;
    }
    // normalize to 1
    for (int t=0; t<tone; t++) {
        A[t] /= Atot;
    }


    // integration: it can be done analytically for superposition of plane waves
    for (int t=0; t<tone; t++) {
        for (int k=0; k<N; k++) {
            hs[k] += ( integ_mono(A[t],omega[t],(k+1)*Delta_t,phi[t]) - integ_mono(A[t],omega[t],k*Delta_t,phi[t]) ) / Tfin;
        }
    }
  
    
    // save J to file
    save_h(hs);
    
    // free the memory
    free(hs);
    
    return 0;
}
