import os
from pathlib import Path
from itertools import product

def create_directories(base_dir):
    # Define the categories and possible values
    reco_list = ['MC', 'AAFit', 'NNFit']
    experiment_list = ['STD', 'TAU']
    type_list = ['NO', 'IO']
    fixed_free_list = ['fixed', 'free']

    # Create the base directory
    base_path = Path(base_dir)
    antares_path = base_path / 'ANTARES'

    # Generate all combinations using itertools.product
    for reco, experiment, type_, ff in product(reco_list, experiment_list, type_list, fixed_free_list):
        dir_path = antares_path / reco / experiment / type_ / ff
        
        # Check if the directory already exists
        if dir_path.exists():
            print(f"Folder already exists: {dir_path}")
        else:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {dir_path}")

if __name__ == '__main__':
    # Specify the base directory
    base_directory = 'output'

    # Create the directory structure
    create_directories(base_directory)