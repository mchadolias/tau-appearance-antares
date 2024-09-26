#include <iostream>
#include <string>
#include <TFile.h>
#include <TTree.h>
#include <TRandom3.h>
#include <TMath.h>

using namespace std;

void usage(){
  cout << "Usage: ./Smearing <input_file> <output_file> <smear_level> <Resolution>" << endl;  
}

double counter; 

// Resolution function
// Resolution function for energy
const double res_en_a = -640.34; // Resolution parameter a 
const double res_en_b = -5.88; // Resolution parameter b
const double res_en_c = -20.44; // Resolution parameter c
const double res_en_d = -0.41; // Resolution parameter d

// Resolution function for zenith angle
const double res_dir_a = -21352.43; // Resolution parameter a
const double res_dir_b = -561954.61; // Resolution parameter b
const double res_dir_c = -556675.55; // Resolution parameter c
const double res_dir_d =  0.09; // Resolution parameter d

double ResolutionFunction(
    double param,
    double a,
    double b,
    double c,
    double d
){
    // Resolution function
    double resolution = a / ( b * param + c ) + d;

    return resolution;
}

pair<double, double> SmearVariables(
    double energy, 
    double cos_zenith,
    double smear_level,
    TRandom3 *rand,
    bool UseResolution = false
){
    
    // Smearing parameters
    double smeared_energy, smeared_cos_zenith, FWHM_en, FWHM_dir;

    if (UseResolution){
        FWHM_en = ResolutionFunction(energy, res_en_a, res_en_b, res_en_c, res_en_d) * energy;
        FWHM_dir = ResolutionFunction(cos_zenith, res_dir_a, res_dir_b, res_dir_c, res_dir_d) * cos_zenith; 
    }
    else{
        FWHM_en = smear_level * energy;
        FWHM_dir = abs(smear_level * cos_zenith);
    }

    while (true){
        smeared_energy = rand->Gaus(energy, FWHM_en / 2.355);
        counter += 1;
        if (smeared_energy > 0){
            break;
        }
    }

    while (true){
        smeared_cos_zenith = rand->Gaus(cos_zenith, FWHM_dir / 2.355);
        counter += 1;
        if (smeared_cos_zenith >= -1 && smeared_cos_zenith <= 1){
            break;
        }
    }

    return make_pair(smeared_energy, smeared_cos_zenith);
}


int main(int argc, char* argv[]){
    cout << "\nStarting Smearing.cc" 
         << "\nRunning code:" 
         << "\nYour input parameters are the following:" << endl;            

    // Check input parameters
    if (argc != 5){
        usage();
        exit(1);
    }

    // Input parameters
    string input_file = argv[1];
    string output_file = argv[2];
    double smeared_level = atof(argv[3]) / 100;
    string Resolution = argv[4];
    bool UseResolution;

    for (int i = 1; i < argc; i++){
        cout << "argv[" << i << "] = " << argv[i] << endl;
    }

    cout << "\nChecking smearing strategy: " <<  endl;
    if (Resolution == "Y"){
        cout << "Using resolution function" << endl;
        UseResolution = true;
    }
    else if (Resolution == "N"){
        cout << "Using constant level" << endl;
        UseResolution = false;
    }
    else{
        cout << "Error: UseResolution must be Y or N" << endl;
        exit(1);
    }

    // Read input file
    TFile *f = new TFile(input_file.c_str(), "READ");
    TTree *oldtree = (TTree*)f->Get("sel");

    if (!f || f->IsZombie()){
        cerr << "Error: Could not open the input ROOT file." << endl;
        exit(1);
    }

    // Output file
    TFile *f_out = new TFile(output_file.c_str(), "RECREATE");
    TTree *newtree = oldtree->CloneTree(0, "fast");

    // Variables
    double energy_true, cos_zenith_true;

    // Branches from old tree
    oldtree->SetBranchAddress("energy_recoTrue", &energy_true);
    oldtree->SetBranchAddress("cos_zenith_recoTrue", &cos_zenith_true);

    // New branches
    double smeared_energy, smeared_cos_zenith;
    newtree->Branch("energy_smeared", &smeared_energy, "energy_smeared/D");
    newtree->Branch("cos_zenith_smeared", &smeared_cos_zenith, "cos_zenith_smeared/D");


    // Set random seed
    TRandom3 *rand = new TRandom3(0);

    unsigned int ntot = (Int_t)oldtree->GetEntries();

    // Set counter to 0
    counter = 0;

    cout << "\nStarting smearing process..." << endl;
    // Call Smearing function
    for (unsigned int i = 0; i < ntot; i++){
        oldtree->GetEntry(i);

        pair<double, double> smeared = SmearVariables(energy_true, cos_zenith_true, smeared_level, rand, UseResolution);
        smeared_energy = smeared.first;
        smeared_cos_zenith = smeared.second;

        newtree->Fill();

        if (i % (ntot/100) == 0){
            cout << "Processed " << i << " events out of " << ntot << endl;
        }
    }

    cout << "\nTotal number of random samplings:" << counter << endl;
    cout << "Additional percentage of random samplings:" << (counter/ntot -1) * 100 << "%" << endl;

    // Write output
    f_out->cd();
    newtree->Write();
    f_out->Close();
    f->Close();

    cout << "\n||============== Successful execution! ==============||" << endl;
}