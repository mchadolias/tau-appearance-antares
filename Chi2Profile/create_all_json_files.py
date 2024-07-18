import json 
import os
from itertools import product

text_conversion = {
    "STD": "Std",
    "TAU": "Tau",
}

reco_info = {"MC" : {"energy": "energy_recoTrue", "zenith": "cos_zenith_recoTrue", "biy": "bjorken_y_recoTrue"},
             "AAFit_dedx" : {"energy": "energy_aafit_dEdX_CEA", "zenith": "aafit_cos_zenith", "biy": "aafit_bjy"},
             "AAFit_ann" : {"energy": "energy_aafit_ANN_ECAP", "zenith": "aafit_cos_zenith", "biy": "aafit_bjy"},
             "NNFit_full" : {"energy": "Energy", "zenith": "cos_zenith", "biy":"NNFit_Bjorken_y"},
             "NNFit_dir": {"energy": "energy_recoTrue", "zenith": "cos_zenith", "biy":"NNFit_Bjorken_y"},
            }

def create_json_User(
    reco_list: list,
    channel_list: list,
    ordering_list: list,
    fixed_free_list: list,
    json_path: str,
):
    # Create the base directory
    sys_option_list = ("systematics", "no_systematics")
    
    # Generate all combinations using itertools.product
    for reco, experiment, order, ff, sys_option in product(reco_list, channel_list, ordering_list, fixed_free_list, sys_option_list):
        
        if ff == 'fixed':
            npoints = 21
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
                "experiment": experiment,
                "reco": reco,
                "both_octants": True,
                "sys_option": sys_option,
            }
        }

        # Check if file already exists
        if os.path.exists(os.path.join(json_path, f'USER/User_{reco}_{experiment}_{order}_{ff}_{sys_option}.json')):
            print(f"File already exists: User_{reco}_{experiment}_{order}_{ff}_{sys_option}.json")
        else:
            with open(os.path.join(json_path, f'USER/User_{reco}_{experiment}_{order}_{ff}_{sys_option}.json'), 'w') as f:
                json.dump(json_file, f, indent=4)
                print(f"Created file: User_{reco}_{experiment}_{order}_{ff}_{sys_option}.json")
        
def create_json_variables(
    channel_list: list,
    json_path: str
):    
    for channel in channel_list:
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

def create_json_classes(
    json_path: str,
    reco_list: list
):    
    for reco in reco_list:
      if reco == "NNFit_full":
        json_file = {
        "classes": [
        {
          "name": "tracks",
          "general_cut": "((abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && (cos_zenith_recoTrue < 0)",
          "muon_loose_cut": "((abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && (cos_zenith_recoTrue < 0)",
          "reconstructions": { 
              "E": f"NNFitTrack_{reco_info[reco]['energy']}",
              "cosT": f"NNFitTrack_{reco_info[reco]['zenith']}",
              "By": f"{reco_info[reco]['biy']}"
            },
          "ClassNorm": "TrackNorm"
        },
        {    
          "name": "showers",
          "general_cut": "(!(abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && (cos_zenith_recoTrue < 0)",
          "muon_loose_cut": "(!(abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && (cos_zenith_recoTrue < 0)",
          "reconstructions": {
              "E": f"NNFitShower_{reco_info[reco]['energy']}",
              "cosT": f"NNFitShower_{reco_info[reco]['zenith']}",
              "By": f"{reco_info[reco]['biy']}"
            },
          "ClassNorm": "ShowerNorm"
        }]}
      elif reco == "NNFit_dir":
                json_file = {
        "classes": [
        {
          "name": "tracks",
          "general_cut": "((abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && (cos_zenith_recoTrue < 0)",
          "muon_loose_cut": "((abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && (cos_zenith_recoTrue < 0)",
          "reconstructions": { 
              "E": f"{reco_info[reco]['energy']}",
              "cosT": f"NNFitTrack_{reco_info[reco]['zenith']}",
              "By": f"{reco_info[reco]['biy']}"
            },
          "ClassNorm": "TrackNorm"
        },
        {    
          "name": "showers",
          "general_cut": "(!(abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && (cos_zenith_recoTrue < 0)",
          "muon_loose_cut": "(!(abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && (cos_zenith_recoTrue < 0)",
          "reconstructions": {
              "E": f"{reco_info[reco]['energy']}",
              "cosT": f"NNFitShower_{reco_info[reco]['zenith']}",
              "By": f"{reco_info[reco]['biy']}"
            },
          "ClassNorm": "ShowerNorm"
        }]}
        
      else:
                json_file = {
        "classes": [
        {
          "name": "tracks",
          "general_cut": "((abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && (cos_zenith_recoTrue < 0)",
          "muon_loose_cut": "((abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && (cos_zenith_recoTrue < 0)",
          "reconstructions": { 
              "E": f"{reco_info[reco]['energy']}",
              "cosT": f"{reco_info[reco]['zenith']}",
              "By": f"{reco_info[reco]['biy']}"
            },
          "ClassNorm": "TrackNorm"
        },
        {    
          "name": "showers",
          "general_cut": "(!(abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && (cos_zenith_recoTrue < 0)",
          "muon_loose_cut": "(!(abs(type) == 14) || (abs(type) == 16 && interaction_type == 2)) && (cos_zenith_recoTrue < 0)",
          "reconstructions": {
              "E": f"{reco_info[reco]['energy']}",
              "cosT": f"{reco_info[reco]['zenith']}",
              "By": f"{reco_info[reco]['biy']}"
            },
          "ClassNorm": "ShowerNorm"
        }]}

        
        
      # Check if file already exists
      if os.path.exists(os.path.join(json_path, f'ANTARES/classes_ANTARES_{reco}.json')):
          print(f"File already exists: classes_ANTARES_{reco}.json")
      else:
          with open(os.path.join(json_path, f'ANTARES/classes_ANTARES_{reco}.json'), 'w') as f:
              json.dump(json_file, f, indent=4)
              print(f"Created file: classes_ANTARES_{reco}.json")    
    
def create_json_params(
    json_path: str,
    ordering_list: list,
    fixed_free_list: list,
    systematics_list: list
):
    create_param_template(json_path, ordering_list)
    
    for order, ff, sys_option in product(ordering_list, fixed_free_list, systematics_list):
        # Read the template file
        with open(os.path.join(json_path, f'PARAMETERS/params_template_{order}.json'), 'r') as f:
            json_file = json.load(f)
        
        # Update the file
        if ff == 'fixed':
            json_file["parameters"]["TauNorm"]["fixed"] = True
        elif ff == 'free':
            json_file["parameters"]["TauNorm"]["fixed"] = False
            
        if sys_option == 'systematics':
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
        if os.path.exists(os.path.join(json_path, f'PARAMETERS/parameters_Data_NO_Model_{order}_{ff}_{sys_option}.json')):
            print(f"File already exists: parameters_Data_NO_Model_{order}_{ff}_{sys_option}.json")
        else:
            with open(os.path.join(json_path, f'PARAMETERS/parameters_Data_NO_Model_{order}_{ff}_{sys_option}.json'), 'w') as f:
                json.dump(json_file, f, indent=4)
                print(f"Created file: parameters_Data_NO_Model_{order}_{ff}_{sys_option}.json")
    
    # Remove the template file
    for order in ordering_list: 
        print(f"Removing template file: params_template_{order}.json")   
        os.remove(os.path.join(json_path, f'PARAMETERS/params_template_{order}.json'))

def create_param_template(
    json_path: str,
    ordering_list: list,
):
    for order in ordering_list:
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


def run_json_files(
    reco_list: list,
    channel_list: list,
    ordering_list: list,
    fixed_free_list: list,
    systematics_list: list,
    json_path: str
):
    # Create the json files
    print("Creating JSON User files...")
    create_json_User(reco_list, channel_list, ordering_list, fixed_free_list, json_path)

    print("\nCreating JSON variables files...")
    create_json_variables(channel_list, json_path)

    print("\nCreating JSON classes files...")
    create_json_classes(json_path, reco_list)
    
    print("\nCreating JSON parameters files...")
    create_json_params(json_path, ordering_list, fixed_free_list, systematics_list)

    
if __name__ == '__main__':
    # Define the categories and possible values
    reco_list = ['MC', 'AAFit_dedx', 'AAFit_ann', 'NNFit_full', 'NNFit_dir']
    channel_list = ['STD', 'TAU']
    ordering_list = ['NO', 'IO']
    fixed_free_list = ['fixed', 'free']
    systematics_list = ['systematics', 'no_systematics']
    
    json_path = os.path.join(os.getcwd(), 'json')
    
    # Check if the directories required exist
    if not os.path.exists(json_path):
        os.makedirs(json_path)
        os.makedirs(os.path.join(json_path, 'USER'))
        os.makedirs(os.path.join(json_path, 'ANTARES'))
        os.makedirs(os.path.join(json_path, 'PARAMETERS'))
    
    run_json_files(reco_list, channel_list, ordering_list, fixed_free_list, systematics_list, json_path)
    