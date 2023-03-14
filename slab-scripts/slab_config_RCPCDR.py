from shutil import copyfile
import sys

workdir = '../../cgenie.muffin/genie-userconfigs/'

var1 = 'RCP'
var2 = 'CDR'
var3 = 'GtCO2'

list1 = [
    '2p6'
    ,'4p5'
    ,'6p0'
    ,'8p5'
    ]
list2 = [
    'ESW'
    ,'ECW'
    ,'DAC'
    ]
# list2 = [
    # 'ECW'
    # ]
list3 = [
    '0p5'
    ,'1p0'
    ,'5p0'
    ,'10p0'
    ,'20p0'
    ,'40p0'
    ]
    
n1,n2,n3 = len(list1),len(list2),len(list3)

test_i = int(sys.argv[1])

for i1 in range(n1):
    src = workdir + 's{:05d}'.format(test_i) + '.RCP'+list1[i1] +'.emis.o' 
    file_name = src
    
    
    with open(file_name) as f:
        for line in f:
            if 'rg_par_weather_CaCO3' not in line: 
                continue
            a = line.split()
            caco3 = float(a[0].replace('rg_par_weather_CaCO3=',''))
            print(caco3)
            break
            
    for i2 in range(n2):
        for i3 in range(n3):
            
            # src = workdir + 'SLAB_test_{:03d}.RCP'.format(test_i) + list1[i1] +'.emis' 
            src = workdir + 's{:05d}'.format(test_i) + '.RCP'+list1[i1] +'.emis.o' 
            # dst = workdir + 'SLAB_test_{:03d}.RCP'.format(test_i) + list1[i1] +'.emis.'  +list2[i2]+'.'+list3[i3]+'GtCO2'
            # dst = workdir + 'SLAB_test_{:03d}.RCP'.format(test_i) + list1[i1] +'.emis.'  +list2[i2]+'.'+list3[i3]+'GtCO2_v2'
            # dst = workdir + 's{:05d}'.format(test_i) + list1[i1] +'.emis.var.'  +list2[i2]+'.'+list3[i3]+'GtCO2_EN4'
            dst = workdir + 's{:05d}'.format(test_i) + '.RCP'+list1[i1] +'.emis.o.' +list2[i2]+list3[i3]+'GtCO2'

            copyfile(src, dst)

            file_name = dst
            
            with open(file_name) as f:
                data_lines = f.read()
        
            if list2[i2]=='ESW':
                data_lines = data_lines.replace(
                    "# --- DATA SAVING ----------------------------------------------"
                    , '# \n' 
                        + 'rg_par_weather_CaSiO3={:.7e}'.format(0.1136363636363636E+15*float(list3[i3].replace('p','.'))/10) 
                        +  " # mol Ca2+ per year" +'\n' 
                        + '#'+'\n' 
                        + '# --- DATA SAVING ----------------------------------------------'
                    )
            if list2[i2]=='ECW':
                # data_lines = data_lines.replace(
                    # "rg_par_weather_CaSiO3=0.1136363636363636E+15                 # mol Ca2+ per year"
                    # ,"# rg_par_weather_CaSiO3=0.1136363636363636E+15                 # mol Ca2+ per year"
                    # )
                data_lines = data_lines.replace(
                    "rg_par_weather_CaCO3="
                    # , 'rg_par_weather_CaCO3={:.7e}'.format(0.949400E+13 + 2 * 0.1136363636363636E+15*float(list3[i3].replace('p','.'))/10) 
                    , 'rg_par_weather_CaCO3={:.7e}'.format(caco3 + 2 * 0.1136363636363636E+15*float(list3[i3].replace('p','.'))/10) 
                        +  " # mol Ca2+ per year #"
                    )
            if list2[i2]=='DAC':
                # data_lines = data_lines.replace(
                    # "rg_par_weather_CaSiO3=0.1136363636363636E+15                 # mol Ca2+ per year"
                    # ,"# rg_par_weather_CaSiO3=0.1136363636363636E+15                 # mol Ca2+ per year"
                    # )
                data_lines = data_lines.replace(
                    'bg_par_forcing_name="worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP'+ list1[i1] +'_'+ 's{:05d}'.format(test_i) +'.o"'
                    ,'bg_par_forcing_name="worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP'+list1[i1] +'_'+ 's{:05d}'.format(test_i) +'.o'+ '.DAC'+list3[i3]+'GtCO2"'
                    # ,'bg_par_forcing_name="worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP'+list1[i1]+'_'+list3[i3]+'GtCO2'+'"'
                    )
            # else: 
                # data_lines = data_lines.replace(
                    # 'bg_par_forcing_name="worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP8p5"'
                    # ,'bg_par_forcing_name="worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP'+list1[i1]+'"'
                    # )
            data_lines = data_lines.replace(
                'bg_par_misc_t_start=1765.0'
                ,'bg_par_misc_t_start=2030.0'
                )
                
            # fine record
            # data_lines = data_lines.replace(
                # "bg_par_infile_sig_name='save_timeseries_historicalfuture_every1.dat'"
                # ,"bg_par_infile_sig_name='save_timeseries_historicalfuture_every1_YKMOD_v2.dat'\n" 
                    # + 'bg_par_data_save_sig_dt=0.1'
                # )

            # finer record
            # data_lines = data_lines.replace(
                # "bg_par_infile_sig_name='save_timeseries_historicalfuture_every1.dat'"
                # ,"bg_par_infile_sig_name='save_timeseries_historicalfuture_every1_YKMOD_v3.dat'\n" 
                    # + 'bg_par_data_save_sig_dt=0.05'
                # )
            data_lines = data_lines.replace(
                'ac_par_atm_slab_savedtyr='
                ,'ac_par_atm_slab_savedtyr=0.05 #'
                )

            with open(file_name, mode="w") as f:
                f.write(data_lines)
            
            
            
for i1 in range(n1):     
    # src = workdir + 'worjh2.ESW.S36x36.RCP8p5.emis.var.10GtCO2_BASE'
    # dst = workdir + 'worjh2.'+'CTRL'+'.S36x36.R3mod.RCP'+list1[i1]+'.emis.var.'+'0GtCO2_EN3'
    # src = workdir + 'SLAB_test_{:03d}_R3mod.RCP'.format(test_i) + list1[i1] +'.emis.var3' 
    # dst = workdir + 'SLAB_test_{:03d}_R3mod.RCP'.format(test_i) + list1[i1] +'.emis.var.'  +'CTRL'+'.'+'0GtCO2_EN4'
    src = workdir + 's{:05d}'.format(test_i) + '.RCP'+list1[i1] +'.emis.o' 
    dst = workdir + 's{:05d}'.format(test_i) + '.RCP'+list1[i1] +'.emis.o.CTRL0p0GtCO2'

    copyfile(src, dst)

    file_name = dst

    with open(file_name) as f:
        data_lines = f.read()

    data_lines = data_lines.replace(
        'bg_par_misc_t_start=1765.0'
        ,'bg_par_misc_t_start=2030.0'
        )
    # fine record
    # data_lines = data_lines.replace(
        # "bg_par_infile_sig_name='save_timeseries_historicalfuture_every1.dat'"
        # ,"bg_par_infile_sig_name='save_timeseries_historicalfuture_every1_YKMOD_v2.dat'\n" 
            # + 'bg_par_data_save_sig_dt=0.1'
        # )

    # finer record
    # data_lines = data_lines.replace(
        # "bg_par_infile_sig_name='save_timeseries_historicalfuture_every1.dat'"
        # ,"bg_par_infile_sig_name='save_timeseries_historicalfuture_every1_YKMOD_v3.dat'\n" 
            # + 'bg_par_data_save_sig_dt=0.05'
        # )
    data_lines = data_lines.replace(
        'ac_par_atm_slab_savedtyr='
        ,'ac_par_atm_slab_savedtyr=0.05 #'
        )

    with open(file_name, mode="w") as f:
        f.write(data_lines) 