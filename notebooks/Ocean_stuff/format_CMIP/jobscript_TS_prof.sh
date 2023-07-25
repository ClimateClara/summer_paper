#!/bin/bash

## RUN PREPARATION OF T AND S PROFILES

mod=CNRM-CM6-1
scenario=historical

path_jobscripts=/bettik/burgardc/SCRIPTS/summer_paper/jobscripts/JOB_SCRIPTS/
path_outfiles=/bettik/burgardc/SCRIPTS/summer_paper/jobscripts/JOB_OUTFILES/

path_python=/bettik/burgardc/SCRIPTS/summer_paper/notebooks/Ocean_stuff/format_CMIP/
path_jobid=/bettik/burgardc/SCRIPTS/summer_paper/jobscripts/JOB_STD_OUTPUT

cat <<EOF > $path_jobscripts/${mod}_${scenario}_TSprof.sh 

#!/bin/bash

conda activate py38
python -u $path_python/prepare_TS_prof_asjob.py ${mod} ${scenario} 2>&1 | tee $path_outfiles/${mod}_${scenario}_TSprof.log
EOF

chmod +x $path_jobscripts/${mod}_${scenario}_TSprof.sh

oarsub -S -n ${mod}_${scenario}_TSprof --stdout $path_jobid/${mod}_${scenario}_TSprof.o%jobid%  --stderr $path_jobid/${mod}_${scenario}_TSprof.e%jobid% -l nodes=1/core=6,walltime=05:00:00 --project mais -p "network_address='luke62'" $path_jobscripts/${mod}_${scenario}_TSprof.sh

# to remove if no CV!!!

