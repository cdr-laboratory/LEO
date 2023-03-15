from shutil import copyfile
import os,sys
import numpy as np

# workdir = '../../cgenie.muffin/genie-userconfigs/'
workdir = '/storage/coda1/p-creinhard3/0/ykanzaki3/scripts/slab/data/'
    
bgdata_list = [
    'atm_pCO2'
    ,'ocn_DIC'
    ,'ocn_ALK'
    ,'atm_temp'
    ,'focnsed_POC'
    ,'focnsed_CaCO3'
    ,'fsedocn_DIC'
    ,'diag_weather_DIC'
    ,'carb_sur_pHsws'
    ,'carb_sur_ohm_cal'
    ,'carb_sur_ohm_arg'
    ,'misc_bio_CaCO3'
    ,'misc_bio_POC'
    ,'fseaair_pCO2'
    ,'diag_misc_specified_forcing_pCH4'
    ,'diag_misc_specified_forcing_pN2O'
    ]
    
acdata_list = [
    'terPOOl'
    ,'terFLX'
    ,'terPOOlg'
    ,'terFLXg'
    ]
    
# srcdir  = '../../cgenie_output/'
# workdir = './data/'
srcdir = '/storage/coda1/p-creinhard3/0/ykanzaki3/cgenie_output/'
# srcdir = '/storage/coda1/p-creinhard3/0/ykanzaki3/scripts/slab/data/'
# rcp conc. forcing 
dst = workdir + sys.argv[1]

os.system('mkdir -p  '+dst)
os.system('mkdir -p  '+dst +'/biogem/')
os.system('mkdir -p  '+dst +'/atchem/tem/')

for bgdata in bgdata_list:
    src = srcdir  + sys.argv[1] + '/biogem/biogem_series_' + bgdata + '.res'
    dst = workdir + sys.argv[1] + '/biogem/biogem_series_' + bgdata + '.res'

    if not os.path.isfile(src):
        os.system('tar -xzf '+'../../cgenie_archive/' + sys.argv[1]+'.tar.gz -C ../../cgenie_output')
    
    try:
        copyfile(src, dst)
    except:
        print(bgdata +' not in '+sys.argv[1] )

for acdata in acdata_list:
    src = srcdir  + sys.argv[1] + '/atchem/tem/' + acdata + '.res'
    dst = workdir + sys.argv[1] + '/atchem/tem/' + acdata + '.res'
    try:
        copyfile(src, dst)
    except:
        print(acdata +' not in '+sys.argv[1] )
                    
                    
                    