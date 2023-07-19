
!#/bin/bash


cat << EOF > /bettik/burgardc/SCRIPTS/summer_paper/notebooks/remapcon_Bedmachine_4km.sh

#!/bin/bash

conda activate py38
python -u /bettik/burgardc/SCRIPTS/summer_paper/notebooks/remapcon_BedMachine.py 2>&1 | tee /bettik/burgardc/SCRIPTS/summer_paper/notebooks/remapcon_Bedmachine_4km.sh

EOF
chmod +x /bettik/burgardc/SCRIPTS/summer_paper/notebooks/remapcon_Bedmachine_4km.sh


oarsub -S -n remapcon_Bedmachine_4km --stdout remapcon_Bedmachine_4km.o%jobid%  --stderr remapcon_Bedmachine_4km.e%jobid% -l nodes=1/core=28,walltime=06:00:00 --project ice_speed -p "network_address='luke62'" /bettik/burgardc/SCRIPTS/summer_paper/notebooks/remapcon_Bedmachine_4km.sh
