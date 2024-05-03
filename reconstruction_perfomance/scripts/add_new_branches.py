import os 
import sys
import pandas as pd
from argparse import ArgumentParser
sys.path.append("../scripts/")
import file_management as fm

def argument_parser():
    parser = ArgumentParser(description="Application to add variables to a rootfile")
    
    parser.add_argument("--r", type=str, dest="input_root_file", help="The input root file.", default="full_nutau_sample.root")
    parser.add_argument("--h5", type=str, dest="input_h5_file", help="The input h5 file. The available options are Taus, Showers, NumuCC and Mupage.", default="Taus")
    parser.add_argument("--p", type=str, dest="path_to_file", help="The path for all files. It's assumed that the same directory structure is kept accross platforms.",
                        default="/home/wecapstor3/capn/mppi133h/ANTARES/mc")
    parser.add_argument("--task", type=str, dest="task", help="The task to perform. The available options are cut_selection and merged.", default="merged")
    parser.add_argument("--c", type=str, dest="cluster", help="The cluster to run the code. The available options are woody and lyon.", default="woody")
    parser.add_argument("--t", type=bool, dest="test", help="Run the test function.", default=False)
    
    return parser.parse_args()

def merge_dataframes(df_main, df_new, on=["RunID","Frame","TriggCounter"], method = "left"):
    df = df_main.merge(df_new, on=on, how=method)
    
    print(f"Shape of the ROOT dataframe: {df_main.shape}")
    print(f"Shape of the H5 dataframe: {df_new.shape}")
    print(f"Shape of the merged dataframe: {df.shape}")
    
    return df

def run_test_woody():
    path = "/home/saturn/capn/mppi133h/master_thesis/tau_appearance/reconstruction_perfomance/data/Comparison"
    files = os.listdir(path)
    input_root_file = [file for file in files if file.endswith(".root")][0]
    input_h5_file = [file for file in files if file.endswith(".hdf5")][0]
    
    return input_root_file, input_h5_file, path

def run_test_lyon():
    path = "/sps/km3net/users/mchadoli/ANTARES/test"
    input_root_file = "MC_065884_anutau_a_CCshow_reco.root"
    input_h5_file = "MC_065884_anutau_a_CCshow_reco.i3.hdf5"
    
    return input_root_file, input_h5_file, path 

def define_file_path(task):
    if task == "cut_selection":
        return "cut_selection/low_energy"
    elif task == "merged":
        return "merged/merged_before_nnfit"
    else:
        raise ValueError("The task is not defined or wrong value has been given. Please choose between cut_selection and merged. Check the argument_parser function.")
    
def modify_dataframe(df, is_merged_file = False):
    # Drop "File" column -> Note: The column is only present in merged h5 files
    if is_merged_file:
        df.drop(columns=["File"], inplace=True)
        print("The column 'File' has been dropped.")
    
    # Insert one column "weights_one_year"  
    df.insert(df.columns.get_loc("weight_honda") + 1, "weights_one_year", df["weight_w2"].copy())
    print("The column 'weights_one_year' has been inserted.\n")

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
    cluster = args.cluster
    task = args.task
    
    if is_test:
        if cluster == "woody":
            input_root_file, input_h5_file, path = run_test_woody()
        elif cluster == "lyon":
            input_root_file, input_h5_file, path = run_test_lyon()     
            
        nnfit_path = rootfile_path = path        
    else:
        nnfit_path = os.path.join(path, "nnfit_reco", input_h5_file)
        rootfile_path = os.path.join(path, define_file_path(task))    
    
    # Load the dataframes
    print("ROOT FILE: ", input_root_file)
    print("H5 FILE: ", input_h5_file)
    print("PATH: ", path)
    print("\nImporting into dataframes...")

    # Load nnfit reco files
    print("\nLoading the nnfit reco files...")
    print(f"Path to the nnfit reco files: {nnfit_path}")
    nnfit_files = fm.list_files_with_pattern(nnfit_path, f"*{input_h5_file}*")
  
    df_nnfit = fm.load_dataframes(nnfit_files, folder_path= nnfit_path)

    # Load the rootfile
    print("\nLoading the rootfile...")
    df_antdst = fm.load_large_rootfile_to_df(os.path.join(rootfile_path, input_root_file))
    
    print("\nExporting the antdst dataframe to a hdf5 file...")
    if is_test:
        fm.save_to_hdf5(df_antdst, f"{input_root_file.split('.')[0]}.hdf5", path = os.path.join(path, "output"))
    else:    
        fm.save_to_hdf5(df_antdst, f"{input_root_file.split('.')[0]}.hdf5", path = rootfile_path)
    
    # Rename the columns
    print("\nRenaming the columns...")
    df_nnfit = fm.rename_h5_df_cols(df_nnfit)
    
    # Merge Dataframes
    print("\nMerging the dataframes...")
    df_merged = merge_dataframes(df_antdst, df_nnfit)
    
    # Delete from memory old frames
    del df_antdst, df_nnfit
    
    #Modify the dataframe
    print("\nModifying the dataframe...")
    if len(nnfit_files) > 1:
        modify_dataframe(df_merged, is_merged_file = True)
    else:
        modify_dataframe(df_merged)
    
    # Export the dataframe to a rootfile
    if is_test:
        fm.save_to_hdf5(df_merged, f"{input_root_file.split('.')[0]}_updated.hdf5", path = os.path.join(path, "output"))
        fm.export_dataframe_to_rootfile(df_merged, f"{input_root_file.split('.')[0]}_updated.root", path = os.path.join(path, "output"))
    else:
        fm.export_dataframe_to_rootfile(df_merged, f"{input_root_file.split('.')[0]}_updated.root", path = rootfile_path)
        fm.save_to_hdf5(df_merged, f"{input_root_file.split('.')[0]}_updated.hdf5", path = rootfile_path)
        
    print("\n============== END OF THE PROGRAM ==============\n")
    
    
    