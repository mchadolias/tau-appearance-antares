import pandas as pd
import numpy as np
from tabulate import tabulate
import os
import time
from datetime import timedelta
import argparse
import sys
sys.path.append("scripts")
import file_management as fm
import lib_masks as masks

def argument_parser():
    parser = argparse.ArgumentParser(description="Application to do count the number of reconstructed events per reconstructed algorithm.")

    parser.add_argument("--c", type=str, dest="cluster", 
                        help="The name of the cluster you are working on.", default="woody")
    
    parser.add_argument("--f", type=str, dest="files",
                        help="The files you are working with.", default="test")
    parser.add_argument("--d", type=str, dest="path",
                        help="The path to the data.", default="cut_selection/low_energy")
    args = parser.parse_args()
    return args

def define_clusters(cluster):
    """
    Define the computing cluster you are working on.
    
    Args:
        cluster (str): The name of the cluster you are working on.
    """
    if cluster == "woody":
        sys.path.append("/home/saturn/capn/mppi133h/master_thesis/tau_appearance/reconstruction_perfomance")
        path = "/home/wecapstor3/capn/mppi133h/ANTARES/mc"
    elif cluster == "lyon":
        sys.path.append("/sps/km3net/users/mchadoli/master_thesis/tau_appearance/reconstuction_perfomance")
        path = "/sps/km3net/users/mchadoli/ANTARES/"
    else:
        print("The cluster you are working on is not defined.")
        sys.exit()
    
    return path

def create_masks(df):
    """
    Create the masks for the flavour types and event types.
    
    Args:
        df (pd.DataFrame): The dataframe containing the data.
        
    Returns:
        df (pd.DataFrame): The dataframe containing the data with the masks.
    """
    # Create the masks for the flavour types
    df_el_ma = masks.get_nuemask(df)
    df.loc[df_el_ma, "Flavour type"] = "electron"

    df_muon_ma = masks.get_numumask(df)
    df.loc[df_muon_ma, "Flavour type"] = "muon"

    df_tau_ma = masks.get_nutaumask(df)
    df.loc[df_tau_ma, "Flavour type"] = "tau"
    
    # Create the masks for the event types
    df_track_ma = masks.get_trackmask(df)
    df.loc[df_track_ma, "Event type"] = "tracks"

    df_shower_nc_ma = masks.get_showermask_nc(df)
    df.loc[df_shower_nc_ma, "Event type"] = "showers_nc"

    df_shower_cc_ma = masks.get_showermask_cc(df)
    df.loc[df_shower_cc_ma, "Event type"] = "showers_cc"
    
    return df


def set_file(file):
    """
    Define the flavour type you are working on.
    
    Args:
        file (str): The flavour type you are working on.
    """
    if file == "nutau":
        identifier = "tau"
        summary_file = "full_nutau_sample.root"
    elif file == "numu":
        identifier = "numu"
        summary_file = "full_numu_sample.root"
    elif file == "nue":
        identifier = "showers"
        summary_file = "full_nue_sample.root"
    elif file == "test":
        identifier = "numu_end_0"
        summary_file = "out_part4.root"
    else:
        print("The flavour type you are working on is not defined.")
        sys.exit()
    
    return identifier, summary_file

def load_nnfit(
    path, 
    identifier
):
    """
    Load the nnfit data.
    
    Args:
        path (str): The path to the data.
        identifier (str): The identifier of the data.
        
    Returns:
        df_nnfit (pd.DataFrame): The dataframe containing the nnfit data.
    """
    # Load the nnfit data
    print("Loading the data...")
    print(f"NNfit data: {identifier}")
    print(f"Path: {path}")
    ctime = time.time()
    
    #Load the dataframes
    print("Importing the dataframes...")
    nnfit_path = os.path.join(path, "nnfit_reco")
    nnfit_files = fm.list_files_with_pattern(nnfit_path, f"*{identifier}*")
    
    df_nnfit = fm.load_dataframes(nnfit_files, folder_path=nnfit_path)
        
    return df_nnfit

def flag_counter(df):
    """
    Count the number of reconstructed events per reconstructed algorithm.
    
    Args:
        df (pd.DataFrame): The dataframe containing the data.
        
    Returns:
        df_flags (pd.DataFrame): The dataframe containing the number of reconstructed events per reconstructed algorithm.
    """ 
    df_flags =  df.groupby(["Flavour type", "Event type"])[["aafit_flag",
                                                            "bbfit_flag",
                                                            "gridfit_flag",
                                                            "showerdusj_flag",
                                                            "NNFitTrack_flag",
                                                            "NNFitShower_flag"]].sum()                                                           
    
    # Merge the dataframes with the number of generated events
    df_flags = df_flags.merge(df.groupby(["Flavour type", "Event type"])["TriggCounter"].count(), on=["Flavour type", "Event type"])
    
    # Merge the number of RunID, Flavor type and Event type
    df_flags = df_flags.merge( df[["RunID", "Flavour type", "Event type"]].drop_duplicates().groupby(["Flavour type", "Event type"]).count(), on=["Flavour type", "Event type"])
    
    df_flags["Missing flags"] = np.abs(df_flags["RunID"] - df["RunID"].nunique())
    
    algo = ["aafit", "bbfit", "gridfit", "showerdusj", "NNFitTrack", "NNFitShower"]
    
    for a in algo:
        df_flags[f"{a}_flag"] = df_flags[f"{a}_flag"] / df_flags["TriggCounter"]
        
    return df_flags

def rename_h5_df_cols(
    df,
    mapper={
        "TrigCount": "TriggCounter",
        "EventID": "Frame",
    },
):
    return df.rename(columns=mapper)

if __name__ == "__main__":
    print("Counting reconstructed events...")
    
    # Define the columns to be loaded
    COLUMNS = [
        "RunID",
        "EventID",
        "TriggCounter",
        "Frame",
        "interaction_type",
        "is_cc",
        "Type",
        "aafit_flag",
        "bbfit_flag",
        "gridfit_flag",
        "showerdusj_flag",
        "bbfit_shower_flag"
    ]    
    
    # Parse the arguments
    args = argument_parser()
    cluster = args.cluster
    file = args.files
    sub_path = args.path
    
    # Define the cluster
    path = define_clusters(cluster)
    
    
    # Define the flavour type
    identifier, summary_file = set_file(file)
    
    # Load the nnfit data
    df_nnfit = load_nnfit(path, identifier)
    
    print("Renaming the columns...\n")
    df_nnfit = rename_h5_df_cols(df_nnfit)
    
    df_nnfit["NNFitTrack_flag"] = df_nnfit["NNFitTrack_Theta"].notna()
    df_nnfit["NNFitShower_flag"] = df_nnfit["NNFitShower_Theta"].notna() 
    
    
    # Load the AntDST extracted files
    print("Loading the AntDST files...")
    ctime = time.time()
    dfnu = fm.rootfile_to_df(os.path.join(path, sub_path, summary_file), columns=COLUMNS)
    print(f"AntDST data loaded in {timedelta(seconds=time.time()-ctime)}\n")
    
    # Merge the dataframes
    print("\nMerging the dataframes...")
    ctime = time.time()
    df = pd.merge(dfnu, df_nnfit, on=["RunID", "Frame", "TriggCounter"], how="left")
    
    print("Number of merged events: ", df.shape[0])
    print("Number of AntDST events: ", dfnu.shape[0])
    print("Number of NNFit events: ", df_nnfit.shape[0])
    
    print(f"Data merged in {timedelta(seconds=time.time()-ctime)}\n")
    
    del dfnu, df_nnfit
    
    # Create the masks
    print("Creating the masks...")
    ctime = time.time()
    
    df = create_masks(df)
    print(f"Masks created in {timedelta(seconds=time.time()-ctime)}")
    
    # Count the number of reconstructed events
    print("\nCounting the number of reconstructed events...")
    ctime = time.time()
    
    df_flags = flag_counter(df)
    
    print(tabulate(df_flags, headers="keys", tablefmt="psql"))
    
    if file != "test":
        with open(f"../summary_files/flag_summary_{file}.txt", "w") as f:
            f.write(tabulate(df_flags, headers="keys", tablefmt="psql"))
        
    print(f"Data counted in {timedelta(seconds=time.time()-ctime)}")
    
    print("\n======== END OF SCRIPT ========")