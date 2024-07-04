import json 
import os
from itertools import product


def create_json_User(
    reco_list: list,
    experiment_list: list,
    ordering_list: list,
    fixed_free_list: list,
):
    # Create the base directory
    json_path = os.path.join(os.getcwd(), 'json')
    
    # Generate all combinations using itertools.product
    for reco, experiment, order, ff in product(reco_list, experiment_list, ordering_list, fixed_free_list):
        
        if ff == 'fixed':
            npoints = 10
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
            }
        }

        # Check if file already exists
        if os.path.exists(os.path.join(json_path, f'User_{reco}_{experiment}_{order}_{ff}.json')):
            print(f"File already exists: User_{reco}_{experiment}_{order}_{ff}.json")
        else:
            with open(os.path.join(json_path, f'User_{reco}_{experiment}_{order}_{ff}.json'), 'w') as f:
                json.dump(json_file, f, indent=4)
                print(f"Created file: User_{reco}_{experiment}_{order}_{ff}.json")
        
    

if __name__ == '__main__':
    # Define the categories and possible values
    reco_list = ['MC', 'AAFit', 'NNFit']
    experiment_list = ['STD', 'TAU']
    ordering_list = ['NO', 'IO']
    fixed_free_list = ['fixed', 'free']
    
    create_json_User(reco_list, experiment_list, ordering_list, fixed_free_list)

    