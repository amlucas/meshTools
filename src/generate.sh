#! /bin/bash

i=0
for P in `seq 2.0 0.5 5.0`; do
    id=`printf "%04d" $i`
    echo $id $P

    ./circ_helix_carrier.py --pitch $P --out helix_head_P_$P.ply
    let "i++" 
done
