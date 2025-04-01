# Tau Neutrino Appearance with ANTARES
- - -

This repo contains the work that is accomplished with SWIM for the statistical analysis. This is the second repository of my Master's thesis containing everything that was calculated with Swim. 

## ReconstructionPerfomance
This folder contains a study for perfoming an analysis in the perfomance of the available reconstructions both availble from the AntDSTs and NNfit.

## CanDimension
In this folder, a 3D vector is added to the final datasample required for the compilation of the detector response matrix in case the object is not already there.

## Chi2Profile
This folder contains a sourcecode based on the example of Swim for the profile analysis. It computes the chi2 based on specific scenarios, both for smeared and unsmeared datasets.

## Smearing
The two smearing strategies employed during this analysis are stored, both the "flat-based" and "reconstruction-perfomance" strategies. Apart from the implementation of smearing, a parameterization of the NNFit perfomance is computed and plotted here.

## Plotter
This folder contains a plotter.py script for the visualization of the chi2 and significance plots for the various scenarios computed in the _Chi2Profile_ folder. 

Disclaimer: In this analysis, the presence of Swim is necessary

