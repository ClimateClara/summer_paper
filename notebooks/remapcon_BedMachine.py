import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Transformer
import pandas as pd
import sys,os
from cdo import Cdo
import time
from tqdm.notebook import tqdm

cdo = Cdo()
print('this is CDO version %s'%(cdo.version()))

inputpath_BedMachine='/bettik/burgardc/DATA/ERWIN_PAPER/'
inputpath_grid='/bettik/burgardc/DATA/SUMMER_PAPER/interim/'


time_start = time.time()
cdo.remapcon(inputpath_grid+'ISMIP6_AIS_4000m_grid.nc',
                 input = inputpath_BedMachine+'BedMachineAntarctica-v3.nc', 
                 output = inputpath_BedMachine+'BedMachineAntarctica-v3_remapcon4km.nc')
timelength = time.time() - time_start

