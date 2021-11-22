/*  -------------------------------------------------------------------------------------------  //

    The program computes the field h for the spin glass Hamiltonian. The field represents
    the signal to be detected.
    
//  -------------------------------------------------------------------------------------------  */


#include <iostream>
#include <cstdio>
#include <iomanip>
#include <fstream>
#include <cmath>

using namespace std;


// global variables
int N, harmonic;
double Tfin, Delta_t;


//  -------------------------------  functions for the integral  ------------------------------  //

// monochromatic case
double integrated_signal(double t) {
    double omega0 = 0.4322/(2.*harmonic+1); 
    
    return 0.5/M_PI * sin(2*omega0*M_PI*t) / omega0;
}



//  ------------------------------------  save output data  -----------------------------------  //

void save_h(double *hs) {
    // create the output file
    char filename[100];
    snprintf(filename, 100, "Init/h_T%.4f_dt%.4f_h%d.txt", Tfin, Delta_t, harmonic);        
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
    if( argc != 4 ) {
        cerr << "\nError! Usage: ./compute_J <Tfin> <Delta_t> <harmonic>\n\n";
        exit(-1);
    }
    Tfin = strtof(argv[1], NULL);
    Delta_t = strtof(argv[2], NULL);
    harmonic = strtod(argv[3], NULL);    
    
    // number of spins
    N = int(Tfin / Delta_t);
    
    
    // dynamic allocation
    double *hs = new double[N]();   
    if (hs==NULL) {
        cerr << "\nError! Memory allocation failed.\n\n";
        exit(-1);
    }
    
    
    // integration: it can be done analytically for monochromatic signals
    for (int k=1; k<=N; k++) {
        hs[k-1] = ( integrated_signal(k*Delta_t) - integrated_signal((k-1)*Delta_t) ) / Tfin;
    }
    
    
    // save J to file
    save_h(hs);
    
    // free the memory
    free(hs);
    
    return 0;
}
