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


// global variables
int N, tone, harmonic;
double Tfin, Delta_t;


//  -------------------------------  functions for the integral  ------------------------------  //

// integrated monochromatic wave
double integ_mono(double A, double nu0, double t) {
    return 0.5/M_PI * A * sin(2*nu0*M_PI*t) / nu0;
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
        cerr << "\nError! Usage: ./h_experiment <Tfin> <Delta_t> <tone> <harmonic>\n\n";
        exit(-1);
    }
    Tfin = strtof(argv[1], NULL);
    Delta_t = strtof(argv[2], NULL);
    tone = strtod(argv[3], NULL);    
    harmonic = strtod(argv[4], NULL);    

    // if tritone, set harmonic=0 by default
    if (tone==3)
        harmonic = 0;
    
    // number of spins
    N = int(Tfin / Delta_t);
    
    
    // check if file already exists
    char filename[100];
    snprintf(filename, 100, "Init/h_T%.4f_dt%.4f_t%d_h%d.txt", Tfin, Delta_t, tone, harmonic); 
    ifstream outfile(filename);
    if (outfile) {
        exit(0);
    } 
    
    
    // dynamic allocation
    double *hs = new double[N]();   
    if (hs==NULL) {
        cerr << "\nError! Memory allocation failed.\n\n";
        exit(-1);
    }
    
    
    // integration: it can be done analytically for monochromatic or trichromatic signals
    if (tone==1) {
        double nu0 = 0.4322/(2.*harmonic+1);
        
        for (int k=1; k<=N; k++) {
            hs[k-1] = ( integ_mono(1.,nu0,k*Delta_t) - integ_mono(1.,nu0,(k-1)*Delta_t) ) / Tfin;
        }
    }
    else if (tone==3) {        
        double A0 = 0.065*0.2+1./5; 
        double nu0 = 0.1150;
        double A1 = 0.237*0.2+1./5; 
        double nu1 = 0.2125; 
        double A2 = 0.389*0.2+1./5; 
        double nu2 = 0.1450; 
        
        double B0 = A0/(A0+A1+A2); 
        double B1 = A1/(A0+A1+A2);
        double B2 = A2/(A0+A1+A2);
                
        for (int k=0; k<N; k++) {
            hs[k]  = ( integ_mono(B0,nu0,(k+1)*Delta_t) - integ_mono(B0,nu0,k*Delta_t) ) / Tfin;
            hs[k] += ( integ_mono(B1,nu1,(k+1)*Delta_t) - integ_mono(B1,nu1,k*Delta_t) ) / Tfin;
            hs[k] += ( integ_mono(B2,nu2,(k+1)*Delta_t) - integ_mono(B2,nu2,k*Delta_t) ) / Tfin;
        }
    }
    else {
        cerr << "\nError! Unrecognized tone value.\n\n";
        exit(-1);
    }
    
    // save J to file
    save_h(hs);
    
    // free the memory
    free(hs);
    
    return 0;
}
