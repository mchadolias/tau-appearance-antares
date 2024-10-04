#include <iostream>
#include <string>
#include <TFile.h>
#include <TTree.h>
#include <TRandom3.h>
#include <TMath.h>

using namespace std;

void usage(){
  cout << "Usage: ./Smearing <input_file> <output_file> <smear_level> <Resolution> <Assimetric_factor>" << endl;  
}

double counter; 

// Resolution function parameters
class ANTARES{
    public:
        // Resolution function for energy
        double res_en_a = -640.34;
        double res_en_b = -5.88;
        double res_en_c = -20.44;
        double res_en_d = -0.41;

        // Resolution function for zenith angle
        double res_dir_a = -21352.43;
        double res_dir_b = -561954.61;
        double res_dir_c = -556675.55;
        double res_dir_d =  0.09;
};

class ORCA6{
    public:
        double res_en = 0.6;
        double res_dir = 0.2;
};

class ORCA115{
    public:
        double res_en = 0.2;
        double res_dir = 0.1;
};

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
    bool UseResolution = false,
    double Assimetric_factor_en = 1,
    double Assimetric_factor_dir = 1,
    string detector = "ANTARES"
){
    
    // Smearing parameters
    double smeared_energy, smeared_cos_zenith, FWHM_en, FWHM_dir, sigma_dir, sigma_en;

    // Resolution parameters
    if (detector == "ANTARES"){
        
        if (UseResolution){
            ANTARES antares;
            FWHM_en = ResolutionFunction(energy, antares.res_en_a, antares.res_en_b, antares.res_en_c, antares.res_en_d);
            FWHM_dir = ResolutionFunction(cos_zenith, antares.res_dir_a, antares.res_dir_b, antares.res_dir_c, antares.res_dir_d);
        }
        else{
            FWHM_en =  smear_level * energy;
            FWHM_dir =  smear_level * cos_zenith;
        }}
    else if (detector == "ORCA6"){
        ORCA6 orca6;
        FWHM_en = orca6.res_en;
        FWHM_dir = orca6.res_dir;
    }
    else if (detector == "ORCA115"){
        ORCA115 orca115;
        FWHM_en = orca115.res_en;
        FWHM_dir = orca115.res_dir;
    }
    else{
        cout << "Error: Detector not found" << endl;
        exit(1);
    }

    // Assign sigma values
    sigma_en = FWHM_en / (2 * TMath::Sqrt(2 * TMath::Log(2))) * Assimetric_factor_en;
    sigma_dir = FWHM_dir / (2 * TMath::Sqrt(2 * TMath::Log(2))) * Assimetric_factor_dir;

    if (sigma_dir < 0.001)
        sigma_dir = 0.001;

    while (true){
        smeared_energy = rand->Gaus(energy, sigma_en);
        counter += 1;
        if (smeared_energy > 0){
            break;
        }
    }

    while (true){
        smeared_cos_zenith = rand->Gaus(cos_zenith, sigma_dir);
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
    if (argc != 8){
        usage();
        exit(1);
    }

    // Input parameters
    string input_file = argv[1];
    string output_file = argv[2];
    double smeared_level = atof(argv[3]) / 100;
    string Resolution = argv[4];
    string detector = argv[5];
    double Assimetric_factor_en = stod(argv[6]);
    double Assimetric_factor_dir = stod(argv[7]);
    bool UseResolution;

    cout << "\nChecking input parameters:" << endl;
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
    int unique_seed = TRandom3(0).GetSeed();
    TRandom3 *rand = new TRandom3(unique_seed);

    unsigned int ntot = (Int_t)oldtree->GetEntries();

    // Set counter to 0
    counter = 0;

    cout << "\nStarting smearing process..." << endl;
    // Call Smearing function
    for (unsigned int i = 0; i < ntot; i++){
        oldtree->GetEntry(i);

        pair<double, double> smeared = SmearVariables(energy_true, cos_zenith_true, smeared_level,
         rand, UseResolution, Assimetric_factor_en, Assimetric_factor_dir, detector);
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