from pathlib import Path
from itertools import product

def create_directories(base_dir):
    # Define the categories and possible values
    reco_list = ['MC', 'AAFit_dedx', 'AAFit_ann', 'NNFit_full', "NNFit_dir"]
    channel_list = ['STD', 'TAU']
    type_list = ['NO', 'IO']
    fixed_free_list = ['fixed', 'free']
    experiment_list = ['ANTARES']
    
    # Create the base directory
    base_path = Path(base_dir)

    # Generate all combinations using itertools.product
    for sys_option in ("systematics", "no_systematics"):
        for reco, channel, type_, ff, experiment in product(reco_list, channel_list, type_list, fixed_free_list, experiment_list):
            dir_path = base_path / experiment / sys_option / reco / channel / type_ / ff

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