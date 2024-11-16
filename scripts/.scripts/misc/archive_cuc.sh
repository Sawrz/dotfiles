#!/bin/bash
simulation_path=/mnt/vault/phd
archive_path=$simulation_path/share/CUC/

for i in $(seq -f "%03g" 1 50)
do
   run_path=$simulation_path/CUC/03_productions/run_$i
   tar --use-compress-program=lbzip2 -cvf $archive_path/cuc_run_$i.tar.bz2 $simulation_path/CUC/03_production/run_$i/

done
