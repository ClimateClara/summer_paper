
#!/bin/bash

conda activate neuralnet
python -u /bettik/burgardc/SCRIPTS/summer_paper/notebooks/Ocean_stuff/format_CMIP//prep_csv_CMIP_asjob.py CNRM-CM6-1 historical False 2>&1 | tee /bettik/burgardc/SCRIPTS/summer_paper/jobscripts/JOB_OUTFILES//CNRM-CM6-1_historical_prepcsvinput.log
