#include <iostream>
#include <string>
#include <TFile.h>
#include <TTree.h>
#include <TRandom3.h>
#include <TMath.h>

using namespace std;

void usage(){
  cout << "Usage: ./Smearing <input_file> <output_file> <cluster>" << endl;
  cout << "cluster: woody or in2p3" << endl;
}

double counter; 

void ResolutionFunction(
    double energy, 
){
    // Resolution function
    double resolution; // TODO: Implement resolution function

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
    double smeared_energy, smeared_cos_zenith;

    // Smearing
    if (UseResolution)
    {
        // TODO: Implement smearing with resolution
    }
    else
    {
        // Smearing with constant level
        smeared_energy = rand->Gaus(energy, smear_level * energy);

        // Smearing zenith angle
        while (true)
        {
            smeared_cos_zenith = rand->Gaus(cos_zenith, smear_level * cos_zenith);
            counter += 1;
            if (smeared_cos_zenith >= -1 && smeared_cos_zenith <= 1)
            {
                break;
            }
        }
    }


    return make_pair(smeared_energy, smeared_cos_zenith);
}


int main(int argc, char* argv[]){
    cout << "\nStarting Smearing.cc" 
         << "\nRunning code:" 
         << "\nYour input parameters are the following:" << endl;            

    // Check input parameters
    if (argc != 4){
        usage();
        exit(1);
    }

    // Input parameters
    string input_file = argv[1];
    string output_file = argv[2];
    double smeared_level = argv[3];
    bool UseResolution = argv[4];

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
    oldtree->SetBranchAddress("energy_true", &energy_true);
    oldtree->SetBranchAddress("cos_zenith_true", &cos_zenith_true);

    // New branches
    double smeared_energy, smeared_cos_zenith;
    newtree->Branch("energy_smeared", &smeared_energy, "energy_smeared/D");
    newtree->Branch("cos_zenith_smeared", &smeared_cos_zenith, "cos_zenith_smeared/D");


    // Set random seed
    TRandom3 *rand = new TRandom3(0);

    ntot = (Int_t)oldtree->GetEntries();

    // Set counter to 0
    counter = 0;

    // Call Smearing function
    for (unsigned int i = 0; i < ntot; i++){
        oldtree->GetEntry(i);

        pair<double, double> smeared = SmearVariables(energy_true, cos_zenith_true, smeared_level, rand, UseResolution);
        smeared_energy = smeared.first;
        smeared_cos_zenith = smeared.second;

        newtree->Fill();

        if (i % ntot/100 == 0){
            cout << "Processed " << i/ntot * 100 << "% of the data." << endl;
        }
    }

    cout << "Total number of random samplings:" << counter << endl;
    cout << "Additional percentage of random samplings:" << (counter/ntot -1) * 100 << "%" << endl;

    // Write output
    f_out->cd();
    newtree->Write();
    f_out->Close();
    f->Close();

    cout << "||============== Successful execution! ==============||" << endl;
}