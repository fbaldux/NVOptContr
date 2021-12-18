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
double integ_mono(double A, double omega0, double t) {
    return 0.5/M_PI * A * sin(2*omega0*M_PI*t) / omega0;
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
        cerr << "\nError! Usage: ./compute_J <Tfin> <Delta_t> <tone>\n\n";
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
    double *hs = new double[N]();   
    if (hs==NULL || A==NULL || omega==NULL) {
        cerr << "\nError! Memory allocation failed.\n\n";
        exit(-1);
    }
    
    
    // random signal extraction
    double Atot = 0.
    for (int t=0; t<tone; t++) {
        A[t] = randomReal(generator)*2-1;
        Atot += A[t]*A[t];
        omega[t] = randomReal(generator);
    }
    // normalize to 1
    for (int t=0; t<tone; t++) {
        A[t] /= Atot;
    }
    
    
    // integration: it can be done analytically for superposition of plane waves
    for (int t=0; t<tone; t++) {
        for (int k=1; k<=N; k++) {
            hs[k-1] += ( integ_mono(A,omega,k*Delta_t) - integ_mono(A,omega,(k-1)*Delta_t) ) / Tfin;
        }
    }
    
    
    // save J to file
    save_h(hs);
    
    // free the memory
    free(hs);
    
    return 0;
}
