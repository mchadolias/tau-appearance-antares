#include "ParseFitter/ParseFitter.h"
#include "OrcaSim/SimpleSens.h"
#include "TSystem.h"

using namespace std;

int main(int argc, char* argv[]){
    ParseFitter Fitter(argc, argv);
    json data = Fitter.GetJSON();

    int npoints = data["user"]["npoints"];
    bool both_octants = data["user"]["both_octants"];
    double parmax = data["user"]["parmax"];
    double parmin = data["user"]["parmin"];
    string parname = data["user"]["parname"];
    string experiment = data["user"]["experiment"];
    string type = data["user"]["type"];
    string ordering = data["user"]["ordering"];
    string detector = data["variables"]["MClabel"];
    string reco = data["user"]["reco"];
    string path = "output/" + detector + "/" + reco + "/" + experiment  + "/" + ordering + "/" + type ; 
    cout << "Output folder: " << path << endl;

    string method = "FitTwoOctants"; 
    if (!both_octants) method = "SimpleFit";
    
    double interval;
     if (npoints < 2)
        interval = 0;
    else
        interval = (parmax - parmin)/double(npoints-1);

    for(int i=0; i<npoints; i++){

        double testvalue = parmin+interval*i;

        json updatedjson;
        updatedjson["parameters"][parname.c_str()]["vModel"] = testvalue; //You can do this with whatever you need to change

        Fitter.UpdateFit(updatedjson); //Update just the part of the fit that you need

        string outputname = string(path + "/Chi2Profile_"+parname+"_"+ experiment +"_"+ ordering + "_"+ type + "_"+ method); // Save all the fits in the same file

        string outPath_root = outputname + ".root";
        bool FileExists = !gSystem->AccessPathName(outPath_root.c_str());

        if (FileExists && i == 0){
            cout << "File " << outputname << " already exists. Skipping.." << endl;
            continue;
        }
        cout << "Output is written to " << outputname << endl;

        if (both_octants) {
            cout << "Performing FitTwoOctants..." << endl;
            Fitter.FitTwoOctants(); // Get best fit between both octants
        } else {
            cout << "Performing SimpleFit..." << endl;
            Fitter.SimpleFit();
        }

        Fitter.WriteOutput(outputname.c_str()); //This will write two output files, 1 json 1 root

        if (testvalue == 0){
            string outputname_data_hist = string(path + "/histograms_data.root");
            string outputname_model_hist = string(path + "/histograms_model.root");

            TFile outFile_data_hist(outputname_data_hist.c_str(),"recreate");
            cout << "Writing data histogram to: " << outputname_data_hist << endl;
            outFile_data_hist.cd();
            Fitter.expData->WriteExperiment(&outFile_data_hist);
            outFile_data_hist.Close();

            TFile outFile_model_hist(outputname_model_hist.c_str(),"recreate");
            cout << "Writing model histogram to: " << outputname_model_hist << endl;
            outFile_model_hist.cd();
            Fitter.expModel->WriteExperiment(&outFile_model_hist);
            outFile_model_hist.Close();

            string outputname_map_poisson = string(path + "/Chi2Maps_poisson");
            string outputname_map_gauss = string(path + "/Chi2Maps_gauss");
            Fitter.WriteChi2Maps(outputname_map_poisson, false);
            Fitter.WriteChi2Maps(outputname_map_gauss, true);

        }
    }
}
