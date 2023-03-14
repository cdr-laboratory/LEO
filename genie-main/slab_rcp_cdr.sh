#!/bin/bash

homedir1="/storage/scratch1/0/ykanzaki3"
homedir2="/storage/coda1/p-creinhard3/0/ykanzaki3"

archdir1="${homedir1}/cgenie_archive/"
archdir2="${homedir2}/cgenie_archive/"

outputdir1="${homedir1}/cgenie_output/"
outputdir2="${homedir2}/cgenie_output/"

pydir="${homedir2}/scripts/slab"

# ==================================
# spinup-1 
baseconfig="muffin.CBSR.worjh2.ESW.S36x36"
outdir="/"

expnum=${1}
echo $expnum
expnumstr=$( printf '%05d' $expnum )
echo $expnumstr

spin1d="s${expnumstr}.SPIN1"
spin1s="s${expnumstr}.SPIN1p5"
spin2="s${expnumstr}.SPIN2"

tauspin=20000
# tauspin=20

if [ -f "${archdir1}/${spin1d}.tar.gz" ]; then
	echo "if spin1 already archived, assume spin1 is already done"
	cp "${archdir1}${spin1d}.tar.gz" "${archdir2}${spin1d}.tar.gz"
	tar -xzf "${archdir2}${spin1d}.tar.gz" -C ${outputdir2}
	rm "${archdir2}${spin1d}.tar.gz"
else
	# else spin1 from scratch
	# creating user-configs
	cp "${homedir2}/cgenie.muffin/genie-userconfigs/slab_spin1p5_done/${spin1s}"  "${homedir2}/cgenie.muffin/genie-userconfigs/${spin1d}"

	# modifying user-configs
	python3 ../../scripts/slab/mod_configs.py $spin1d $spin1d 113  "bg_par_infile_slice_name='save_timeslice_NONE.dat'"

	runduration=$tauspin
	run=$spin1d
	restart=""

	./runmuffin.sh  $baseconfig $outdir $run $runduration $restart
fi

# ==================================
# spinup-2

# userconfigs
python3 ../../scripts/slab/slab_configs_spin1to2.py $spin1d $spin2

runduration=$tauspin
run=$spin2
restart=$spin1d

if [ -f "${archdir1}/${run}.tar.gz" ]; then
	echo "if ${run} already archived, assume ${run} is already done"
	cp "${archdir1}${run}.tar.gz" "${archdir2}${run}.tar.gz"
	tar -xzf "${archdir2}${run}.tar.gz" -C ${outputdir2}
	rm "${archdir2}${run}.tar.gz"
else

    ./runmuffin.sh  $baseconfig $outdir $run $runduration $restart
fi

# now can remove spin1
rm -r $outputdir2$spin1d
mv "${archdir2}${spin1d}.tar.gz" $archdir1

# ==================================
# RCP conc. forcings

declare -a rcps=("2p6" "4p5" "6p0" "8p5") 

nrcps=${#rcps[@]}

for (( i=1; i<${nrcps}+1; i++ )); do
    
    rcp=${rcps[$i-1]}
    
    # making config file
    python3 ../../scripts/slab/slab_config_spin2toRCPconcs.py $expnum $rcp
    
    concforce="s${expnumstr}.RCP${rcp}.conc.o"
    
    runduration=735
    # runduration=20
    run=$concforce
    restart=$spin2
    
    if [ -f "${archdir1}/${run}.tar.gz" ]; then
        echo "if ${run} already archived, assume ${run} is already done"
        cp "${archdir1}${run}.tar.gz" "${archdir2}${run}.tar.gz"
        tar -xzf "${archdir2}${run}.tar.gz" -C ${outputdir2}
        rm "${archdir2}${run}.tar.gz"
    else
        ./runmuffin.sh  $baseconfig $outdir $run $runduration $restart
    fi
    
# done

# ==================================
# RCP emis. forcings

    # makeing forcings from conc results
    python3 ../../scripts/slab/slab_force_RCPconc2flx.py $expnum $rcp
    
    # user config
    python3 ../../scripts/slab/slab_config_spin2toRCPemis.py $expnum $rcp

# for (( i=1; i<${nrcps}+1; i++ )); do
    
    # rcp=${rcps[$i-1]}
    
    emisforce="s${expnumstr}.RCP${rcp}.emis.o"
    
    runduration=735
    # runduration=20
    run=$emisforce
    restart=$spin2
    
    if [ -f "${archdir1}/${run}.tar.gz" ]; then
        echo "if ${run} already archived, assume ${run} is already done"
        cp "${archdir1}${run}.tar.gz" "${archdir2}${run}.tar.gz"
        tar -xzf "${archdir2}${run}.tar.gz" -C ${outputdir2}
        rm "${archdir2}${run}.tar.gz"
    else
        ./runmuffin.sh  $baseconfig $outdir $run $runduration $restart
    fi
    
    python3 ../../scripts/slab/slab_x_data.py  $run

    # now remove emis 
    rm -r $outputdir2$run
    mv "${archdir2}${run}.tar.gz" $archdir1
    
    # also conc
    concforce="s${expnumstr}.RCP${rcp}.conc.o"
    rm -r $outputdir2$concforce
    mv "${archdir2}${concforce}.tar.gz" $archdir1
    
# done


# ==================================
# RCP histrical runs 
    python3 ../../scripts/slab/slab_config_emis2his.py $expnum $rcp

# for (( i=1; i<${nrcps}+1; i++ )); do
    
    # rcp=${rcps[$i-1]}
    
    hist="s${expnumstr}.RCP${rcp}.hist.o"
    
    runduration=265
    # runduration=20
    run=$hist
    restart=$spin2
    
    if [ -f "${archdir1}/${run}.tar.gz" ]; then
        echo "if ${run} already archived, assume ${run} is already done"
        cp "${archdir1}${run}.tar.gz" "${archdir2}${run}.tar.gz"
        tar -xzf "${archdir2}${run}.tar.gz" -C ${outputdir2}
        rm "${archdir2}${run}.tar.gz"
    else
        ./runmuffin.sh  $baseconfig $outdir $run $runduration $restart
    fi
    
    python3 ../../scripts/slab/slab_x_data.py  $run

done

# now can remove spin2
rm -r $outputdir2$spin2
mv "${archdir2}${spin2}.tar.gz" $archdir1

# ==================================
# RCP + CDR 

declare -a CDRs=("DAC" "ESW" "ECW") 
declare -a deps=("0p5" "1p0" "5p0" "10p0" "20p0" "40p0") 

nCDRs=${#CDRs[@]}
ndeps=${#deps[@]}

# get DAC forcing 
python3 ../../scripts/slab/slab_force_RCPDAC.py $expnum

# configs for CDR and control
python3 ../../scripts/slab/slab_config_RCPCDR.py $expnum

for (( i=1; i<${nrcps}+1; i++ )); do
    
    rcp=${rcps[$i-1]}
    
    ctrl="s${expnumstr}.RCP${rcp}.emis.o.CTRL0p0GtCO2"
    hist="s${expnumstr}.RCP${rcp}.hist.o"
    
    runduration=470
    # runduration=20
    run=$ctrl
    restart=$hist
    
    if [ -f "${archdir1}/${run}.tar.gz" ]; then
        echo "if ${run} already archived, assume ${run} is already done"
        cp "${archdir1}${run}.tar.gz" "${archdir2}${run}.tar.gz"
        tar -xzf "${archdir2}${run}.tar.gz" -C ${outputdir2}
        rm "${archdir2}${run}.tar.gz"
    else
        ./runmuffin.sh  $baseconfig $outdir $run $runduration $restart
    fi
    
    python3 ../../scripts/slab/slab_x_data.py  $run
    # now remove ctrl 
    rm -r $outputdir2$run
    mv "${archdir2}${run}.tar.gz" $archdir1
    

    for (( j=1; j<${nCDRs}+1; j++ )); do
        
        CDR=${CDRs[$j-1]}

        for (( k=1; k<${ndeps}+1; k++ )); do
            
            dep=${deps[$k-1]}
            
            capexp="s${expnumstr}.RCP${rcp}.emis.o.${CDR}${dep}GtCO2"
            
            runduration=470
            # runduration=20
            run=$capexp
            restart=$hist
    
            if [ -f "${archdir1}/${run}.tar.gz" ]; then
                echo "if ${run} already archived, assume ${run} is already done"
                cp "${archdir1}${run}.tar.gz" "${archdir2}${run}.tar.gz"
                tar -xzf "${archdir2}${run}.tar.gz" -C ${outputdir2}
                rm "${archdir2}${run}.tar.gz"
            else
                ./runmuffin.sh  $baseconfig $outdir $run $runduration $restart
            fi
            
            python3 ../../scripts/slab/slab_x_data.py  $run
            # now remove capexp 
            rm -r $outputdir2$run
            mv "${archdir2}${run}.tar.gz" $archdir1
        
        done
    
    done
    
    # now remove hist 
    rm -r $outputdir2$hist
    mv "${archdir2}${hist}.tar.gz" $archdir1

done
