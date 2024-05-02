import os
import sys
import file_management as fm
from argparse import ArgumentParser
from tabulate import tabulate

def argument_parser():
    parser = ArgumentParser(description="Application to count number of files per interaction type in the selected ROOT file.")

    parser.add_argument("--r", type=str, dest="input_root_file", help="The input root file.", default="full_nutau_sample.root")
    parser.add_argument("--p", type=str, dest="path_to_file", help="The path for all files. It's assumed that the same directory structure is kept accross platforms.",
                        default="/home/wecapstor3/capn/mppi133h/ANTARES/mc/cut_selection/low_energy")
    return parser.parse_args()


if __name__ == "__main__":
    
    # Load the data
    print("Loading the data...")
    args = argument_parser()    

    if not vars(args):
        print("No arguments given. Exciting the program...")
        sys.exit(1)
    
    root_file = args.input_root_file
    path = args.path_to_file
    
    print(f"ROOT file: {root_file}")
    print(f"Path to file: {path}")
    
    COLUMNS = ["RunID", "Type", "interaction_type"] 
        
    df_antdst = fm.load_large_rootfile_to_df(os.path.join(path, root_file), columns=COLUMNS)
    
    unique_runs = list(df_antdst.groupby(["Type","interaction_type"])["RunID"].nunique().items())
    
    print(tabulate(unique_runs, headers=[["Type", "interaction_type"], "Number of files"], tablefmt="pretty"))
    
    with open(f"./summary_files/{root_file.split('.')[0]}_num_runs.txt", "w") as f:
        f.write(tabulate(unique_runs, headers=[["Type", "interaction_type"], "Number of files"], tablefmt="pretty"))
        print(f"\nFile {root_file.split('.')[0]}_num_runs.txt was created.")
        
    print("\n======== END OF SCRIPT ========")