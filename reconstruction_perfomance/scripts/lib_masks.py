def get_trackmask(df):
    cc_ma = df["is_cc"] == True
    numu_ma = abs(df["type"]) == 14

    track_tau = df["interaction_type"] == 2
    tau_ma = abs(df["type"]) == 16

    track_ma = (cc_ma & numu_ma) | (track_tau & tau_ma)

    return track_ma


def get_showermask_cc(df):
    nue_mask = get_nuemask(df)
    nutau_mask = get_nutaumask(df)

    CCshower = df["interaction_type"] == 3 
    is_cc = df["is_cc"] == True

    shower_cc = (nue_mask | nutau_mask & CCshower) & is_cc
    
    return shower_cc

def get_showermask_nc(df):
    nue_mask =  get_nuemask(df)
    numu_mask = get_numumask(df)
    nutau_mask =  get_nutaumask(df)
    nu_mask = nue_mask | numu_mask | nutau_mask

    nc_ma = (df["is_cc"] == False) & nu_mask

    return nc_ma 
        
def get_nutaumask(df):
    nutau_mask = abs(df["type"]) == 16

    return nutau_mask

def get_numumask(df):
    numu_mask = abs(df["type"]) == 14

    return numu_mask

def get_nuemask(df):
    nue_mask = abs(df["type"]) == 12

    return nue_mask

def get_low_energymask(df):
    low_energy = (df["energy_true"] < 100)  & (df["energy_true"] > 10)

    return low_energy

def get_region(df):
    energy_region = (df["energy_true"] < 40)  & (df["energy_true"] > 20)

    return energy_region

def get_upgoingmask(df):
    upgoing = df["cos_zenith_true"] < 0

    return upgoing

def get_runmask(rdur):
    return "short run" if (rdur * 365.25 * 24) < 3 else "long run"

def get_cutrun(df):
    run_mask = df["run_id"] > 34348 #no tau production beforehand

    return run_mask
