import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np
import uproot
import argparse
from itertools import product
import os
import scienceplots

# Set the style of the plots
plt.style.use(['science', "grid"])    
plt.rcParams['savefig.dpi'] = 1000
plt.rcParams.update({
    'axes.titlesize': 20,
    'axes.labelsize': 15,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12
})

text_conversion = {
    "STD": "CC",
    "TAU": "NC+CC",
    "NO": "Normal Ordering",
    "IO": "Inverted Ordering",
    "MC": "MC",
    "AAFit": "AAFit",
    "NNFit": "NNFit",
    "AAFit_dedx": "AAFit dedx",
    "AAFit_ann": "AAFit ANN",
    "NNFit_full": "NNFit",
    "NNFit_dir": "NNFit direction reco only"
}

def ArgumentParser():
    parser = argparse.ArgumentParser(description='Plotter for chi2 profile')
    parser.add_argument('--type', type=str, default='reconstruction', 
                        help="Select type of plot to be made: reconstruction or study")
    parser.add_argument('--reco', type=str, 
                        help="Choose the reconstruction algorithm used to reconstruct the events")
    parser.add_argument('--channel', type=str,
                        help="Choose which channel to channel. STD corresponds to CC and TAU corresponds to NC")
    parser.add_argument('--path', type=str, 
                        default="/sps/km3net/users/mchadoli/master_thesis/tau_appearance/Chi2Profile/",
                        help="Path to the root files")
    parser.add_argument('--systematic', type=str, default="no_systematics",
                        help="Choose if the systematic uncertainties are included or not")
    parser.add_argument('--cut', type=str, default="no_muons",
                        help="Choose if the muons are included or not")
    args = parser.parse_args()
    return args

def _root_to_tables(root_file, tree_name = "outTree", columns = ["chi2","TauNorm"]):
    
    # Load the root file
    with uproot.open(root_file) as f:
        data = f[tree_name].arrays(columns, library="numpy")
    return data

def load_chi2_data(
    reco,
    channel,
    order,
    path,
):
    # Load the data
    print(f"Loading data for {reco} {channel} {order}...")
    data_fixed = _root_to_tables(os.path.join(path, reco, channel, order,
                                        f"fixed/Chi2Profile_TauNorm_{channel}_{order}_fixed_FitTwoOctants.root"))
    data_free = _root_to_tables(os.path.join(path, reco, channel, order,
                                        f"free/Chi2Profile_TauNorm_{channel}_{order}_free_FitTwoOctants.root"))
    
    return data_fixed, data_free

def square_root(
    data_list: list,
):
    return [np.sqrt(x) if x > 0 else 0 for x in data_list]

def plot_chi2(
    type,
    path,
    channel,
    reco,
    save_path,
):
    
    # Define the mass ordering
    ordering = ["IO"]
    
    # Define the font for legend
    font = font_manager.FontProperties(family='sans-serif', style='normal', size=12)
    
    print(f"Plotting {type}...")
    if type == "reconstruction":
        recos = ["MC", "AAFit_dedx", "AAFit_ann", "NNFit_full", "NNFit_dir"]

        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        for order in ordering:
            print(f"Plotting for {order}...")
            zoomed_ax = fig.add_axes([0.6, 0.6, 0.29, 0.26])
            for reco in recos:
                data_fixed, data_free = load_chi2_data(reco, channel, order, path)
                print(len(data_fixed["TauNorm"]), len(data_fixed["chi2"] - data_free["chi2"]))
                ax.plot(data_fixed["TauNorm"], data_fixed["chi2"] - data_free["chi2"], 
                        'o', markersize=7, label=f"{text_conversion[reco]}")
                zoomed_ax.plot(data_fixed["TauNorm"], data_fixed["chi2"] - data_free["chi2"],
                                 'o--', linewidth=2, markersize=5)
            zoomed_ax.set(
                xlim = (0, 2),
                ylim = (0, 100),
            )
            ax.set(
                xlabel="Tau Normalization",
                ylabel="$\Delta \chi^2$",
                xlim=(0, 2),
                title = f"Chi2 profile for {text_conversion[channel]} channel and \
                {text_conversion[order]}",
                ylim = (0, 750),
            )
            ax.legend(prop=font, frameon=False, loc=(0.2, 0.8))
            fig.savefig(os.path.join(save_path, f"Chi2Profile_{type}_{channel}_{order}.png"))
        
    elif type == "study":
        channels = ["STD", "TAU"]
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        zoomed_ax = fig.add_axes([0.5, 0.5, 0.39, 0.36]) 
        for order, channel in product(ordering, channels):
            data_fixed, data_free = load_chi2_data(reco, channel, order, path)   
            ax.plot(data_fixed["TauNorm"], data_fixed["chi2"] - data_free["chi2"], 
                    'o', markersize=7, label=f"{text_conversion[order]} ({text_conversion[channel]})")
            zoomed_ax.plot(data_fixed["TauNorm"], data_fixed["chi2"] - data_free["chi2"],
                            'o--', linewidth=2, markersize=5)
        ax.set(
            xlabel="Tau Normalization",
            ylabel="$\Delta \chi^2$",
            xlim=(0, 2),
            title = f"Chi2 profile for {reco} reco",
            ylim= (0, 100)
        )
        ax.legend(prop=font, frameon=False)
        fig.savefig(os.path.join(save_path, f"Chi2Profile_{type}_{reco}.png"))
            
def sigma_plots(
    type,
    path,
    channel,
    reco,
    save_path,
):
    
    # Define the mass ordering        
    ordering = ["NO", "IO"]
    
    # Define the font for legend
    font = font_manager.FontProperties(family='sans-serif', style='normal', size=10)
    
    print(f"\nPlotting sigma plots for {type}...")
    if type == "reconstruction":
        recos = ["MC", "AAFit_dedx", "AAFit_ann", "NNFit_full", "NNFit_dir"]

        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        for order in ordering:
            for reco in recos:
                data_fixed, data_free = load_chi2_data(reco, channel, order, path)
                ax.plot(data_fixed["TauNorm"], square_root(data_fixed["chi2"] - data_free["chi2"]), 
                        'o--', linewidth=2, markersize=4, label=f"{text_conversion[reco]}")
            ax.axhline(y=3, linestyle='--', c = "black")
            ax.axhline(y=5, linestyle='-.', c = "black")
            ax.set(
                xlabel="Tau Normalization",
                ylabel="Significance ($\sigma$)",
                xlim=(0, 2),
                title = f"Sensitivity of Tau Normalization for {text_conversion[channel]} channel and \
                {text_conversion[order]}",
                ylim = (0, 30),
            )
            ax.legend(prop=font, frameon=False)
            fig.savefig(os.path.join(save_path, f"SigmaPlots_{type}_{channel}_{order}.png"))
        
    elif type == "study":
        channels = ["STD", "TAU"]
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 8)) 
        for order, channel in product(ordering, channels):
            data_fixed, data_free = load_chi2_data(reco, channel, order, path)   
            diff = data_fixed["chi2"] - data_free["chi2"]
            square_diff = [np.sqrt(x) if x > 0 else 0 for x in diff]
            ax.plot(data_fixed["TauNorm"], square_diff, 
                    'o--', linewidth=2, markersize=5, label=f"{text_conversion[order]} ({text_conversion[channel]})")
        ax.axhline(y=3, linestyle='--', c = "black")
        ax.axhline(y=5, linestyle='-.', c = "black")
        ax.set(
            xlabel="Tau Normalization",
            ylabel="Significance ($\sigma$)",
            xlim=(0, 2),
            title = f"Sensitivity of Tau Normalization for {reco} reco",
            ylim= (0, 30)
        )
        ax.legend(prop=font, frameon=False)
        fig.savefig(os.path.join(save_path, f"SigmaPlots_{type}_{reco}.png"))

if __name__ == '__main__':
    
    args = ArgumentParser()
    type = args.type
    path = args.path
    reco = args.reco
    channel = args.channel
    systematic = args.systematic
    cut_option = args.cut
    
    rootpath =  os.path.join(path, f"output/ANTARES/{cut_option}/{systematic}")
    save_path = os.path.join(path, f"plots/{cut_option}/{systematic}/merged")
    
    if type ==  "reconstruction":
        if channel is None:
            raise ValueError("Please provide the channel channel")
    elif type == "study":
        if reco is None:
            raise ValueError("Please provide the reconstruction algorithm")
        
    # Check if the paths exist
    if not os.path.exists(path):
        raise ValueError("The path for the files does not exist")
    if not os.path.exists(save_path):
        print("The path to save the plots does not exist. Creating the directory...")
        os.makedirs(save_path)
    
    # Plotting the chi2 profile
    plot_chi2(type, rootpath, channel, reco, save_path)
    
    # Plotting the significance
    sigma_plots(type, rootpath, channel, reco, save_path)
    
    
    