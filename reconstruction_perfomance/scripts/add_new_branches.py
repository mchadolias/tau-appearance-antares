import os 
import sys
import pandas as pd
from argparse import ArgumentParser
sys.path.append("../scripts/")
from file_management import rootfile_to_df, list_files_with_pattern, load_dataframes, export_dataframe_to_rootfile, rename_h5_df_cols

def argument_parser():
    parser = ArgumentParser(description="Application to add variables to a rootfile")
    
    parser.add_argument("--i", type=str, dest="input_root_file", help="The input root file.")
    parser.add_argument("--n", type=str, dest="input_h5_file", help="The input h5 file.")
    parser.add_argument("--p", type=str, dest="path_to_file", help="The path for all files. It's assumed that the same directory structure is kept accross platforms.",
                        default="/home/wecapstor3/capn/mppi133h/ANTARES/mc")
    parser.add_argument("--t", type=bool, dest="test", help="Run the test function.", default=False)
    
    return parser.parse_args()

def merge_dataframes(df_main, df_new, on=["RunID","Frame","TriggCounter"], method = "left"):
    df = df_main.merge(df_new, on=on, how=method)
    
    print(f"Shape of the main dataframe: {df_main.shape}")
    print(f"Shape of the new dataframe: {df_new.shape}")
    print(f"Shape of the merged dataframe: {df.shape}")
    
    return df

def run_test():
    path = "/home/saturn/capn/mppi133h/master_thesis/tau_appearance/reconstruction_perfomance/data/Comparison"
    files = os.listdir(path)
    input_root_file = [file for file in files if file.endswith(".root")][0]
    input_h5_file = [file for file in files if file.endswith(".hdf5")][0]
    
    return input_root_file, input_h5_file, path

if __name__ == "__main__":
    # Load the data
    print("Loading the data...")
    
    # Parse the arguments
    args = argument_parser()
    
    if not vars(args):
        print("No arguments given. Exciting the program...")
        sys.exit(1)
        
    
    input_root_file = args.input_root_file
    input_h5_file = args.input_h5_file
    path = args.path_to_file
    is_test = args.test
    
    if is_test:
        input_root_file, input_h5_file, path = run_test()
        nnfit_path = path ; rootfile_path = path
    else:
        nnfit_path = os.path.join(path, "nnfit_reco")
        rootfile_path = os.path.join(path, "cut_selection/low_energy")       
    
    # Load the dataframes
    print("Importing into dataframes...")

    # Load nnfit reco files
    nnfit_files = list_files_with_pattern(nnfit_path, f"*{input_h5_file}*")    
    
    df_nnfit = load_dataframes(nnfit_files, folder_path= nnfit_path)

    # Load the rootfile
    df_antdst = rootfile_to_df(os.path.join(rootfile_path, input_root_file))
    
    # Rename the columns
    df_nnfit = rename_h5_df_cols(df_nnfit)
    
    # Merge Dataframes
    df_merged = merge_dataframes(df_antdst, df_nnfit)
    
    # Delete from memory old frames
    del df_antdst, df_nnfit
    
    # Export the dataframe to a rootfile
    if is_test:
        export_dataframe_to_rootfile(df_merged, f"{input_root_file.split('.')[0]}_updated.root", path)
    else:
        export_dataframe_to_rootfile(df_merged, f"{input_root_file.split('.')[0]}_updated.root")
    
    print("\n============== END OF THE PROGRAM ==============")
    
    
    
    
    
    