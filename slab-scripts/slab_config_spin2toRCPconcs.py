from shutil import copyfile
import numpy as np
import sys

workdir = '../../cgenie.muffin/genie-userconfigs/'



rcps = ['RCP2p6','RCP4p5','RCP6p0','RCP8p5']

    
i = int(sys.argv[1])

rcpsp = sys.argv[2]

print ('{:05d}'.format(i))

# src = workdir + 'SLAB_test_{:03d}'.format(i) + '.SPIN2'
# src = workdir + 'SLAB_cmip5_{:03d}'.format(i) + '.SPIN2'
src = workdir + 's{:05d}'.format(i) + '.SPIN2'
                
for rcp in rcps:
    
    if rcpsp not in rcp: continue
    
    print(rcp,rcpsp)

    # rcp conc. forcing 
    dst = workdir + 'SLAB_cmip5_{:03d}'.format(i) + '.'+rcp
    dst = workdir + 's{:05d}'.format(i) + '.'+rcp+'.conc.o'
    # dst = workdir + 's{:05d}'.format(i) + '.'+rcp+'.emis'

    copyfile(src, dst)
    
    file_name = dst
    
    with open(file_name) as f:
        data_lines = f.read()
    
    data_lines = data_lines.replace(
        "ac_par_atm_slab_restart=.false."
        ,"ac_par_atm_slab_restart=.true."
        ) 
    
    data_lines = data_lines.replace(
        "# ac_par_atm_slab_savedtyr=100.0"
        , "ac_par_atm_slab_savedtyr=1.0" 
        )
    data_lines = data_lines.replace(
        "# ac_par_atm_slab_ss_dtyr=1.0"
        , "ac_par_atm_slab_ss_dtyr=0.0"
        )
        
    data_lines = data_lines.replace(
        "bg_par_infile_slice_name='save_timeslice_NONE.dat'"
        ,"# bg_par_infile_slice_name='save_timeslice_NONE.dat'"
        )
    
    data_lines = data_lines.replace(
        "bg_par_data_save_level=10"
        ,"bg_par_data_save_level=10\n"
        +"bg_par_infile_slice_name='save_timeslice_historicalfuture_FINE.dat'" + "\n"
        +"bg_par_infile_sig_name='save_timeseries_historicalfuture_every1_YKMOD_v3.dat'" + "\n"
        +"bg_par_data_save_sig_dt=0.05"
        )
    
    data_lines = data_lines.replace(
        "bg_ctrl_data_save_slice_diag="
        ,"# bg_ctrl_data_save_slice_diag="
        )
    data_lines = data_lines.replace(
        "bg_ctrl_data_save_slice_misc="
        ,"# bg_ctrl_data_save_slice_misc="
        )
    data_lines = data_lines.replace(
        "bg_ctrl_bio_remin_redox_save="
        ,"# bg_ctrl_bio_remin_redox_save="
        )
    if 'conc' in dst:
        data_lines = data_lines.replace(
            "bg_par_forcing_name="
            ,'bg_par_forcing_name="worjh2.detSED.RpCO2.RpO2.RpCH4.RpN2O.'+rcp+'"' + ' #'
            # ,'bg_par_forcing_name="worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.'+rcp+'_'+'s{:05d}'.format(i) + '"' + ' #'
            )
    elif 'emis' in dst:
        data_lines = data_lines.replace(
            "bg_par_forcing_name="
            # ,'bg_par_forcing_name="worjh2.detSED.RpCO2.RpO2.RpCH4.RpN2O.'+rcp+'"' + ' #'
            ,'bg_par_forcing_name="worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.'+rcp+'_'+'s{:05d}'.format(i) + '"' + ' #'
            )
    
    data_lines = data_lines.replace(
        "bg_par_atm_force_scale_val_3="
        ,"# bg_par_atm_force_scale_val_3="
        )
    data_lines = data_lines.replace(
        "bg_par_atm_force_scale_val_10="
        ,"# bg_par_atm_force_scale_val_10="
        )
    data_lines = data_lines.replace(
        "bg_par_atm_force_scale_val_14="
        ,"# bg_par_atm_force_scale_val_14="
        )
    data_lines = data_lines.replace(
        "bg_ocn_init_25="
        ,"# bg_ocn_init_25="
        )
    
    data_lines = data_lines.replace(
        "bg_ocn_init_50=5.282E-02            # Mg [mol/kg]"
        ,"bg_ocn_init_50=5.282E-02            # Mg [mol/kg]" +"\n"
        +"#" +"\n"
        +"# --- MISC -----------------------------------------------------" +"\n"
        +"#" +"\n"
        +"# change start year" +"\n"
        +"bg_par_misc_t_start=1765.0" +"\n"
        +"#" 
        )
        
        

    with open(file_name, mode="w") as f:
        f.write(data_lines)
                