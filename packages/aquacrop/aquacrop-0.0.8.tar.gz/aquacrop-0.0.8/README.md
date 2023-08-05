# AquaCrop-OS
> Python version of AquaCropOS 


## Install

`pip install aquacrop`

AquaCrop-OS, an open source version of FAO’s multi-crop model, AquaCrop. AquaCrop-OS was released in August 2016 and is the result of collaboration between researchers at the University of Manchester, Water for Food Global Institute, U.N. Food and Agriculture Organization, and Imperial College London.

AquaCropOS is an environment built for the design and testing of irrigation stratgeies. We are still in early development and so ensure you have downloaded the latest version.

It is built upon the AquaCropOS crop-growth model (written in Matlab `link`) which itself itself is based on the FAO AquaCrop model. Comparisons to both base models are shown in `link`

### to do:

 - allow crop rotation - compute crop calander at planting
 
 - jit complile groundwater functions
  
 - fix func docstrings
 
 - improve names - change class to struct
 
 - create struct for other FieldMngt, InitWC
 
 - tutorials (comparisson)
 
 - batch tutorials
 
 - tut: optimisation
 
 - tut: calibration
 
 - tut: custom irrigation decisions
 
 - env.gym style wrapper
 
 - add a display_full_outputs arg so we dont create a pandas dataframe after each model end
 
 - add all calibrated crops and test
  
 - add __repr__
 
 - add export and import crop feature
 
 - add test for irrigation

