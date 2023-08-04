"""
Created on Tue Jul 18 11:29 2023
This script is to run tuning of the params, options read in from BASH => including the ones from Christoph for summer paper
@author: Clara Burgard
"""

import sys
import pandas as pd
import xarray as xr
import numpy as np
import summer_paper.tuning_functions as tf

#######

run_list = ['OPM006','OPM016','OPM018','OPM021','OPM031','ctrl94','isf94','isfru94']  #

inputpath_chunk_info = '/bettik/burgardc/DATA/SUMMER_PAPER/interim/'
info_file = pd.read_csv(inputpath_chunk_info+'info_chunks.txt',header=None, index_col=0)

##### OPTIONS FROM TERMINAL

isf_opt= 'LARGE'

tuning_approach=isf_opt

geometry_info_2D, geometry_info_1D, isf_stack_mask, Nisf_all, file_TS_all, target_melt_all, box_1D_all, box_2D_all, idx_ds = tf.load_data_nemo_tuning_summer_paper(run_list)
geometry_info_2D = geometry_info_2D.assign_coords({'option': ['cavity','lazero','local']})

#######
    
tblock_dim = np.arange(1,17).tolist()+np.arange(21,50).tolist()
tblock_list = tblock_dim

random_time_list = []
rrun_list = []
for tt in tblock_list:
    run, tstart, tend = info_file.loc[tt]
    random_time_list.append(idx_ds['time'].where((idx_ds['run']==run) & (idx_ds['years']>=tstart) & (idx_ds['years']<=tend)).dropna(dim='time').values.astype(int))
    rrun_list.append(run)
time_idx = np.concatenate(random_time_list,axis=0)

final_run_list = []
for rr in run_list:
    if rr in rrun_list:
        final_run_list.append(rr)

if isf_opt == 'ALL':
    random_isf_sample = Nisf_all
elif isf_opt == 'SMALL':
    random_isf_sample = Nisf_all.drop_sel(Nisf=[10,11])
elif isf_opt == 'LARGE':
    random_isf_sample = Nisf_all.sel(Nisf=[10,11])
    
#####

dom=50    

# always needs to be filled
option_param = 'plume' #box

# if linear or qaudratic
if option_param in ['linear','quadratic']:
    simple_form = str(sys.argv[5]) #'quadratic_local', 'quadratic_local_cavslope', 'quadratic_local_locslope', quadratic_mixed_mean', 'quadratic_mixed_cavslope', 'quadratic_mixed_locslope' 
    plume_form = None
    nD_config = None
    pism_version = None

# if plume
elif option_param == 'plume':
    plume_form = 'lazero19'
    simple_form = None
    nD_config = None
    pism_version = None
    picop_opt = None

# if box 
elif option_param == 'box':
    nD_config = 4
    pism_version = 'yes'
    picop_opt = 'no'
    simple_form = None
    plume_form = None

tf.tuning_param_BT(option_param, tuning_approach, dom, 
         file_TS_all, random_isf_sample, time_idx, target_melt_all,
         geometry_info_2D, geometry_info_1D, isf_stack_mask,
         box_2D_all, box_1D_all, 
         plume_form=plume_form, nD_config=nD_config, pism_version=pism_version, picop_opt=picop_opt,run_list=final_run_list)