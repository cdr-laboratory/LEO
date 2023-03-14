#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# LEO — A large-ensemble framework for evaluating the ocean response to CDR
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# --------------------------------------------------------------------------------
# REQUIREMENTS: 
# --------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------
# SUMMARY
# --------------------------------------------------------------------------------
#
# The core of LEO is a carbon-centric version of the Grid ENabled Integrated Earth 
# system model (cGENIE). cGENIE is classified as an intermediate complexity Earth 
# system model (ESMIC), and is built on a 3-D frictional-geostrophic ocean model 
# with extensive ocean/sediment biogeochemistry, a 2-D energy-moisture balance 
# model (EMBM) with simplified atmospheric chemistry, and a dynamic-thermodynamic 
# sea ice model. The basic structure and ocean-atmosphere physics can be found in:
#
#     [ Edwards and Marsh | 2005 | doi:10.1007/s00382-004-0508-8 ]
#     [ Marsh et al. | 2011 | doi:10.5194/gmd-4-957-2011 ] 
#
# The ocean biogeochemistry is described in: 
#
#     [ Ridgwell et al. | 2007 | doi:10.5194/bg-4-87-2007 ]
#     [ Ridgwell and Hargreaves | 2007 | doi:10.1029/2006GB002764 ]
#     [ Reinhard et al. | 2020 | doi:10.5194/gmd-2020-32 ] 
#
# Extensive documentation of the cGENIE code, including a manual detailing code 
# installation, basic model configuration, tutorials covering various aspects of 
# model configuration, experimental, design, and output, plus the processing of 
# results, can be found in: 
#
#     [ /github.com/derpycode/muffindoc ].
#
# LEO includes a simplified ("slab") terrestrial biosphere, in which primary
# production is controlled by atmospheric carbon dioxide abundance and soil
# respiration is controlled primarily by temperature. This is meant to capture
# the basic dynamics of exchange with a terrestrial carbon reservoir while 
# being computationally efficient and mechanistically transparent. The base 
# version of the slab biosphere is described and validated against modern 
# observations in:
#
#     [ Kanzaki et al. | 2023 | doi: ]
#
# This initial tagged release contains all base/user configuration files and 
# forcing files to reproduce the simulations presented in Kanzaki et al. [2023].
# Base configuration files can be found in:
#
#     LEO/
#        ├── genie-main/
#                ├── configs/
#                       ├── ...
#
# User configuration files can be found in:
#
#     LEO/
#        ├── genie-userconfigs/
#                 ├── ...
#
#
# A shell script for model spinup and historical/future transient simulations
# can be found in:
#
#     LEO/
#        ├── genie-main/
#                ├── slab_rcp_cdr.sh
#
# Future releases will contain additional upstream/downstream tools and wrappers 
# for implementing large ensembles and managing/processing output. 
# --------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------
# CTR | 2023-03-14
# --------------------------------------------------------------------------------
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#