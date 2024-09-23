from pathlib import Path
from itertools import product
import argparse

def ArgumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cut", type=str, default="muon_free",
                        help="Choose the cut to be applied")
    return parser.parse_args()
    
    
def create_directories(base_dir, cut):
    # Define the categories and possible values
    smeared_level_list = [
        'km3net', 
        '10_percent',
        '50_percent',
        '100_percent',
        '200_percent',
        '500_percent',
        "antares"]
    
    reco_list = [
        'MC',
        'AAFit_dedx',
        'AAFit_ann',
        'NNFit_full',
        "NNFit_dir"]
    
    channel_list = ['STD', 'TAU']
    type_list = ['NO', 'IO']
    fixed_free_list = ['fixed', 'free']
    experiment_list = ['ANTARES']
    
    # Create the base directory
    base_path = Path(base_dir)

    counter = 0
    # Generate all combinations using itertools.product
    for sys_option in ("systematics", "no_systematics"):
        for reco, channel, type_, ff, experiment in product(reco_list, channel_list, type_list, fixed_free_list, experiment_list):
            
            dir_path = base_path / experiment / cut / "unsmeared" /  sys_option / reco / channel / type_ / ff

            # Check if the directory already exists
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {dir_path}")
                counter += 1

        for channel, type_, ff, experiment, smeared_level in product(channel_list, type_list, fixed_free_list, experiment_list, smeared_level_list):
            
            dir_path = base_path / experiment / cut / "smeared" / smeared_level / sys_option / channel / type_ / ff

            # Check if the directory already exists
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {dir_path}")
    
    if counter == 0:
        print("\nAll directories already exist.")
    else:
        print(f"\nCreated {counter} directories.")
        
if __name__ == '__main__':
    # Specify the base directory
    base_directory = 'output'
    
    args = ArgumentParser()
    cut = args.cut

    # Create the directory structure
    create_directories(base_directory, cut)