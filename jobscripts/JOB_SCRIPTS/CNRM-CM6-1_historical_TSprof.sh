
#!/bin/bash

conda activate py38
python -u /bettik/burgardc/SCRIPTS/summer_paper/notebooks/Ocean_stuff/format_CMIP//prepare_TS_prof_asjob.py CNRM-CM6-1 historical 2>&1 | tee /bettik/burgardc/SCRIPTS/summer_paper/jobscripts/JOB_OUTFILES//CNRM-CM6-1_historical_TSprof.log
