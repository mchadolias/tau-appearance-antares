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
    "NNFit": "NNFit"
}

def ArgumentParser():
    parser = argparse.ArgumentParser(description='Plotter for chi2 profile')
    parser.add_argument('--type', type=str, default='reconstruction', 
                        help="Select type of plot to be made: reconstruction or study")
    parser.add_argument('--reco', type=str, 
                        help="Choose the reconstruction algorithm used to reconstruct the events")
    parser.add_argument('--probe', type=str,
                        help="Choose which channel to probe. STD corresponds to CC and TAU corresponds to NC")
    parser.add_argument('--path', type=str, 
                        default="/sps/km3net/users/mchadoli/master_thesis/tau_appearance/Chi2Profile/output/ANTARES/",
                        help="Path to the root files")
    parser.add_argument('--save_path', type=str,
                        default="/sps/km3net/users/mchadoli/master_thesis/tau_appearance/Chi2Profile/plots/merged",
                        help="Path to save the plots")
    args = parser.parse_args()
    return args

def _root_to_tables(root_file, tree_name = "outTree", columns = ["chi2","TauNorm"]):
    
    # Load the root file
    with uproot.open(root_file) as f:
        data = f[tree_name].arrays(columns, library="numpy")
    return data

def load_chi2_data(
    reco,
    probe,
    order,
    path,
):
    # Load the data
    print(f"Loading data for {reco} {probe} {order}...")
    data_fixed = _root_to_tables(os.path.join(path, reco, probe, order,
                                        f"fixed/Chi2Profile_TauNorm_{probe}_{order}_fixed_FitTwoOctants.root"))
    data_free = _root_to_tables(os.path.join(path, reco, probe, order,
                                        f"free/Chi2Profile_TauNorm_{probe}_{order}_free_FitTwoOctants.root"))
    
    return data_fixed, data_free

def plot_chi2(
    type,
    path,
    probe,
    reco,
):
    
    # Define the mass ordering
    ordering = ["NO", "IO"]
    
    # Define the font for legend
    font = font_manager.FontProperties(family='sans-serif', style='normal', size=12)
    
    print(f"Plotting {type}...")
    if type == "reconstruction":
        recos = ["MC", "AAFit", "NNFit"]
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        for reco, order in product(recos, ordering):
            data_fixed, data_free = load_chi2_data(reco, probe, order, path)
            ax.plot(data_fixed["TauNorm"], data_fixed["chi2"] - data_free["chi2"], 
                    'o--', linewidth=2, markersize=5, label=f"{text_conversion[reco]} {text_conversion[order]}")
        ax.set(
            xlabel="Tau Normalization",
            ylabel="$\Delta \chi^2$",
            xlim=(0, 2),
            title = f"Chi2 profile for different reconstructions",
            #yscale = "log"
        )
        ax.legend(prop=font, frameon=False)
        fig.savefig(os.path.join(save_path, f"Chi2Profile_{type}_{probe}.png"))
        
    elif type == "study":
        probes = ["STD", "TAU"]
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 8)) 
        for order, probe in product(ordering, probes):
            data_fixed, data_free = load_chi2_data(reco, probe, order, path)   
            ax.plot(data_fixed["TauNorm"], data_fixed["chi2"] - data_free["chi2"], 
                    'o--', linewidth=2, markersize=5, label=f"{text_conversion[order]} ({text_conversion[probe]})")   
        ax.set(
            xlabel="Tau Normalization",
            ylabel="$\Delta \chi^2$",
            xlim=(0, 2),
            title = f"Chi2 profile for {reco} reco",
            ylim= (0, None)
        )
        ax.legend(prop=font, frameon=False)
        fig.savefig(os.path.join(save_path, f"Chi2Profile_{type}_{reco}.png"))
    elif type == "ordering":
        probes = ["STD", "TAU"]
        recos = ["MC", "AAFit", "NNFit"]
        
        for order in ordering:
            fig, ax = plt.subplots(1, 1, figsize=(10, 8)) 
            for reco, probe in product(recos, probes):
                data_fixed, data_free = load_chi2_data(reco, probe, order, path)   
                ax.plot(data_fixed["TauNorm"], data_fixed["chi2"] - data_free["chi2"], 
                        'o--', linewidth=2, markersize=5, label=f"{text_conversion[reco]} ({text_conversion[probe]})")
            ax.set(
                xlabel="Tau Normalization",
                ylabel="$\Delta \chi^2$",
                xlim=(0, 2),
                title = f"Chi2 profile for {reco} reco",
                ylim= (0, None)
            )
            ax.legend(prop=font, frameon=False)
            fig.savefig(os.path.join(save_path, f"Chi2Profile_{type}_{order}.png"))
            
def sigma_plots(
    type,
    path,
    probe,
    reco,
):
    
    # Define the mass ordering        
    ordering = ["NO", "IO"]
    
    # Define the font for legend
    font = font_manager.FontProperties(family='sans-serif', style='normal', size=12)
    
    print(f"\nPlotting sigma plots for {type}...")
    if type == "reconstruction":
        recos = ["MC", "AAFit", "NNFit"]
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        for reco, order in product(recos, ordering):
            data_fixed, data_free = load_chi2_data(reco, probe, order, path)
            ax.plot(data_fixed["TauNorm"], np.sqrt(data_fixed["chi2"]), 
                    'o--', linewidth=2, markersize=5, label=f"{reco} {order}")
        ax.axhline(y=3, linestyle='--', c = "black")
        ax.text(0.1, 3.15, "3$\sigma$ line",  fontsize=10)
        ax.axhline(y=5, linestyle='--', c = "black")
        ax.text(0.1, 5.15, "5$\sigma$ line", fontsize=10)
        ax.set(
            xlabel="Tau Normalization",
            ylabel="Significance ($\sigma$)",
            xlim=(0, 2),
            title = f"Sensitivity of Tau Normalization for different reconstructions",
            #yscale = "log"
        )
        ax.legend(prop=font, frameon=False)
        fig.savefig(os.path.join(save_path, f"SigmaPlots_{type}_{probe}.png"))
        
    elif type == "study":
        probes = ["STD", "TAU"]
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 8)) 
        for order, probe in product(ordering, probes):
            data_fixed, data_free = load_chi2_data(reco, probe, order, path)   
            ax.plot(data_fixed["TauNorm"], np.sqrt(data_fixed["chi2"]), 
                    'o--', linewidth=2, markersize=5, label=f"{probe} {order}")
        ax.set(
            xlabel="Tau Normalization",
            ylabel="Significance ($\sigma$)",
            xlim=(0, 2),
            title = f"Sensitivity of Tau Normalization for {reco} reco",
            ylim= (0, None)
        )
        ax.legend(prop=font, frameon=False)
        fig.savefig(os.path.join(save_path, f"SigmaPlots_{type}_{reco}.png"))
    elif type == "ordering":
        probes = ["STD", "TAU"]
        recos = ["MC", "AAFit", "NNFit"]
        
        for order in ordering:
            fig, ax = plt.subplots(1, 1, figsize=(10, 8)) 
            for reco, probe in product(recos, probes):
                data_fixed, data_free = load_chi2_data(reco, probe, order, path)   
                ax.plot(data_fixed["TauNorm"], np.sqrt(data_fixed["chi2"]), 
                        'o--', linewidth=2, markersize=5, label=f"{probe} {order}")
            ax.set(
                xlabel="Tau Normalization",
                ylabel="Significance ($\sigma$)",
                xlim=(0, 2),
                title = f"Sensitivity of Tau Normalization for {order} ordering",
                ylim= (0, None)
            )
            ax.legend(prop=font, frameon=False)
            fig.savefig(os.path.join(save_path, f"SigmaPlots_{type}_{order}.png"))



if __name__ == '__main__':
    
    args = ArgumentParser()
    type = args.type
    path = args.path
    reco = args.reco
    probe = args.probe
    save_path = args.save_path
    
    
    if type ==  "reconstruction":
        if probe is None:
            raise ValueError("Please provide the probe channel")
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
    plot_chi2(type, path, probe, reco, save_path)
    
    # Plotting the significance
    sigma_plots(type, path, probe, reco, save_path)
    
    
    