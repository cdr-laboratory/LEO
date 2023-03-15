import numpy as np 
from shutil import copyfile
import shutil,os,sys

def force_conc2flx(workdir,src,dst,flxsimname):

    if not os.path.exists(dst): 
        shutil.copytree(src, dst)
    else:
        print (' *** CAUTION: FORCING has been created before')
        print (' ---> ACTION: remove old directory and create new one')
        shutil.rmtree(dst)
        shutil.copytree(src, dst)
    
    print (dst)
    
    file_name = dst+'/configure_forcings_atm.dat'

    with open(file_name) as f:
        data_lines = f.read()
        
    data_lines = data_lines.replace(
          " 03  t  0.1  f  t  F   2  01  01  '[carbon dioxide (CO2) partial pressure (atm)]'"
        , " 03  f  0.1  t  t  F   2  01  01  '[carbon dioxide (CO2) partial pressure (atm)]'"
        )

    with open(file_name, mode="w") as f:
        f.write(data_lines)
    
    file_name  = '../../cgenie_output/'
    file_name += flxsimname
    file_name += '/biogem/biogem_series_diag_misc_specified_forcing_pCO2.res'
    
    try:
        data = np.loadtxt(file_name,skiprows = 1)
    except: 
        print('****** forcing could not be found in conc forcing run *******\n'
            +file_name+'\n\n\n\n\n\n\n\n\n')
        return
    
    file_name = dst+'/biogem_force_flux_atm_pCO2_sig.dat'
    
    with open(file_name, mode="w") as f:
        f.write('-START-OF-DATA-'+'\n')
        f.write('0.0 {:.7e}\n'.format(data[0,1]))
        for i in range(data.shape[0]):
            f.write('{:.4f} '.format(data[i,0]) + '{:.7e}\n'.format(data[i,1]))
        
        f.write('999999999.0 {:.7e}\n'.format(data[-1,1]))
        f.write('-END-OF-DATA-')
        
    
    file_name = dst+'/biogem_force_restore_atm_pCO2_sig.dat'
    if os.path.exists(file_name): os.remove(file_name)
    
def main():

    workdir = '../../LEO/genie-forcings/'

    rcps = ['2p6','4p5','6p0','8p5']
    # rcps = ['2p6']
    # rcps = ['8p5']
    
    i = int(sys.argv[1])
    
    slab = 's{:05d}'.format(i) 
    
    rcpsp = sys.argv[2]
    
    for rcp in rcps:
        if rcpsp not in rcp: continue
        print(rcp,rcpsp)
        src = workdir + 'worjh2.detSED.RpCO2.RpO2.RpCH4.RpN2O.RCP' + rcp
        dst = workdir + 'worjh2.detSED.FpCO2.RpO2.RpCH4.RpN2O.RCP' + rcp +'_'+ slab + '.o' 
        flxsimname =  slab + '.RCP'+rcp+'.conc.o'
        force_conc2flx(workdir,src,dst,flxsimname)

if __name__ == '__main__':
    main()
