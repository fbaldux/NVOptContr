/*  -------------------------------------------------------------------------------------------  //

    The program computes the field h for the spin glass Hamiltonian. The field represents
    the signal to be detected.      
    The signal is composed of `tone` random frequencies in [0,1] MHz, random phases and random
    amplitudes (that sum to 1).  Such numbers are loaded from Init/hData\_{...}

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


//  ------------------------------  solving issues with rounding  -----------------------------  //

double round(double d) {
    return floor(d+0.5);
}


//  -----------------------------------  load signal specs  -----------------------------------  //

void load_specs(double *A, double *omega, double *phi) {
    char filename[100];
    snprintf(filename, 100, "Init/hData_T%.4f_dt%.4f_t%d_h%d_r%d.txt", 80., Delta_t, tone, 0, rep); 
    ifstream infile(filename);
	
    if ( ! infile.is_open() ) {
        cerr << "\nError! No input file \"" << filename << "\"\n\n\n";
        exit(-1);
    }
    
    // skipping the header
    infile.ignore(1000,'\n');

	// read each row
	for(int t=0; t<tone; t++) {
        // read each column
		infile >> A[t]; 
        infile >> omega[t];
        infile >> phi[t];        
	}
	infile.close();

    
    for (int t=0; t<tone; t++) {
        omega[t] *= 2*M_PI;
    }
}


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
    N = round(Tfin / Delta_t);
    
    
    // dynamic allocation
    double *hs = new double[N]();   
    if (hs==NULL) {
        cerr << "\nError! Memory allocation failed.\n\n";
        exit(-1);
    }
    

    double *A = new double[tone]();   
    double *omega = new double[tone]();   
    double *phi = new double[tone]();  

    load_specs(A,omega,phi);
    
        
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
