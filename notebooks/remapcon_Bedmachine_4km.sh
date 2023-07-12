
#!/bin/bash

conda activate py38
python -u /bettik/burgardc/SCRIPTS/summer_paper/notebooks/remapcon_BedMachine.py 2>&1 | tee /bettik/burgardc/SCRIPTS/summer_paper/notebooks/remapcon_Bedmachine_4km.sh

