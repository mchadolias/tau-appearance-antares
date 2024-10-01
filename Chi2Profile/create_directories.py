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

# Global variables
SMEARED_LEVEL = [
    'orca6',
    'orca115', 
    '10_percent',
    '50_percent',
    "70_percent",
    '100_percent',
    '200_percent',
    '500_percent',
    "antares"
]
    
RECO_LIST = [
    'MC',
    'AAFit_dedx',
    'AAFit_ann',
    'NNFit_full',
    "NNFit_dir"
]
    
CHANNEL_LIST = [
    'STD', 
    'TAU'
]

TYPE_LIST = [
    'NO', 
    'IO'
]
FIT_LIST = [
    'fixed', 
    'free'
]

SYS_LIST = [
    "no_systematics",
    "systematics",
]

def output_directory(
    base_dir,
    cut
):
    
    # Create the base directory
    base_path = Path(os.path.join(base_dir, "output", "ANTARES", cut))

    counter = 0
    # Generate all combinations using itertools.product
    for reco, channel, type_, ff, sys_option in product(RECO_LIST,CHANNEL_LIST, TYPE_LIST, FIT_LIST, SYS_LIST):
        
        dir_path = base_path / "unsmeared" /  sys_option / reco / channel / type_ / ff
        # Check if the directory already exists
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {dir_path}")
            counter += 1

    for channel, type_, ff, sys_option, smeared_level in product(CHANNEL_LIST, TYPE_LIST, FIT_LIST, SYS_LIST, SMEARED_LEVEL):
        dir_path = base_path / "smeared" / smeared_level / sys_option / channel / type_ / ff
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

    for sys_option, type in product(SYS_LIST, type):
        dir_path = base_path / sys_option / type

        # Check if the directory already exists
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {dir_path}")
        else:
            print(f"Directory already exists: {dir_path}")

def main():
    args = ArgumentParser()
    base_directory = args.base_directory
    cut = args.cut
    
    # Create the directory structure
    output_directory(base_directory, cut)

    # Create plot directory
    plot_directory(base_directory, cut)

if __name__ == "__main__":
    main()