#!/bin/bash

## RUN PREPARATION OF T AND S PROFILES

mod=CNRM-CM6-1
scenario=historical
to2300=False

path_jobscripts=/bettik/burgardc/SCRIPTS/summer_paper/jobscripts/JOB_SCRIPTS/
path_outfiles=/bettik/burgardc/SCRIPTS/summer_paper/jobscripts/JOB_OUTFILES/

path_python=/bettik/burgardc/SCRIPTS/summer_paper/notebooks/Ocean_stuff/format_CMIP/
path_jobid=/bettik/burgardc/SCRIPTS/summer_paper/jobscripts/JOB_STD_OUTPUT

cat <<EOF > $path_jobscripts/${mod}_${scenario}_prepcsvinput.sh 

#!/bin/bash

conda activate neuralnet
python -u $path_python/prep_csv_CMIP_asjob.py ${mod} ${scenario} ${to2300} 2>&1 | tee $path_outfiles/${mod}_${scenario}_prepcsvinput.log
EOF

chmod +x $path_jobscripts/${mod}_${scenario}_prepcsvinput.sh

oarsub -S -n ${mod}_${scenario}_prepcsvinput --stdout $path_jobid/${mod}_${scenario}_prepcsvinput.o%jobid%  --stderr $path_jobid/${mod}_${scenario}_prepcsvinput.e%jobid% -l nodes=1/core=3,walltime=08:00:00 --project mais -p "network_address='luke62'" $path_jobscripts/${mod}_${scenario}_prepcsvinput.sh

# to remove if no CV!!!

