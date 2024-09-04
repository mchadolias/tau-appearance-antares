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
    string sys_option = data["user"]["sys_option"];

    string method = "FitTwoOctants"; 
    if (!both_octants) method = "SimpleFit";
    
    double interval;
     if (npoints < 2)
        interval = 0;
    else
        interval = (parmax - parmin)/double(npoints-1);

    string path = "output/" + detector + "/" + sys_option  + "/" + reco + "/" + experiment  + "/" + ordering + "/" + type ; 
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
