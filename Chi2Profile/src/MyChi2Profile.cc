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
    string detector = "ANTARES";
    string reco = data["user"]["reco"];
    string sys_option = data["user"]["systematics"];
    string cut_option = data["user"]["cut_option"];
    bool smeared = data["user"]["is_smeared"];
    
    cout << "\nParameters: " << endl;
    cout << "====================" << endl;
    cout << "Fitting parameter: " << parname << endl;
    cout << "Number of points: " << npoints << endl;
    cout << "Parameter range: " << parmin << " - " << parmax << endl;
    cout << "Experiment: " << experiment << endl;
    cout << "Type: " << type << endl;
    cout << "Ordering: " << ordering << endl;
    cout << "Detector: " << detector << endl;
    cout << "Reconstruction: " << reco << endl;
    cout << "Systematics: " << sys_option << endl;
    cout << "Cuts: " << cut_option << endl;
    cout << "Smeared: " << smeared << endl;
    cout << "Both octants: " << both_octants << endl;

    string smear_level;
    if (smeared){
        smear_level = data["user"]["smear_level"];
    }

    if (smear_level == "km3net" || smear_level == "antares") {
        cout << "Smearing level: " << smear_level << endl;
    } else {
        cout << "Smearing level: " << smear_level << " percent" << endl;
    }

    string method = "FitTwoOctants"; 
    if (!both_octants) method = "SimpleFit";
    
    double interval;
     if (npoints < 2)
        interval = 0;
    else
        interval = (parmax - parmin)/double(npoints-1);

    string path;
    if (smeared){
        cout << "Fitting smeared data" << endl;
        if (smear_level != "orca6" && smear_level != "antares" && smear_level != "orca115") {    
            path = "output/" + detector + "/"  + cut_option + "/smeared/" + smear_level + "_percent/" + sys_option + "/" +  experiment  + "/" + ordering + "/" + type ;
        } 
        else {
            path = "output/" + detector + "/"  + cut_option + "/smeared/" + smear_level + "/" + sys_option + "/" +  experiment  + "/" + ordering + "/" + type ;
        }
    }
    else { 
        path = "output/" + detector + "/"  + cut_option + "/unsmeared/" + sys_option  + "/" + reco + "/" + experiment  + "/" + ordering + "/" + type ; 
    }
    cout << "Output folder: " << path << endl;

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
            break;
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
    }
}
