from shutil import copyfile
import numpy as np
import sys

workdir = '../../cgenie.muffin/genie-userconfigs/'

rcps = ['RCP2p6','RCP4p5','RCP6p0','RCP8p5']

i = int(sys.argv[1])
    
print ('{:05d}'.format(i))

rcpsp = sys.argv[2]
                
for rcp in rcps:

    if rcpsp not in rcp: continue
    
    print(rcp,rcpsp)

    # rcp conc. forcing 
    src = workdir + 's{:05d}'.format(i) + '.'+rcp+'.emis.o'
    dst = workdir + 's{:05d}'.format(i) + '.'+rcp+'.hist.o'

    copyfile(src, dst)
    
    file_name = dst
    
    with open(file_name) as f:
        data_lines = f.read()
    
    data_lines = data_lines.replace(
        "ac_par_atm_slab_savedtyr=1.0"
        ,"ac_par_atm_slab_savedtyr=0.05"
        ) 
    
        
        

    with open(file_name, mode="w") as f:
        f.write(data_lines)
                