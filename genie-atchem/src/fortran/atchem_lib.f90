! ******************************************************************************************************************************** !
! atchem_lib.f90
! Atmosphere Chemistry
! LIBRARY MODULE
! ******************************************************************************************************************************** !


MODULE atchem_lib


  use genie_control
  use gem_util
  use gem_carbchem
  IMPLICIT NONE
  SAVE


  ! ****************************************************************************************************************************** !
  ! *** NAMELIST DEFINITIONS ***************************************************************************************************** !
  ! ****************************************************************************************************************************** !

  ! ### EDIT ADD AND/OR EXTEND NAME-LIST PARAMETER AND CONTROL OPTIONS ########################################################### !
  ! ------------------- TRACER INITIALIZATION ------------------------------------------------------------------------------------ !
  REAL,DIMENSION(n_atm)::atm_init                              ! atmosphere tracer array initial values
  NAMELIST /ini_atchem_nml/atm_init
  REAL,DIMENSION(n_atm)::atm_dinit                             ! atmosphere tracer array restart perturbation values
  NAMELIST /ini_atchem_nml/atm_dinit
  logical::ctrl_atm_dinit                                      ! absolute (not relative) tracer re-start adjustment?
  NAMELIST /ini_atchem_nml/ctrl_atm_dinit
  ! ------------------- COSMOGENIC & RADIOGENIC PRODUCTION  ---------------------------------------------------------------------- !
  real::par_atm_F14C                                           ! Global cosmogenic production rate of 14C (mol yr-1)
  NAMELIST /ini_atchem_nml/par_atm_F14C
  ! ------------------- ATMOSPHERIC PHOTOCHEMISTRY --------------------------------------------------------------------------------!
  CHARACTER(len=63)::par_atm_CH4_photochem                     ! Atmospheric photochemical scheme ID string (e.g., golblatt, claire)
  NAMELIST /ini_atchem_nml/par_atm_CH4_photochem
  real::par_pCH4_oxidation_C0                                  ! Baseline atmospheric pCH4 (atm)
  NAMELIST /ini_atchem_nml/par_pCH4_oxidation_C0
  real::par_pCH4_oxidation_tau0                                ! Baseline CH4 lifetime (yr)
  NAMELIST /ini_atchem_nml/par_pCH4_oxidation_tau0
  real::par_pCH4_oxidation_N                                   ! Exponent for CH4 lifetime (dimensionless)
  NAMELIST /ini_atchem_nml/par_pCH4_oxidation_N
  real::par_atm_pO2_fixed                                      ! Atmospheric pO2 for fixed fixed scheme
  NAMELIST /ini_atchem_nml/par_atm_pO2_fixed
  ! ------------------- EMISSIONS-TO-ATMOSPHERE ---------------------------------------------------------------------------------- !
  real::par_atm_wetlands_FCH4                                  ! Wetlands CH4 flux (mol yr-1) 
  real::par_atm_wetlands_FCH4_d13C                             ! Wetlands CH4 d13C (o/oo) 
  NAMELIST /ini_atchem_nml/par_atm_wetlands_FCH4,par_atm_wetlands_FCH4_d13C
  ! ------------------- SLAB BIOSPHERE ------------------------------------------------------------------------------------------- !
  real::par_atm_slabbiosphere_C                                  ! 
  real::par_atm_slabbiosphere_C_d13C                             ! 
  NAMELIST /ini_atchem_nml/par_atm_slabbiosphere_C,par_atm_slabbiosphere_C_d13C
  real::par_atm_FterrCO2exchange          ! 
  NAMELIST /ini_atchem_nml/par_atm_FterrCO2exchange
  logical::par_atm_slabON                                      ! box model for terrestrial biosphere
  logical::par_atm_slabsave                                    ! crude saving of box terrestrial biosphere
  logical::par_atm_slab_restart                                ! restart from a previous run 
  logical::par_atm_slab_hetero                                 ! do heterogeneous calculation  
  logical::par_atm_slab_inclPolar                                  ! include Antarctica and Greenland on land mask
  NAMELIST /ini_atchem_nml/par_atm_slabON,par_atm_slabsave,par_atm_slab_restart,par_atm_slab_hetero,par_atm_slab_inclPolar
  real::par_atm_slab_Fnpp0                                      ! NPP const (PgC yr-1)
  real::par_atm_slab_B                                          ! NPP pCO2 dependence 
  real::par_atm_slab_pCO2ref                                    ! NPP reference pCO2 (ppm)
  real::par_atm_slab_tau                                        ! turnover year for vegitation
  real::par_atm_slab_gamma                                      ! decay const (yr-1) for SOM
  real::par_atm_slab_Q10                                        ! temperature dependence in Q10
  NAMELIST /ini_atchem_nml/par_atm_slab_Fnpp0,par_atm_slab_B,par_atm_slab_tau,par_atm_slab_gamma,par_atm_slab_Q10,par_atm_slab_pCO2ref
  real::par_atm_slab_tau0                                       ! tau (yr) as function of vegi amount (intercept)
  real::par_atm_slab_dtaudvegi                                  ! tau (yr) as function of vegi amount (slope)
  NAMELIST /ini_atchem_nml/par_atm_slab_dtaudvegi,par_atm_slab_tau0
  real::par_atm_slab_savedtyr                                   ! time interval for SOM data storage
  real::par_atm_slab_ss_dtyr                                    ! time duration assuming steady state
  NAMELIST /ini_atchem_nml/par_atm_slab_savedtyr,par_atm_slab_ss_dtyr 
  ! ------------------- RUN CONTROL ---------------------------------------------------------------------------------------------- !
  logical::ctrl_continuing                                     ! continuing run?
  NAMELIST /ini_atchem_nml/ctrl_continuing
  ! ------------------- I/O DIRECTORY DEFINITIONS -------------------------------------------------------------------------------- !
  CHARACTER(len=255)::par_pindir_name                           ! 
  CHARACTER(len=255)::par_indir_name                           ! 
  CHARACTER(len=255)::par_outdir_name                          ! 
  CHARACTER(len=255)::par_rstdir_name                          ! 
  NAMELIST /ini_atchem_nml/par_indir_name,par_outdir_name,par_rstdir_name,par_pindir_name
  CHARACTER(len=127)::par_infile_name,par_outfile_name         ! 
  NAMELIST /ini_atchem_nml/par_infile_name,par_outfile_name
  ! ------------------- DATA SAVING: MISC ---------------------------------------------------------------------------------------- !
  LOGICAL::ctrl_ncrst                                          ! restart as netCDF format?
  NAMELIST /ini_atchem_nml/ctrl_ncrst
  CHARACTER(len=127)::par_ncrst_name                           ! 
  NAMELIST /ini_atchem_nml/par_ncrst_name
  ! ------------------- DEBUGGING OPTIONS ---------------------------------------------------------------------------------------- !
  LOGICAL::ctrl_debug_lvl1                                       ! report 'level #1' debug?
  NAMELIST /ini_atchem_nml/ctrl_debug_lvl1 
  ! ############################################################################################################################## !


  ! ****************************************************************************************************************************** !
  ! *** MODEL CONFIGURATION CONSTANTS ******************************************************************************************** !
  ! ****************************************************************************************************************************** !

  ! *** array dimensions ***
  ! grid dimensions
  INTEGER,PARAMETER::n_i                                  = ilon1_atm ! 
  INTEGER,PARAMETER::n_j                                  = ilat1_atm ! 
  ! grid properties array dimensions 
  INTEGER,PARAMETER::n_phys_atm                           = 15    ! number of grid properties descriptors

  ! *** array index values ***
  ! atmosperhic 'physics' properties array indices
  INTEGER,PARAMETER::ipa_lat                              = 01    ! latitude (degrees) [mid-point]
  INTEGER,PARAMETER::ipa_lon                              = 02    ! longitude (degrees) [mid-point]
  INTEGER,PARAMETER::ipa_dlat                             = 03    ! latitude (degrees) [width]
  INTEGER,PARAMETER::ipa_dlon                             = 04    ! longitude (degrees) [width]
  INTEGER,PARAMETER::ipa_latn                             = 05   ! latitude (degrees) [north edge]
  INTEGER,PARAMETER::ipa_lone                             = 06   ! longitude (degrees) [east edge]
  INTEGER,PARAMETER::ipa_hmid                             = 07    ! height (m) [mid-point]
  INTEGER,PARAMETER::ipa_dh                               = 08    ! height (m) [thickness]
  INTEGER,PARAMETER::ipa_hbot                             = 09    ! height (m) [bottom]
  INTEGER,PARAMETER::ipa_htop                             = 10    ! height (m) [top]
  INTEGER,PARAMETER::ipa_A                                = 11    ! area (m2)
  INTEGER,PARAMETER::ipa_rA                               = 12    ! reciprocal area (to speed up numerics)
  INTEGER,PARAMETER::ipa_V                                = 13    ! atmospheric box volume (m3)
  INTEGER,PARAMETER::ipa_rV                               = 14    ! reciprocal volume (to speed up numerics)
  INTEGER,PARAMETER::ipa_P                                = 15    ! pressure (atm)

  ! *** array index names ***
  ! atmosphere interface 'physics'
  CHARACTER(len=16),DIMENSION(n_phys_atm),PARAMETER::string_phys_atm = (/ &
       & 'lat             ', &
       & 'lon             ', &
       & 'dlat            ', &
       & 'dlon            ', &
       & 'latn            ', &
       & 'lone            ', &
       & 'hmid            ', &
       & 'dh              ', &
       & 'hbot            ', &
       & 'htop            ', &
       & 'A               ', &
       & 'rA              ', &
       & 'V               ', &
       & 'rV              ', &
       & 'P               ' /)

  ! *** miscellaneous ***
  ! effective thickness of atmosphere (m) in the case of a 1-cell thick atmosphere
  ! NOTE: was 8000.0 m in Ridgwell et al. [2007]
  REAL,parameter::par_atm_th = 7777.0

  ! *********************************************************
  ! *** GLOBAL VARIABLE AND RUN-TIME SET PARAMETER ARRAYS ***
  ! *********************************************************

  ! *** PRIMARY ATCHEM ARRAYS ***
  real,dimension(n_atm,n_i,n_j)::atm                           ! 
  real,dimension(n_atm,n_i,n_j)::fatm                          ! 
  real,dimension(n_phys_atm,n_i,n_j)::phys_atm                 ! 

  ! *** Miscellanenous ***
  !
  real,dimension(n_atm,n_i,n_j)::atm_slabbiosphere             ! 
  real,dimension(n_i,n_j)::slab_frac_vegi                      ! YK added 02.08.2021
  integer,dimension(n_i,n_j)::slab_landmask                    ! YK added 08.20.2021
  real::slab_time_cnt                                          ! YK added 02.08.2021
  real::slab_time_cnt2                                         ! YK added 02.08.2021
  real::slab_int_avSLT                                         ! YK added 08.23.2021
  real::slab_int_t                                             ! YK added 09.20.2021 integrate time
  real::slab_int_vegiC                                         ! YK added 09.20.2021 integrate inventory (vegi and soil C)
  real::slab_int_soilC                                         ! YK added 09.20.2021 integrate inventory (vegi and soil C)
  real::slab_int_resp                                          ! YK added 09.20.2021 integrate respiration and productivity
  real::slab_int_prod                                          ! YK added 09.20.2021 integrate respiration and productivity
  integer::utest                                               ! YK added 02.12.2021
  ! netCDF and netCDF restart parameters
  CHARACTER(len=31)::string_rstid                              ! 
  CHARACTER(len=7) ::string_ncrunid                            ! 
  CHARACTER(len=254) ::string_ncrst                            ! 
  integer::ncrst_ntrec                                         ! count for netcdf datasets
  integer::ncrst_iou                                           ! io for netcdf restart
  
  ! *** copies of GOLDSTEIn variables ***
  ! miscellaneous
  REAL,DIMENSION(0:n_j)::goldstein_c                             !
  REAL,DIMENSION(0:n_j)::goldstein_cv                            !
  REAL,DIMENSION(0:n_j)::goldstein_s                             !
  REAL,DIMENSION(0:n_j)::goldstein_sv                            !


END MODULE atchem_lib

