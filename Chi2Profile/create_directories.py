from pathlib import Path
import os
from itertools import product
import argparse

def ArgumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_directory", type=str, 
                        default="/sps/km3net/users/mchadoli/master_thesis/tau_appearance/Chi2Profile/",
                        help="Path to the project directory")
    parser.add_argument("--cut", type=str, default="muon_free",
                        help="Choose the cut to be applied")
    return parser.parse_args()
    
    
def output_directory(
    base_dir,
    cut
):
    # Define the categories and possible values
    smeared_level_list = [
        'km3net', 
        '10_percent',
        '50_percent',
        "70_percent",
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
    base_path = Path(os.path.join(base_dir, "output"))

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

def plot_directory(
    base_directory,
    cut,
):
    base_path = Path(os.path.join(base_directory, "plots", cut))

    # Define the categories and possible values
    type = ["reconstruction", "study", "smeared"]
    sys_option = ["systematics", "no_systematics"]

    for sys_option, type in product(sys_option, type):
        dir_path = base_path / sys_option / type

        # Check if the directory already exists
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {dir_path}")
        else:
            print(f"Directory already exists: {dir_path}")

if __name__ == '__main__':
    
    args = ArgumentParser()
    base_directory = args.base_directory
    cut = args.cut

    # Create the directory structure
    output_directory(base_directory, cut)

    # Create plot directory
    plot_directory(base_directory, cut)