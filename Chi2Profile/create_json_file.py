import json 
import os
from itertools import product
import numpy as np
import argparse

text_conversion = {
    "STD": "Std",
    "TAU": "Tau",
}

reco_info = {"MC" : {"energy": "energy_recoTrue", "zenith": "cos_zenith_recoTrue", "biy": "bjorken_y_recoTrue"},
             "AAFit_dedx" : {"energy": "energy_aafit_dEdX_CEA", "zenith": "aafit_cos_zenith", "biy": "aafit_bjy"},
             "AAFit_ann" : {"energy": "energy_aafit_ANN_ECAP", "zenith": "aafit_cos_zenith", "biy": "aafit_bjy"},
             "NNFit_full" : {"energy": "NNFitShower_Energy", "zenith": "NNFitShower_cos_zenith", "biy":"NNFit_Bjorken_y"},
             "NNFit_dir": {"energy": "energy_recoTrue", "zenith": "NNFitShower_cos_zenith", "biy":"NNFit_Bjorken_y"},
             "Smeared": {"energy": "energy_smeared", "zenith": "cos_zenith_smeared", "biy": "bjorken_y_recoTrue"},
            }

def ArgumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", type=str,
                        help="Choose the channel to probe. STD corresponds to Std and TAU corresponds to Tau") 
    parser.add_argument("--reco", type=str,
                        help="Choose the reconstruction algorithm used to reconstruct the events. \
                        Options: MC, AAFit_dedx, AAFit_ann, NNFit_full, NNFit_dir")
    parser.add_argument("--order", type=str,   
                        help="Choose the mass ordering. Options: NO, IO")
    parser.add_argument("--systematics", type=str,
                        help="Choose the systematics option. Options: 0 for no systematics, 1 for systematics")
    parser.add_argument("--cut", type=str, default="muon_free",
                        help="Choose the cut to be applied")
    parser.add_argument("--smear_level", type=str,
                        help="Choose the smear level to be applied")
    parser.add_argument("--assym_energy", type=str, default="1.0",
                        help="Choose the asymmetry energy to be applied")
    parser.add_argument("--assym_direction", type=str, default="1.0",
                        help="Choose the asymmetry direction to be applied")
    return parser.parse_args()
    
def create_json_User(
    reco: str,
    order: str,
    channel: str,
    systematics: str,
    json_path: str,
    cut: str,
    npoints: int,
    smear_level: str,
):
    # Create the base directory
    for ff in ("fixed", "free"):
        if ff == 'fixed':
            npoints = npoints
            parmin = 0.0
            parmax = 2.0
        elif ff == 'free':
            npoints = 1
            parmin = 0.5
            parmax = 0.5
        
        json_file = {
            "user": {
                "parname": "TauNorm",
                "npoints": npoints,
                "parmin": parmin,
                "parmax": parmax,
                "type": ff,
                "ordering": order,
                "experiment": channel,
                "reco": reco,
                "both_octants": True,
                "systematics": systematics,
                "cut_option": cut,
            }
        }

        if (reco == "Smeared"):
          json_file["user"]["is_smeared"] = True
          json_file["user"]["smear_level"] = smear_level

          # Check if file already exists
          if os.path.exists(os.path.join(json_path, f'USER/User_{reco}_{smear_level}_{channel}_{order}_{cut}_{systematics}_{ff}.json')):
              print(f"File already exists: User_{reco}_{smear_level}_{channel}_{order}_{cut}_{systematics}_{ff}.json")
          else:
              with open(os.path.join(json_path, f'USER/User_{reco}_{smear_level}_{channel}_{order}_{cut}_{systematics}_{ff}.json'), 'w') as f:
                  json.dump(json_file, f, indent=4)
                  print(f"Created file: User_{reco}_{smear_level}_{channel}_{order}_{cut}_{systematics}_{ff}.json")
        
        else:
          json_file["user"]["is_smeared"] = False
          json_file["user"]["smear_level"] = 0

          # Check if file already exists
          if os.path.exists(os.path.join(json_path, f'USER/User_{reco}_{channel}_{order}_{cut}_{systematics}_{ff}.json')):
              print(f"File already exists: User_{reco}_{channel}_{order}_{cut}_{systematics}_{ff}.json")
          else:
              with open(os.path.join(json_path, f'USER/User_{reco}_{channel}_{order}_{cut}_{systematics}_{ff}.json'), 'w') as f:
                  json.dump(json_file, f, indent=4)
                  print(f"Created file: User_{reco}_{channel}_{order}_{cut}_{systematics}_{ff}.json")
        
def create_json_variables(
    channel: str,
    json_path: str,
    smear_level: str,
    asymetric_factor_direction: str = "1.0",
    asymetric_factor_energy: str = "1.0",
):    
        if (smear_level == "0"):
          json_file = {
              "variables": {
                  "MClabel": "ANTARES",
                  "SelectedEvents_filename": [
                      "antares_w_nnfit_FINAL1.root"
                  ],
                  "exposure_nyears": 12.433,
                  "output_path": "output",
                  "flux_path": "flux/Honda2014_frj-solmin-aa_ORCA6_hist.root",
                  "by_path": "xsection/dummy_by_ORCA6.root",
                  "crossfile_InteractingEvents_path": "xsection/xsection_gsg_v5r1_SWIM.root",
                  "crossfile_RespMatrix_path": "xsection/xsection_gsg_v5r1_SWIM.root",
                  "PREMTable": "prem_default.txt",
                  "ExtensiveOutput": True,
                  "EnableMCError": True,
                  "UseW2Method": True,
                  "PlotEffMass": False,
                  "Verbose": False,
                  "SetMuons": False,
                  "EnableSmearMachine": False,
                  "Analysis_Type": "Asimov",
                  "Experiment_Type": text_conversion[channel],
                  "PseudoExperiment_seed": 11,
                  "SetBootstrap": False,
                  "Bootstrap_seed": 1,
                  "Bootstrap_Fraction": 1
              }
          }

          # Check if file already exists
          if os.path.exists(os.path.join(json_path, f'ANTARES/variables_ANTARES_{channel}.json')):
              print(f"File already exists: variables_ANTARES_{channel}.json")
          else:
              with open(os.path.join(json_path, f'ANTARES/variables_ANTARES_{channel}.json'), 'w') as f:
                  json.dump(json_file, f, indent=4)
                  print(f"Created file: variables_ANTARES_{channel}.json")
        elif((smear_level == "antares") & (asymetric_factor_direction != "1.0")):
            json_file = {
              "variables": {
                  "MClabel": f"ANTARES_Smeared_{smear_level}_{asymetric_factor_direction}_{asymetric_factor_energy}",
                  "SelectedEvents_filename": [
                      f"antares_smeared_{smear_level}_{asymetric_factor_direction}_{asymetric_factor_energy}.root"
                  ],
                  "exposure_nyears": 12.433,
                  "output_path": "output",
                  "flux_path": "flux/Honda2014_frj-solmin-aa_ORCA6_hist.root",
                  "by_path": "xsection/dummy_by_ORCA6.root",
                  "crossfile_InteractingEvents_path": "xsection/xsection_gsg_v5r1_SWIM.root",
                  "crossfile_RespMatrix_path": "xsection/xsection_gsg_v5r1_SWIM.root",
                  "PREMTable": "prem_default.txt",
                  "ExtensiveOutput": True,
                  "EnableMCError": True,
                  "UseW2Method": True,
                  "PlotEffMass": False,
                  "Verbose": False,
                  "SetMuons": False,
                  "EnableSmearMachine": False,
                  "Analysis_Type": "Asimov",
                  "Experiment_Type": text_conversion[channel],
                  "PseudoExperiment_seed": 11,
                  "SetBootstrap": False,
                  "Bootstrap_seed": 1,
                  "Bootstrap_Fraction": 1
              }
            }
          
            # Check if file already exists
            if os.path.exists(os.path.join(json_path, f'ANTARES/variables_ANTARES_{channel}_Smeared_{smear_level}_{asymetric_factor_direction}_{asymetric_factor_energy}.json')):
                print(f"File already exists: variables_ANTARES_{channel}_Smeared_{smear_level}_{asymetric_factor_direction}_{asymetric_factor_energy}.json")
            else:
                with open(os.path.join(json_path, f'ANTARES/variables_ANTARES_{channel}_Smeared_{smear_level}_{asymetric_factor_direction}_{asymetric_factor_energy}.json'), 'w') as f:
                    json.dump(json_file, f, indent=4)
                    print(f"Created file: variables_ANTARES_{channel}_Smeared_{smear_level}_{asymetric_factor_direction}_{asymetric_factor_energy}.json")
        else:
            json_file = {
              "variables": {
                  "MClabel": f"ANTARES_Smeared_{smear_level}",
                  "SelectedEvents_filename": [
                      f"antares_smeared_{smear_level}.root"
                  ],
                  "exposure_nyears": 12.433,
                  "output_path": "output",
                  "flux_path": "flux/Honda2014_frj-solmin-aa_ORCA6_hist.root",
                  "by_path": "xsection/dummy_by_ORCA6.root",
                  "crossfile_InteractingEvents_path": "xsection/xsection_gsg_v5r1_SWIM.root",
                  "crossfile_RespMatrix_path": "xsection/xsection_gsg_v5r1_SWIM.root",
                  "PREMTable": "prem_default.txt",
                  "ExtensiveOutput": True,
                  "EnableMCError": True,
                  "UseW2Method": True,
                  "PlotEffMass": False,
                  "Verbose": False,
                  "SetMuons": False,
                  "EnableSmearMachine": False,
                  "Analysis_Type": "Asimov",
                  "Experiment_Type": text_conversion[channel],
                  "PseudoExperiment_seed": 11,
                  "SetBootstrap": False,
                  "Bootstrap_seed": 1,
                  "Bootstrap_Fraction": 1
              }
            }

            # Check if file already exists
            if os.path.exists(os.path.join(json_path, f'ANTARES/variables_ANTARES_{channel}_Smeared_{smear_level}.json')):
                print(f"File already exists: variables_ANTARES_{channel}_Smeared_{smear_level}.json")
            else:
                with open(os.path.join(json_path, f'ANTARES/variables_ANTARES_{channel}_Smeared_{smear_level}.json'), 'w') as f:
                    json.dump(json_file, f, indent=4)
                    print(f"Created file: variables_ANTARES_{channel}_Smeared_{smear_level}.json")


def create_json_classes(
    json_path: str,
    reco: str,
    cut: str,
    smear_level: str,
):    
    if (cut == "muon_free"):
        selection = "cos_zenith_recoTrue < 0"
    elif (cut == "is_nnfit"):
        selection = "NNFitShower_cos_zenith < 0"
    elif (cut == "is_aafit"):
        selection = "(aafit_flag == 1) && (cos_zenith_recoTrue < 0)"
    elif (cut == "hard_cut"):
        selection = "(cos_zenith_recoTrue < -0.4) && (bbfit_flag == 1)"

    json_file = {
    "classes": [
    {
      "name": "tracks",
      "general_cut": f"((abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && ({selection})",
      "muon_loose_cut": f"((abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && ({selection})",
      "reconstructions": { 
          "E": f"{reco_info[reco]['energy']}",
          "cosT": f"{reco_info[reco]['zenith']}",
          "By": f"{reco_info[reco]['biy']}"
        },
      "ClassNorm": "TrackNorm"
    },
    {    
      "name": "showers",
      "general_cut": f"(!(abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && ({selection})",
      "muon_loose_cut": f"(!(abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && ({selection})",
      "reconstructions": {
          "E": f"{reco_info[reco]['energy']}",
          "cosT": f"{reco_info[reco]['zenith']}",
          "By": f"{reco_info[reco]['biy']}"
        },
      "ClassNorm": "ShowerNorm"
    }]}

    if ((reco == "NNFit_full")):
        json_file["classes"][0]["reconstructions"]["E"] = "NNFitTrack_Energy"
        json_file["classes"][0]["reconstructions"]["cosT"] = "NNFitTrack_cos_zenith"
    elif ((reco == "NNFit_dir")):
        json_file["classes"][0]["reconstructions"]["cosT"] = "NNFitTrack_cos_zenith"
      
        
    if (reco == "Smeared"):
      #Check if file already exists
      if os.path.exists(os.path.join(json_path, f'ANTARES/classes_ANTARES_{cut}_{reco}_{smear_level}.json')):
          print(f"File already exists: classes_ANTARES_{cut}_{reco}_{smear_level}.json")
      else:
          with open(os.path.join(json_path, f'ANTARES/classes_ANTARES_{cut}_{reco}_{smear_level}.json'), 'w') as f:
              json.dump(json_file, f, indent=4)
              print(f"Created file: classes_ANTARES_{cut}_{reco}_{smear_level}.json")
    else:
      # Check if file already exists
      if os.path.exists(os.path.join(json_path, f'ANTARES/classes_ANTARES_{cut}_{reco}.json')):
          print(f"File already exists: classes_ANTARES_{reco}.json")
      else:
          with open(os.path.join(json_path, f'ANTARES/classes_ANTARES_{cut}_{reco}.json'), 'w') as f:
              json.dump(json_file, f, indent=4)
              print(f"Created file: classes_ANTARES_{cut}_{reco}.json")    
    
def create_json_params(
    json_path: str,
    order: str,
    systematics: str,
):
    create_param_template(json_path, order)
    for ff in ("fixed", "free"):
        # Read the template file
        with open(os.path.join(json_path, f'PARAMETERS/params_template_{order}.json'), 'r') as f:
            json_file = json.load(f)
        
        # Update the file
        if ff == 'fixed':
            json_file["parameters"]["TauNorm"]["fixed"] = True
        elif ff == 'free':
            json_file["parameters"]["TauNorm"]["fixed"] = False
            
        if systematics == 'systematics':
            json_file["parameters"]["Dm31"]["fixed"] = False
            json_file["parameters"]["Theta23"]["fixed"] = False
            json_file["parameters"]["EnergyScale"]["fixed"] = False
            json_file["parameters"]["ZenithSlope"]["fixed"] = False
            json_file["parameters"]["EnergySlope"]["fixed"] = False
            json_file["parameters"]["NumuNumubarSkew"]["fixed"] = False
            json_file["parameters"]["NueNuebarSkew"]["fixed"] = False
            json_file["parameters"]["NumuNueSkew"]["fixed"] = False
            json_file["parameters"]["NCscale"]["fixed"] = False
            json_file["parameters"]["MuonNorm"]["fixed"] = False
            json_file["parameters"]["TrackNorm"]["fixed"] = False
            json_file["parameters"]["ShowerNorm"]["fixed"] = False
        
        # Check if file already exists
        if os.path.exists(os.path.join(json_path, f'PARAMETERS/parameters_Data_NO_Model_{order}_{systematics}_{ff}.json')):
            print(f"File already exists: parameters_Data_NO_Model_{order}_{systematics}_{ff}.json")
        else:
            with open(os.path.join(json_path, f'PARAMETERS/parameters_Data_NO_Model_{order}_{systematics}_{ff}.json'), 'w') as f:
                json.dump(json_file, f, indent=4)
                print(f"Created file: parameters_Data_NO_Model_{order}_{systematics}_{ff}.json")

def create_param_template(
    json_path: str,
    order: str,
):
    if order == "NO":
        json_file = {
                    "parameters": {
                      "Dm21": {
                        "vData": 7.42e-05,
                        "vModel": 7.42e-05,
                        "fixed": True,
                        "prior": False,
                        "prior_mean": 7.42e-05,
                        "prior_sigma": 2.1e-06
                      },
                      "Dm31": {
                        "vData": 2.517e-03,
                        "vModel": 2.517e-03,
                        "fixed": True,
                        "prior": False,
                        "prior_mean": 2.517e-03,
                        "prior_sigma": 2.1e-05
                      },
                      "DeltaCP": {
                        "vData": 197.0,
                        "vModel": 197.0,
                        "fixed": True,
                        "prior": False,
                        "prior_mean": 197.0,
                        "prior_sigma": 27.0
                      },
                      "Theta13": {
                        "vData": 8.57,
                        "vModel": 8.57,
                        "fixed": True,
                        "prior": True,
                        "prior_mean": 8.57,
                        "prior_sigma": 0.12
                      },
                      "Theta12": {
                        "vData": 33.44,
                        "vModel": 33.44,
                        "fixed": True,
                        "prior": False,
                        "prior_mean": 33.44,
                        "prior_sigma": 0.77
                      },
                      "Theta23": {
                        "vData": 49.2,
                        "vModel": 49.2,
                        "fixed": True,
                        "prior": False,
                        "prior_mean": 49.2,
                        "prior_sigma": 2.0
                      },
                      "EnergyScale": {
                        "vData": 1.0,
                        "vModel": 1.0,
                        "fixed": True,
                        "prior": True,
                        "prior_mean": 1.0,
                        "prior_sigma": 0.05
                      },
                      "ZenithSlope": {
                        "vData": 0.0,
                        "vModel": 0.0,
                        "fixed": True,
                        "prior": True,
                        "prior_mean": 0.0,
                        "prior_sigma": 0.07
                      },
                      "EnergySlope": {
                        "vData": 0.0,
                        "vModel": 0.0,
                        "fixed": True,
                        "prior": True,
                        "prior_mean": 0.0,
                        "prior_sigma": 0.3
                      },
                      "NumuNumubarSkew": {
                        "vData": 0.0,
                        "vModel": 0.0,
                        "fixed": True,
                        "prior": True,
                        "prior_mean": 0.0,
                        "prior_sigma": 0.1
                      },
                      "NueNuebarSkew": {
                        "vData": 0.0,
                        "vModel": 0.0,
                        "fixed": True,
                        "prior": True,
                        "prior_mean": 0.0,
                        "prior_sigma": 0.1
                      },
                      "NumuNueSkew": {
                        "vData": 0.0,
                        "vModel": 0.0,
                        "fixed": True,
                        "prior": True,
                        "prior_mean": 0.0,
                        "prior_sigma": 0.03
                      },
                      "NCscale": {
                        "vData": 1.0,
                        "vModel": 1.0,
                        "fixed": True,
                        "prior": True,
                        "prior_mean": 1.0,
                        "prior_sigma": 0.1
                      },
                      "TauNorm": {
                        "vData": 1.0,
                        "vModel": 1.0,
                        "fixed": True,
                        "prior": True,
                        "prior_mean": 1.0,
                        "prior_sigma": 0.2
                      },
                      "MuonNorm": {
                        "vData": 1.0,
                        "vModel": 1.0,
                        "fixed": True,
                        "prior": False,
                        "prior_mean": 1.0,
                        "prior_sigma": 0.05
                      },
                      "TrackNorm": {
                        "vData": 1.0,
                        "vModel": 1.0,
                        "fixed": True,
                        "prior": False,
                        "prior_mean": 1.0,
                        "prior_sigma": 0.1
                      },
                      "ShowerNorm": {
                        "vData": 1.0,
                        "vModel": 1.0,
                        "fixed": True,
                        "prior": False,
                        "prior_mean": 1.0,
                        "prior_sigma": 0.1
                      }
                    }
                  }
    elif order == "IO":
         json_file = {
                    "parameters": {
                        "Dm21": {
                          "vData": 7.42e-05,
                          "vModel": 7.42e-05,
                          "fixed": True,
                          "prior": False,
                          "prior_mean": 7.42e-05,
                          "prior_sigma": 2.1e-06
                        },
                        "Dm31": {
                          "vData": 2.517e-03,
                          "vModel": -2.4238e-03,
                          "fixed": True,
                          "prior": False,
                          "prior_mean": -2.4238e-03,
                          "prior_sigma": 2.1e-05
                        },
                        "DeltaCP": {
                          "vData": 197.0,
                          "vModel": 282.0,
                          "fixed": True,
                          "prior": False,
                          "prior_mean": 282.0,
                          "prior_sigma": 27.0
                        },
                        "Theta13": {
                          "vData": 8.57,
                          "vModel": 8.60,
                          "fixed": True,
                          "prior": True,
                          "prior_mean": 8.60,
                          "prior_sigma": 0.12
                        },
                        "Theta12": {
                          "vData": 33.44,
                          "vModel": 33.45,
                          "fixed": True,
                          "prior": False,
                          "prior_mean": 33.45,
                          "prior_sigma": 0.77
                        },
                        "Theta23": {
                          "vData": 49.2,
                          "vModel": 49.3,
                          "fixed": False,
                          "prior": False,
                          "prior_mean": 49.3,
                          "prior_sigma": 2.0
                        },
                        "EnergyScale": {
                          "vData": 1.0,
                          "vModel": 1.0,
                          "fixed": True,
                          "prior": True,
                          "prior_mean": 1.0,
                          "prior_sigma": 0.05
                        },
                        "ZenithSlope": {
                          "vData": 0.0,
                          "vModel": 0.0,
                          "fixed": True,
                          "prior": True,
                          "prior_mean": 0.0,
                          "prior_sigma": 0.07
                        },
                        "EnergySlope": {
                          "vData": 0.0,
                          "vModel": 0.0,
                          "fixed": True,
                          "prior": True,
                          "prior_mean": 0.0,
                          "prior_sigma": 0.3
                        },
                        "NumuNumubarSkew": {
                          "vData": 0.0,
                          "vModel": 0.0,
                          "fixed": True,
                          "prior": True,
                          "prior_mean": 0.0,
                          "prior_sigma": 0.1
                        },
                        "NueNuebarSkew": {
                          "vData": 0.0,
                          "vModel": 0.0,
                          "fixed": True,
                          "prior": True,
                          "prior_mean": 0.0,
                          "prior_sigma": 0.1
                        },
                        "NumuNueSkew": {
                          "vData": 0.0,
                          "vModel": 0.0,
                          "fixed": True,
                          "prior": True,
                          "prior_mean": 0.0,
                          "prior_sigma": 0.03
                        },
                        "NCscale": {
                          "vData": 1.0,
                          "vModel": 1.0,
                          "fixed": True,
                          "prior": True,
                          "prior_mean": 1.0,
                          "prior_sigma": 0.1
                        },
                        "TauNorm": {
                          "vData": 1.0,
                          "vModel": 1.0,
                          "fixed": True,
                          "prior": True,
                          "prior_mean": 1.0,
                          "prior_sigma": 0.2
                        },
                        "MuonNorm": {
                          "vData": 1.0,
                          "vModel": 1.0,
                          "fixed": True,
                          "prior": False,
                          "prior_mean": 1.0,
                          "prior_sigma": 0.05
                        },
                        "TrackNorm": {
                          "vData": 1.0,
                          "vModel": 1.0,
                          "fixed": True,
                          "prior": False,
                          "prior_mean": 1.0,
                          "prior_sigma": 0.1
                        },
                        "ShowerNorm": {
                          "vData": 1.0,
                          "vModel": 1.0,
                          "fixed": True,
                          "prior": False,
                          "prior_mean": 1.0,
                          "prior_sigma": 0.1
                        }
                      }
                    }

    # Check if file already exists
    if os.path.exists(os.path.join(json_path, f'PARAMETERS/params_template_{order}.json')):
        print(f"File already exists: params_template_{order}.json")
    else:
        with open(os.path.join(json_path, f'PARAMETERS/params_template_{order}.json'), 'w') as f:
            json.dump(json_file, f, indent=4)
            print(f"Created file: params_template_{order}.json")    

def create_json_binning(
  json_path: str,
  nbins: int,
):
  energy_reco_bins = np.round(np.geomspace(10, 100, nbins), 4)
  energy_reco_bins = np.append(energy_reco_bins, 1000)
  json_file = {
      "binning": {
        "nEbinsTrue": 30,
        "EminTrue": 1,
        "EmaxTrue": 100,

        "nEbinsReco": 20,
        "EminReco": 10,
        "EmaxReco": 100,

        "ncosTbinsTrue": 40,
        "ncosTbinsReco": 25,

        "nBybinsTrue": 1,
        "nBybinsReco": 1,

        "custom" : True,
        "custom_EbinsReco": energy_reco_bins.tolist()
      }
    }
  
  # Check if file already exists
  if os.path.exists(os.path.join(json_path, f'ANTARES/binning_ANTARES_{nbins+1}.json')):
      print(f"File already exists: binning_ANTARES_{nbins+1}.json")
  else:
      with open(os.path.join(json_path, f'ANTARES/binning_ANTARES_{nbins+1}.json'), 'w') as f:
          json.dump(json_file, f, indent=4)
          print(f"Created file: binning_ANTARES_{nbins+1}.json")

        

def run_json_files(
    channel: str,
    reco: str,
    order: str,
    systematics: str,    
    json_path: str,
    npoints: int,
    cut: str,
    smear_level: str,
    assym_energy: str,
    assym_direction: str,
):
    # Create the json files
    print("Creating JSON User files...")
    create_json_User(reco, order, channel, systematics, json_path, cut, npoints, smear_level)

    print("\nCreating JSON variables files...")
    create_json_variables(channel, json_path, smear_level, assym_energy, assym_direction)

    print("\nCreating JSON classes files...")
    create_json_classes(json_path, reco, cut, smear_level)
    
    print("\nCreating JSON parameters files...")
    create_json_params(json_path, order, systematics)
    
    print("\nCreate JSON binning files...")
    create_json_binning(json_path, 15)


def main():
    # Define the parameters
    arg = ArgumentParser()
    channel = arg.channel
    reco = arg.reco
    order = arg.order
    systematics = arg.systematics
    cut_option = arg.cut
    smear_level = arg.smear_level
    assym_energy = arg.assym_energy
    assym_direction = arg.assym_direction

    print("Starting the process...")
    print("\nArguments provided:")
    print(f"Channel: {channel}")
    print(f"Reconstruction: {reco}")
    print(f"Mass ordering: {order}")
    print(f"Systematics: {systematics}")
    print(f"Cut option: {cut_option}")
    print(f"Smear level: {smear_level}\n")
    
    systematics = "systematics" if systematics == "1" else "no_systematics"
    
    if (channel is None) or (reco is None) or (order is None) or (systematics is None):
        raise ValueError("Please provide the required arguments")
    
    # Define the json path
    json_path = os.path.join(os.getcwd(), 'json')
    
    # Check if the directories required exist
    if not os.path.exists(json_path):
        os.makedirs(json_path)
        os.makedirs(os.path.join(json_path, 'USER'))
        os.makedirs(os.path.join(json_path, 'ANTARES'))
        os.makedirs(os.path.join(json_path, 'PARAMETERS'))
    elif not os.path.exists(os.path.join(json_path, 'USER')):
        os.makedirs(os.path.join(json_path, 'USER'))
    elif not os.path.exists(os.path.join(json_path, 'ANTARES')):
        os.makedirs(os.path.join(json_path, 'ANTARES'))
    elif not os.path.exists(os.path.join(json_path, 'PARAMETERS')):
        os.makedirs(os.path.join(json_path, 'PARAMETERS'))
      
    if systematics == "no_systematics":
      npoints = 21
    elif systematics == "systematics":
      npoints = 15
        
    run_json_files(channel, reco, order, systematics, json_path, npoints, cut_option, smear_level, assym_energy, assym_direction)
    
if __name__ == '__main__':
    main()