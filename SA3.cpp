/*  -------------------------------------------------------------------------------------------  //

    The program anneals a random configuration of Ising spins s[i]=+/-1, according to the 
    cost function

        H = sum_ij J[i,j] s[i] s[j] - log |sum_i h[i] s[i]| - K sum_i s[i] s[i+1]

    - The variables J[i,j] and h[i] are loaded from Init/
    - The energy is computed efficiently at each step.
    - The configurations found are saved to Configurations/, with the # of pulses and 1/eta
      in the header.
    - The # of pulses and 1/eta for each configuration are saved to a file in Results/
    – LOAD SPHERICAL AND DO JUST DOMAIN WALL MOVES
    
//  -------------------------------------------------------------------------------------------  */


#include <iostream>
#include <cstdio>
#include <iomanip>
#include <fstream>
#include <cmath>
#include <random>
#include <vector>

using namespace std;

// random number generator
random_device seed; // obtain a random number from hardware
mt19937 generator(seed()); // seed the generator (Mersenne twister)
uniform_int_distribution<> randomBit(0,1);
uniform_real_distribution<> randomReal(0.0,1.0);

// struct definition
struct EStruct {
  double J;
  double h;
  double K;
  double tot;
};

// fixed variables
#define lambda 1.       // for the exponential temperature ramp
#define gyro 28025      // to compute eta

// global variables
int N, tone, harmonic, ann_steps, MC_steps, MC_ramp_step; 
double Tfin, Delta_t, T0, K0;
double *Js, *hs;


//  ------------------------------------  load h, J and s  ------------------------------------  //

void load_J() {
    char filename[100];
    snprintf(filename, 100, "Init/J_T%.4f_dt%.4f.txt", Tfin, Delta_t);            
    ifstream infile(filename);
        
    if ( ! infile.is_open() ) {
        cerr << "\nError! No input file.\n\n" << endl;
        exit(-1);
    }
    
    // skipping the header
    //infile.ignore(1000,'\n');
    
    int i=0;
    double Ji;
    while (infile >> Ji) {
        Js[i++] = Ji;
    }
    
    infile.close();
}


void load_h() {
    char filename[100];
    snprintf(filename, 100, "Init/h_T%.4f_dt%.4f_t%d_h%d.txt", Tfin, Delta_t, tone, harmonic);        
    ifstream infile(filename);
    
    if ( ! infile.is_open() ) {
        cerr << "\nError! No input file.\n\n" << endl;
        exit(-1);
    }
    
    // skipping the header
    //infile.ignore(1000,'\n');
    
    int i=0;
    double hi;
    while (infile >> hi) {
        hs[i++] = hi;
    }

    infile.close();
}


void load_s(int *s) {
    char filename[100];
    snprintf(filename, 100, "Configurations/sSpher_T%.4f_dt%.4f_t%d_h%d.txt", Tfin, Delta_t, tone, harmonic);         
    ifstream infile(filename);
    
    if ( ! infile.is_open() ) {
        cerr << "\nError! No input file.\n\n" << endl;
        exit(-1);
    }
    
    // skipping the header
    infile.ignore(1000,'\n');
    
    int i=0;
    double si;
    while (infile >> si) {
        s[i++] = si;
    }

    infile.close();
}


//  -----------------------------------  copy configuration  ----------------------------------  //
// copies s1 into s2
void copy_s(int *s1, int *s2) {
    for (int i=0; i<N; i++)
        s2[i] = s1[i];
}


//  -------------------------------------  cost function  -------------------------------------  //

EStruct energy(int *s){
    EStruct E;
    E.J=0.; E.h=0.; E.K=0.;
    
    for (int i=0; i<N; i++) {
        E.h += hs[i]*s[i];
        
        for (int j=0; j<i; j++) {
            E.J += 2.*Js[abs(i-j)]*s[i]*s[j];
        }
    }
    // also the diagonal term matters
    E.J += Js[0]*N;
    
    for (int i=1; i<N; i++) {
        E.K += K0*s[i-1]*s[i];
    }

    E.tot = E.J - log(abs(E.h)) - E.K;
  
    return E;
} 


EStruct new_energy(int *s, int flip, EStruct E){
    EStruct E_new = E;
    
    // h term
    E_new.h -= 2*hs[flip]*s[flip];
    
    // J term
    for (int i=0; i<flip; i++)
        E_new.J -= 4*Js[flip-i]*s[i]*s[flip];
    for (int i=flip+1; i<N; i++){
        E_new.J -= 4*Js[i-flip]*s[i]*s[flip];
    }
    
    // K term
    if (flip>0) {
        if (flip<N-1)
            E_new.K -= 2*K0*s[flip]*(s[flip-1]+s[flip+1]);
        else
            E_new.K -= 2*K0*s[flip]*s[flip-1];
    }
    else
        E_new.K -= 2*K0*s[flip]*s[flip+1];
    
    E_new.tot = E_new.J - log(abs(E_new.h)) - E_new.K;

    return E_new;
} 


//  ------------------------------------  temperature ramp  -----------------------------------  //

double temperature(int n) {
    // exponential ramp
    //return T0*exp(-lambda*(double)n/ann_steps);
    
    // power-law ramp
    //return T0*(1.-(double)n/ann_steps);
    //return T0*(1.-(double)n/ann_steps)*(1.-(double)n/ann_steps);
    //return T0**(1.-(double)n/ann_steps)*(1.-(double)n/ann_steps)*(1.-(double)n/ann_steps);
    //return T0**(1.-(double)n/ann_steps)*(1.-(double)n/ann_steps)*(1.-(double)n/ann_steps)*(1.-(double)n/ann_steps);

    // inverse-power-law ramp
    return T0/(1.+lambda * n * T0);

    // from arXiv:2102.00182
    //return max( 0.5/asinh(tan(0.5*M_PI*n/ann_steps)), 0.);
}


//  ---------------------------------  acceptance probability  --------------------------------  //

double acceptance_prob(double deltaE, double T) {
    if (deltaE<0.)
        return 1.;
    else
        return exp(-deltaE/T);
}


//  ------------------------------------  annealing cycle  ------------------------------------  //

void anneal(int *s, int *best_s, EStruct *E){
    // initial energy
    *E = energy(s);
    double best_E = E->tot;
    
    cout << E->tot << endl;
    
    
    // find the domain walls
    vector<int> DW;
    for (int i=0; i<N-1; i++) {
        if (s[i] == -s[i+1]) {
            DW.push_back(i);
        }
    }
    
    // gradually decrease the temperature
    for (int n=ann_steps/2; n<ann_steps; n++) {
        
        double T = temperature(n);
        
        // move around the domain walls
        for (int t=0; t<MC_steps; t++) {
    
            // pick a domain wall
            int DW_ind = randomReal(generator)*DW.size();
            int flip = DW.at(DW_ind);
        
            // choose to move it left (0) or right (1)
            int direction = randomBit(generator);
            flip += direction;
        
            // find the new energy       
            EStruct E_new = new_energy(s, flip, *E);
    
            // assess the move
            double coin = randomReal(generator);
            if (coin<acceptance_prob(E_new.tot-E->tot,0)) {
                s[flip] = -s[flip];
                *E = E_new;
                DW.at(DW_ind) += 2*direction-1;
            }
        
            cout << E->tot << endl;
    
            // keep track of the best configuration so far
            if (E->tot < best_E) {
                best_E = E->tot;
                copy_s(s, best_s);
            }
        }
    }
    
    *E = energy(best_s);   
}


//  ---------------------------------  analyze configuration  ---------------------------------  //

// count the domain walls
int domain_walls(int *s) {
    int count=0;
    for (int i=1; i<N; i++)
        count += s[i]*s[i-1];
    
    return (N-count-1)/2;
}


// sensitivity
double etaInv(double epsilon) {
    return 1./exp(epsilon - log(gyro)-0.5*log(N*Delta_t*1e-6));
}


//  ------------------------------------  save output data  -----------------------------------  //

void save_s(int *s, int dw, double this_etaInv, int r) {
    // create the output file
    char filename[100];
    snprintf(filename, 100, "Configurations/s_T%.4f_dt%.4f_t%d_h%d_K%.4f_r%d.txt", Tfin, Delta_t, tone, harmonic, K0, r);        
    ofstream outfile(filename);
    
    if ( ! outfile.is_open() ) {
        cerr << "\nError with the output file!\n\n" << endl;
        exit(-1);
    }

    // write the header
    outfile << "# pulses=" << dw << ", 1/eta=" << this_etaInv << endl;
    // write the rest
    for (int i=0; i<N; i++) {
        outfile << s[i] << endl;
    }
    
    outfile.close();
}


//  ------------------------------------------  main  -----------------------------------------  //

int main( int argc, char *argv[] ) {
    int Reps, *s, *best_s;
    EStruct E;
    
    // parameter acquisition
    if( argc != 10 ) {
        cerr << "\nError! Usage: ./SA <Tfin> <Delta_t> <tone> <harmonic> <ann_steps> <MC_steps> <Temp0> <K> <Reps>\n\n";
        exit(-1);
    }
    Tfin = strtof(argv[1], NULL);
    Delta_t = strtof(argv[2], NULL);
    tone = strtod(argv[3], NULL);
    harmonic = strtod(argv[4], NULL);
    ann_steps = strtod(argv[5], NULL);
    MC_steps = strtod(argv[6], NULL);
    T0 = strtof(argv[7], NULL);
    K0 = strtof(argv[8], NULL);
    Reps = strtod(argv[9], NULL);
    
    // if tritone, set harmonic=0 by default
    if ( tone == 3 )
        harmonic = 0;
    else if ( tone != 1 ) {
        cerr << "\nError! Unrecognized tone value.\n\n";
        exit(-1);
    }
    
    // number of spins
    N = int(Tfin / Delta_t);
       
    // dynamic allocation
    Js = new double[N]();
    hs = new double[N]();
    s = new int[N]();
    best_s = new int[N]();
    
    if (Js==NULL || hs==NULL || s==NULL|| best_s==NULL) {
        cerr << "\nError! Memory allocation failed.\n\n";
        exit(-1);
    }
    
    // load J and h
    load_J();
    load_h();
        
 
    // create the output file
    char filename[100];
    snprintf(filename, 100, "Results/T%.4f_dt%.4f_t%d_h%d_K%.4f.txt", Tfin, Delta_t, tone, harmonic, K0);        
    FILE *outfile = fopen(filename, "w");  
    fprintf(outfile, "# N=%d, MC_steps=%d, T0=%f, K=%f\n# pulses 1/eta\n", N, MC_steps, T0, K0);
    
    
    // perform many annealing cycles
    for (int r=0; r<Reps; r++) {
        // initial state from spherical model solution
        load_s(s);
        
        // anneal the state s to best_s
        anneal(s, best_s, &E);
        
        // save data
        int dw = domain_walls(best_s);
        double this_etaInv = etaInv(E.tot+E.K);
        fprintf(outfile, "%d %e\n", dw, this_etaInv);
        // save configuration to file
        save_s(best_s, dw, this_etaInv, r);
        
        fflush(0);
    }
    
    // close the files 
    fclose(outfile);
    
    
    // free the memory
    free(Js);
    free(hs);
    free(s);
    free(best_s);
    
    return 0;
}