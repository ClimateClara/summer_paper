
#!/bin/bash

conda activate neuralnet
python -u /bettik/burgardc/SCRIPTS/summer_paper/notebooks/Ocean_stuff/new_tuning//run_training_whole_dataset_summer_paper.py large extrap std newbasic2 1 2>&1 | tee /bettik/burgardc/SCRIPTS/summer_paper/jobscripts/JOB_OUTFILES//large_extrap_std_wholedataset_newbasic2_1.log
