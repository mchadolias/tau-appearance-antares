import matplotlib.pyplot as plt
import seaborn as sns
import uproot
import os

def _root_to_tables(root_file, tree_name = "outTree", columns = ["chi2","TauNorm"]):
    
    # Load the root file
    with uproot.open(root_file) as f:
        data = f[tree_name].arrays(columns, library="numpy")
    
    return data

def plot_chi2(
    data_free,
    data_fixed,
    save_path,
    order,
    ):
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.plot(data_fixed["TauNorm"], data_fixed["chi2"]-data_free["chi2"], "o" label=f"{order} Ordering")
    ax.set(
        xlabel="Tau Normalization",
        ylabel="$\chi^2$ value",
        xlim=(0, 2)
    )
    ax.legend()
    fig.savefig(os.path.join(save_path, f"Chi2Profile_TauNorm_STD_{order}.png"))
    

if __name__ == '__main__':
    
    # Load the data
    directory = "/sps/km3net/users/mchadoli/master_thesis/tau_appearance/Chi2Profile/output/ANTARES/MC"
    save_path = "/sps/km3net/users/mchadoli/master_thesis/tau_appearance/Chi2Profile/plots"
    
    ordering = ["NO", "IO"]
    
    for order in ordering:
        print(f"=============== Loading {order} Ordering ===============")
        data_free = _root_to_tables(os.path.join(directory, "STD", order, f"free/Chi2Profile_TauNorm_STD_{order}_free_FitTwoOctants.root"))
        data_fixed = _root_to_tables(os.path.join(directory, "STD", order, f"fixed/Chi2Profile_TauNorm_STD_{order}_fixed_FitTwoOctants.root"))
        
        print(f"=============== Plotting {order} Ordering ===============")
        plot_chi2(data_free, data_fixed, save_path, order)
        
    print("=============== Plotting Chi2 Profile Done ===============")
                                                 

                                                 
    
    
    
    
    
    
    