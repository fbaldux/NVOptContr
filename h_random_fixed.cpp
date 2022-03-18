/*  -------------------------------------------------------------------------------------------  //

    The program computes the field h for the spin glass Hamiltonian. The field represents
    the signal to be detected.      
    The signal is composed of `tone` random frequencies in [0,1] MHz, random phases and random
    amplitudes (that sum to 1).

//  -------------------------------------------------------------------------------------------  */


#include <iostream>
#include <cstdio>
#include <iomanip>
#include <fstream>
#include <cmath>
#include <random>

#define SAVE_SIGNAL

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

void save_signal(double *A, double *omega, double *phi) {
    // create the output file
    char filename[100];
    snprintf(filename, 100, "Init/hData_T%.4f_dt%.4f_t%d_h%d_r%d.txt", Tfin, Delta_t, tone, 0, rep);        
    FILE *outfile = fopen(filename, "w");  
    fprintf(outfile, "# A nu phi\n");
    
    for (int t=0; t<tone; t++) {
        fprintf(outfile, "%f %f %f\n", A[t], 0.5*omega[t]/M_PI, phi[t]);
    }
    
    fclose(outfile);
}


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
    

    double A[7] = {0.142241, 0.102567, 0.164911, 0.174642, 0.214671, 0.06411 , 0.136858};   
    double omega[7] = {0.935326, 0.184713, 0.691916, 0.409031, 0.216931, 0.582142, 0.079503};   
    double phi[7] = {5.90295 , 1.77293 , 1.948228, 0.77013 , 4.60635 , 0.942352, 0.520557};  
     

    for (int i=0; i<7; i++) {
        omega[i] *= 2*M_PI;
    }
    
#ifdef SAVE_SIGNAL
    save_signal(A,omega,phi);
#endif


    // integration: it can be done analytically for superposition of plane waves
    for (int k=0; k<N; k++) {
        for (int t=0; t<tone; t++) {
            hs[k] += ( integ_mono(A[t],omega[t],(k+1)*Delta_t,phi[t]) - integ_mono(A[t],omega[t],k*Delta_t,phi[t]) ) / Tfin;
        }
    }
    
    // save J to file
    save_h(hs);
    
    // free the memory
    free(hs);
    
    return 0;
}
