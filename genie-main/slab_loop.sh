#!/bin/bash

homedir2="/storage/coda1/p-creinhard3/0/ykanzaki3"

pydir="${homedir2}/scripts/slab"

file="${pydir}/2nd_pass_compile.save_allemis"

cnt=1

totn=${2}
remainderin=${1}

declare -a f1  
while read -r f1;do
	num=${f1%.*}

	remainder=$((cnt%totn))
	remainder=$((remainder+1))

	if [ "$remainder" -ne "${remainderin}" ] ; then
		cnt=$((cnt+1))
		continue
	fi
	
	echo $remainderin $totn $num
	
	./slab_rcp_cdr.sh $num
	
    cnt=$((cnt+1))
    
    # break

done <$file