#!/bin/bash

# ===== read nx ny from SurfMap.in =====

inputfile="SurfMap.in"

# remove comment/blank line
line2=$(grep -v '^#' $inputfile | grep -v '^$' | sed -n '2p')
line5=$(grep -v '^#' $inputfile | grep -v '^$' | sed -n '5p')
line7=$(grep -v '^#' $inputfile | grep -v '^$' | sed -n '7p')
# line 2 : nx ny nz
read nx ny nz << EOF
$line2
EOF
n=$((nx*ny-1))

# ===== rewrite surfdisp.in =====

# line 5 : ifunc mode kmax
read ifunc mode kmax << EOF
$line5
EOF
# line 7 : periods
periods="$line7"

: > OUTPUT/disp_all_phase.txt
: > OUTPUT/disp_all_group.txt
# ===== loop over igr(0 for phase; 1 for group) =====
for igr in 0 1
do
    # store current igr
    echo $igr > igr.tmp
    # rewrite surfdisp.in
    cat > surfdisp.in << EOF
ref_v.mdl
disp.txt
$ifunc $mode $igr $kmax
$periods
EOF
    # main loop
    for i in $(seq 0 $n)
    do
        python ./src/process.py $i
        ./bin/surfdisp < surfdisp.in
        python ./src/process2.py
        echo "igr=$igr point=$i"
    done
done

# ===== convert to matlab format =====

python ./src/convert_to_mat.py

rm *.tmp
rm disp.txt

echo "Finished SurfMap"
