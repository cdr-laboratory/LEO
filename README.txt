#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# LEO — A large-ensemble framework for evaluating the ocean response to CDR
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# ----------------------------------------------------------------------------------
# SUMMARY
# ----------------------------------------------------------------------------------
#
# The core of LEO is a carbon-centric version of the Grid ENabled Integrated Earth 
# system model (cGENIE). cGENIE is classified as an intermediate complexity Earth 
# system model (ESMIC), and is built on a 3-D frictional-geostrophic ocean model 
# with extensive ocean/sediment biogeochemistry, a 2-D energy-moisture balance 
# model (EMBM) with simplified atmospheric chemistry, and a dynamic-thermodynamic 
# sea ice model. The basic structure and ocean-atmosphere physics can be found in:
#
#     [ -------------------------------------------------------- ]
#     [ Edwards and Marsh | 2005 | doi:10.1007/s00382-004-0508-8 ]
#     [ Marsh et al.      | 2011 | doi:10.5194/gmd-4-957-2011    ] 
#     [ -------------------------------------------------------- ]
#
# The ocean biogeochemistry is described in: 
#
#     [ --------------------------------------------------------- ]
#     [ Ridgwell et al. | 2007 | doi:10.5194/bg-4-87-2007         ]
#     [ Ridgwell and Hargreaves | 2007 | doi:10.1029/2006GB002764 ]
#     [ Reinhard et al. | 2020 | doi:10.5194/gmd-2020-32          ]
#     [ --------------------------------------------------------- ]
#
# Extensive documentation of the cGENIE code, including a manual detailing code 
# installation, basic model configuration, tutorials covering various aspects of 
# model configuration, experimental, design, and output, plus the processing of 
# results, can be found in: 
#
#     [ ------------------------------- ]
#     [ /github.com/derpycode/muffindoc ]
#     [ ------------------------------- ]
#
# LEO includes a simplified ("slab") terrestrial biosphere, in which primary
# production is controlled by atmospheric carbon dioxide abundance and soil
# respiration is controlled primarily by temperature. This is meant to capture
# the basic dynamics of exchange with a terrestrial carbon reservoir while 
# being computationally efficient and mechanistically transparent. The base 
# version of the slab biosphere is described and validated against modern 
# observations in:
#
#     [ ---------------------------- ]
#     [ Kanzaki et al. | 2023 | doi: ]
#     [ ---------------------------- ]
#
# ----------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------
# CONFIGURATION | FORCING | DISCRETE SIMULATIONS
# ----------------------------------------------------------------------------------
#
# This initial tagged release contains all base configuration files and a basic 
# set of user configuration and forcing files needed to reproduce the 
# simulations presented in Kanzaki et al. [2023]. Base configuration files 
# can be found in:
#
#     [ ------------------------------------------------------------ ]
#     [ LEO/                                                         ]
#     [   ├── genie-main/                                            ]
#     [            ├── configs/                                      ]
#     [                    ├── muffin.CBSR.worjh2.ESW.S36x36.config  ]
#     [ ------------------------------------------------------------ ]
#
# User configuration and forcing files are created while performing a large 
# ensemble set of experiments. Template user configuration files from which 
# a large ensemble can be built are found in:
#
#     [ ------------------------------------ ]
#     [ LEO/                                 ]                        
#     [   ├── genie-userconfigs/             ]
#     [               ├── slab_spin1p5_done/ ]
#     [                           ├── ...    ]
#     [                           ├── ...    ]
#     [                           ├── ...    ]
#     [ ------------------------------------ ]
#
# A series of Python scripts for making user configuration files and forcings
# as well as managing output data for large ensembles can be found in:
#
#     [ ------------------- ] 
#     [ LEO/                ]
#     [   ├── slab-scripts/ ]
#     [             ├── ... ]
#     [ ------------------- ] 
#
# Shell scripts for model spinup and historical/future transient simulations
# (and ensembles) can be found in:
#
#     [ ------------------------------ ] 
#     [ LEO/                           ]
#     [   ├── genie-main/              ]
#     [            ├── slab_rcp_cdr.sh ]
#     [            ├── slab_loop.sh    ]
#     [ ------------------------------ ] 
#
# ----------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------
# WORKFLOW FOR LARGE ENSEMBLE SETS
# ----------------------------------------------------------------------------------
#
#
# Workflow for a discrete CDR simulation with a given slab biosphere parameter set
#
#    [ -------------------------------------------------------------------------- ]
#    [ 1. Spin-up with closed sediment               (SPIN1)                      ]
#    [ 2. Spin-up with open sediment                 (SPIN2 restart from SPIN1)   ]
#    [ 3. Concentration forcing under RCP scenario   (conc.o restart from SPIN2)  ]
#    [ 4. Emission forcing under RCP scenario        (emis.o restart from SPIN2)  ]
#    [ 5. Historical transient                       (hist.o restart from SPIN2)  ] 
#    [ 6. CDR run (including CTRL without CDR)       (DAC/ESW/ECW.emis.o.XGtCO2   ]
#    [                                                restart from hist.o         ]
#    [                                                where X is deployment rate) ]
#    [ -------------------------------------------------------------------------- ]
#
# A single series (1-6 above) for one slab parameter set is run using:
#
#     [ --------------------------- ]
#     [ /genie-main/slab_rcp_cdr.sh ]
#     [ --------------------------- ]
#
# A simulation ensemble is run by repeatedly executing:
#
#     [ --------------------------- ]
#     [ /genie-main/slab_loop.sh    ]
#     [ --------------------------- ]
#
# Slab biosphere parameter sets that pass screening are saved in:
#
#     [ ------------------------------------------- ]
#     [ /slab-scripts/2nd_pass_compile.save_allemis ]
#     [ ------------------------------------------- ]
#
# NOTE: Because of the quantity of data produced by the full ensemble 
#       (~980 slab parameter sets, 6 deployment rates, 3 CDR schemes, 4 RCP scenarios, 
#       in addition to control and historical transients and 2 forcing and 2 spin-up 
#       runs for each individual RCP), this tagged release includes Python scripts 
#       (run with Python3) that can be used to make user configuration and forcing 
#       files for the large ensemble reported in Kanzaki et al. [2023].
#
# NOTE: Shell and Python scripts are designed such that completed runs that are no 
#       longer needed are removed from the output directory ('outputdir2' in 
#       slab_rcp_cdr.sh) with archived files being stored in a different directory 
#       ('archdir2' in slab_rcp_cdr.sh) than the archive directory saved by cGENIE in 
#       the default setting ('archdir1' in slab_rcp_cdr.sh), while extracted results 
#       files relevant for global C budget calculations are stored in another 
#       directory ('workdir' in slab_x_data.py).
#
# ----------------------------------------------------------------------------------
# 
# ----------------------------------------------------------------------------------
# IMPLEMENTING PYTHON AND SHELL SCRIPTS
# ----------------------------------------------------------------------------------
#
#   1. Create directory /scripts in the same level as LEO (not as its subdirectory) 
#      and create a subdirectory /scripts/slab/ and subsubdirectory /scripts/slab/data 
#         
#      For instance:
#         [ --------------- ]
#         [ $ cd ~          ]
#         [ $ mkdir scripts ]
#         [ $ cd scripts    ]
#         [ $ mkdir slab    ]
#         [ $ cd slab       ]
#         [ $ mkdir data    ]
#         [ --------------- ]
#
#   2. Copy all the files in /LEO/slab-scripts to /scripts/slab:
#
#         [ ------------------------- ]
#         [ $ cd ~/LEO/slab-scripts   ]
#         [ $ cp ./* ../scripts/slab/ ]
#         [ ------------------------- ]
#    
#   3. Modify directory names in 3 scripts (slab_rcp_cdr.sh and slab_loop.sh in 
#      ~/LEO/genie-main/ and slab_x_data.py in ~/scripts/slab/):
#
#            [ ------------------- ]
#      (3-1) [ In slab_rcp_cdr.sh: ]
#            [ ------------------- ]
#              Modify 'homedir1' and 'homedir2' (L3-4)
#                -- 'homedir2' should be the directory where /LEO/ and /scripts/ 
#                   are located so that 'outputdir2' and 'archdir2' are typical 
#                   cGENIE output and archive directories
#                -- 'homedir1' can be either the same as or different from 
#                   'homedir2' so that 'archdir1' can be any storage place for 
#                   archived runs
#
#            [ ---------------- ]
#      (3-2) [ In slab_loop.sh: ]
#            [ ---------------- ]
#              Modify 'homedir2' (L3) 
#                -- 'homedir2' should be the directory where /LEO/ and /scripts/ 
#                   are located so that 'pydir' corresponds to ~/scripts/slab/
#
#            [ ------------------ ]
#      (3-3) [ In slab_x_data.py: ]
#            [ ------------------ ]
#              Modify 'workdir' (L6) and 'srcdir' (L36) 
#                -- 'workdir' should correspond to ~/scripts/slab/data/ created in 
#                   Step 1 above 
#                -- 'srcdir' should correspond to 'outputdir2' in Step (3-1) 
#
#   4. Run the ensemble:
#         [ ---------------- ]
#         [ $ ./slab_loop.sh ]
#         [ ---------------- ]
# 
# NOTE: One can also test a series of run for one slab parameter set by:
#         [ --------------------- ]
#         [ $ ./slab_rcp_cdr.sh Y ]
#         [ --------------------- ]
#       where Y is the ID of slab parameter set. 
#
# ----------------------------------------------------------------------------------
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#