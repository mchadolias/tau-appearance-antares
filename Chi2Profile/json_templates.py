import json
import os

text_conversion = {
    "STD": "Std",
    "TAU": "Tau",
}

def json_variables_template(channel):
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
    return json_file

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
                          "prior_mean": 1.0,"vData": 7.42e-05,
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