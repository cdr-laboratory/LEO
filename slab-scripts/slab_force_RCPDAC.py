from shutil import copyfile
import shutil,os,sys
import numpy as np

workdir = '../../LEO/genie-forcings/'

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
    ]
list3 = [
    '0p5'
    ,'1p0'
    ,'5p0'
    ,'10p0'
    ,'20p0'
    ,'40p0'
    ]
    
n1,n2,n3 = len(list1),len(list2),len(list3)


i =int(sys.argv[1])
    
for i1 in range(n1):
    for i2 in range(n2):
        for i3 in range(n3):
            slab = 's{:05d}'.format(i) 
            
            # src = workdir + 'worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP'+list1[i1]
            # dst = workdir + 'worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP'+list1[i1]+'_'+list3[i3]+'GtCO2'
            # src = workdir + 'worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP'+list1[i1]+'_R3mod_3'
            # dst = workdir + 'worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP'+list1[i1]+'_R3mod_3'+'_'+list3[i3]+'GtCO2'
            # src = workdir + 'worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP'+list1[i1]+'_R3mod_SLABt{:03d}_3'.format(test_i)
            # dst = workdir + 'worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP'+list1[i1]+'_R3mod_SLABt{:03d}_3'.format(test_i)+'_'+list3[i3]+'GtCO2'
            src = workdir + 'worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP' + list1[i1] +'_'+ slab +'.o'
            dst = workdir + 'worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP' + list1[i1] +'_'+ slab +'.o'+ '.DAC'+list3[i3]+'GtCO2'
            
            print(slab, list1[i1],)
            if os.path.isdir(src):
                pass
            else:
                print('source does not exist')
            
            # copyfile(src, dst)
            if not os.path.exists(dst): 
                shutil.copytree(src, dst)
            else:
                print (' *** CAUTION: FORCING has been created before')
                print (' ---> ACTION: remove old directory and create new one')
                shutil.rmtree(dst)
                shutil.copytree(src, dst)

            file_name = dst+'/biogem_force_flux_atm_pCO2_sig.dat'
            
            if os.path.isfile(file_name):
                pass
            else:
                print('target does not exist')
            
            line_mod = ''
            
            with open(file_name) as f:
            
                lines = f.read()
                for l in lines.split("\n"):
                    try: 
                        # print(float(l.split()[0]),float(l.split()[1]))
                        if float(l.split()[0] ) >= 2030:
                            line_mod += l.split()[0] + ' {:.7e}'.format(float(l.split()[1] ) - 2. * 0.1136363636363636E+15*float(list3[i3].replace('p','.'))/10.) + '\n'
                        else:
                            line_mod += l + '\n'
                    except: 
                        line_mod += l + '\n'
                    
                # data_lines = f.read()
        
            # if list2[i2]=='ESW':
                # data_lines = data_lines.replace(
                    # "rg_par_weather_CaSiO3=0.1136363636363636E+15                 # mol Ca2+ per year"
                    # , 'rg_par_weather_CaSiO3={:.7e}'.format(0.1136363636363636E+15*float(list3[i3].replace('p','.'))/10) 
                        # +  "                 # mol Ca2+ per year"
                    # )
            # if list2[i2]=='ECW':
                # data_lines = data_lines.replace(
                    # "rg_par_weather_CaSiO3=0.1136363636363636E+15                 # mol Ca2+ per year"
                    # ,"# rg_par_weather_CaSiO3=0.1136363636363636E+15                 # mol Ca2+ per year"
                    # )
                # data_lines = data_lines.replace(
                    # "rg_par_weather_CaCO3=0.949400E+13"
                    # , 'rg_par_weather_CaCO3={:.7e}'.format(0.949400E+13+0.1136363636363636E+15*float(list3[i3].replace('p','.'))/10) 
                        # +  "                 # mol Ca2+ per year"
                    # )
            # data_lines = data_lines.replace(
                # 'bg_par_forcing_name="worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP8p5"'
                # ,'bg_par_forcing_name="worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP'+list1[i1]+'"'
                # )

            with open(file_name, mode="w") as f:
                f.write(line_mod)
            