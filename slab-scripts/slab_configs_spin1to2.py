from shutil import copyfile
import sys 

def make_configs(src,dst,inlist,replacelist):
    
    copyfile(src, dst)

    file_name = dst
    
    with open(file_name) as f:
        data_lines = f.read()
    
    # print (len(inlist),len(replacelist))
    if len(inlist)>0 and len(inlist) == len(replacelist):
        # print ('do replacement')
        for i in inlist:
            data_lines = data_lines.replace(i, replacelist[inlist.index(i)] )

    with open(file_name, mode="w") as f:
        f.write(data_lines)


def main():
    workdir = '../../LEO/genie-userconfigs/'

    src = workdir + sys.argv[1]
    dst = workdir + sys.argv[2]
    
    with open('../../cgenie_output/'+sys.argv[1]+'/sedgem/seddiag_misc_DATA_GLOBAL.res') as f:
        for line in f:
            if 'Total CaCO3 pres' not in line: continue
            a = line.split()
            done=False
            cnt =0
            while not done:
                try:
                    print (float(a[cnt]),a[cnt])
                    caco3 = a[cnt]
                    done = True
                except:
                    pass
                cnt += 1 
            
            if done: break
            
    
    inlist = [
        'sg_ctrl_sed_bioturb=.false.'
        # ,'# sediment  grid options'
        ,"# set a 'CLOSED' system"
        ,"bg_ctrl_force_sed_closedsystem=.true."
        ,'rg_par_weather_CaCO3='
        ,'# ac_par_atm_slab_ss_dtyr=1.0'
        ,'ac_par_atm_slab_restart=.false.'
        ]
    replacelist = [
        'sg_ctrl_sed_bioturb=.true.'
        # ,"# Sediment grid\nSEDGEMNLONSOPTS='$(DEFINE)SEDGEMNLONS=36'\nSEDGEMNLATSOPTS='$(DEFINE)SEDGEMNLATS=36'\n# sediment  grid options"
        ,"# set an 'OPEN' system"
        ,"bg_ctrl_force_sed_closedsystem=.false."
        ,'rg_par_weather_CaCO3='+caco3+'     #'
        ,'ac_par_atm_slab_ss_dtyr=0.0'
        ,'ac_par_atm_slab_restart=.true.'
        ]
    
    make_configs(src,dst,inlist,replacelist)
    
if __name__=='__main__':
    main()