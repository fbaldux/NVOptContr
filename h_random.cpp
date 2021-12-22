/*  -------------------------------------------------------------------------------------------  //

    The program extracts randomly the field h for the spin glass Hamiltonian, as the superposition
    of plane waves (`tone` in number) with random amplitudes, frequencies and phases.
    The field represents the signal to be detected.
    The variable `harmonic` is dummy.

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
int N, tone, harmonic;
double Tfin, Delta_t;


//  -------------------------------  functions for the integral  ------------------------------  //

// integrated monochromatic wave
double integ_mono(double A, double omega0, double t, double phi0) {
    //return 0.5/M_PI * A * sin(2*nu0*M_PI*t) / nu0;
    return A * sin(omega0*t+phi0) / omega0;
}



//  ------------------------------------  save output data  -----------------------------------  //

void save_h(double *hs) {
    // create the output file
    char filename[100];
    snprintf(filename, 100, "Init/h_T%.4f_dt%.4f_t%d_h%d.txt", Tfin, Delta_t, tone, harmonic);        
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
        cerr << "\nError! Usage: ./h_random <Tfin> <Delta_t> <tone> <harmonic>\n\n";
        exit(-1);
    }
    Tfin = strtof(argv[1], NULL);
    Delta_t = strtof(argv[2], NULL);
    tone = strtod(argv[3], NULL);    
    harmonic = 0;

    
    // number of spins
    N = int(Tfin / Delta_t);
    
    
    /* check if file already exists
    char filename[100];
    snprintf(filename, 100, "Init/h_T%.4f_dt%.4f_t%d_h%d.txt", Tfin, Delta_t, tone, harmonic); 
    ifstream outfile(filename);
    if (outfile) {
        exit(0);
    }*/ 
    
    
    // dynamic allocation
    double *A = new double[tone]();   
    double *omega = new double[tone]();   
    double *phi = new double[tone]();   
    double *hs = new double[N]();   
    if (hs==NULL || A==NULL || omega==NULL || phi==NULL) {
        cerr << "\nError! Memory allocation failed.\n\n";
        exit(-1);
    }
    
    
    // random signal extraction
    double Atot = 0.;
    for (int t=0; t<tone; t++) {
        A[t] = randomReal(generator)*2-1;
        Atot += A[t]*A[t];
        omega[t] = randomReal(generator) * 2*M_PI;
        phi[t] = randomReal(generator) * 2*M_PI;
    }
    // normalize to 1
    for (int t=0; t<tone; t++) {
        A[t] /= Atot;
    }
    
    
    // integration: it can be done analytically for superposition of plane waves
    for (int t=0; t<tone; t++) {
        for (int k=1; k<=N; k++) {
            hs[k-1] += ( integ_mono(A[t],omega[t],k*Delta_t,phi[t]) - integ_mono(A[t],omega[t],(k-1)*Delta_t,phi[t]) ) / Tfin;
        }
    }
    
    
    // save J to file
    save_h(hs);
    
    // free the memory
    free(hs);
    
    return 0;
}
