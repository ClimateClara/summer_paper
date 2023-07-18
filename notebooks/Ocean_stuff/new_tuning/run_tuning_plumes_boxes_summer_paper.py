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

run_list = ['OPM006','OPM016','OPM018','OPM021','OPM031','ctrl94','isf94','isfru94'] 

#inputpath_chunk_info = '/bettik/burgardc/DATA/BASAL_MELT_PARAM/interim/T_S_PROF/'
#info_file = pd.read_csv(inputpath_chunk_info+'info_chunks.txt',header=None, index_col=0)

##### OPTIONS FROM TERMINAL


if sys.argv[2] == 'ALL':
    
    tuning_approach='all_data'
    
    geometry_info_2D, geometry_info_1D, isf_stack_mask, Nisf_all, file_TS_all, target_melt_all, box_1D_all, box_2D_all, idx_ds = tf.load_data_nemo_tuning_summer_paper(run_list)

    tblock_dim = np.arange(1,14).tolist()  
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


    random_isf_sample = Nisf_all

elif sys.argv[2] == 'AMUNDSEN':
    
    tuning_approach='all_data'
    
    #inputpath_mask = '/bettik/burgardc/SCRIPTS/basal_melt_param/data/interim/ANTARCTICA_IS_MASKS/nemo_5km_OPM006/'
    #file_isf_orig = xr.open_dataset(inputpath_mask+'nemo_5km_isf_masks_and_info_and_distance_new_oneFRIS.nc')
    #nonnan_Nisf = file_isf_orig['Nisf'].where(np.isfinite(file_isf_orig['front_bot_depth_max']), drop=True).astype(int)
    #file_isf_nonnan = file_isf_orig.sel(Nisf=nonnan_Nisf)
    #large_isf = file_isf_nonnan['Nisf'].where(file_isf_nonnan['isf_area_here'] >= 2500, drop=True)
    
    #isf_list = large_isf
        
    #tblock_out, tblock_run, tblock_start, tblock_end = [False, False, False, False]
    
    #geometry_info_2D, geometry_info_1D, isf_stack_mask, Nisf_all, file_TS_all, target_melt_all, box_1D_all, box_2D_all = tf.load_data_nemo_tuning_CV(run_list, isf_list, tblock_run, tblock_start, tblock_end)
    
    geometry_info_2D, geometry_info_1D, isf_stack_mask, Nisf_all, file_TS_all, target_melt_all, box_1D_all, box_2D_all, idx_ds = tf.load_data_nemo_tuning_BT(run_list)

    tblock_dim = np.arange(1,14).tolist()  
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


    random_isf_sample = Nisf_all.sel(Nisf=[23,38,52,53])


    
else:
    print(str(sys.argv[2]) + ' is an unusual command for the tuning approach, are you sure?')
    tuning_approach=str(sys.argv[2])
    

# always needs to be filled
option_param = str(sys.argv[3]) #linear, quadratic, plume, box
dom = int(sys.argv[4])

# if linear or qaudratic
if option_param in ['linear','quadratic']:
    simple_form = str(sys.argv[5]) #'quadratic_local', 'quadratic_local_cavslope', 'quadratic_local_locslope', quadratic_mixed_mean', 'quadratic_mixed_cavslope', 'quadratic_mixed_locslope' 
    plume_form = None
    nD_config = None
    pism_version = None

# if plume
elif option_param == 'plume':
    plume_form = str(sys.argv[5])
    simple_form = None
    nD_config = None
    pism_version = None
    picop_opt = None

# if box 
elif option_param == 'box':
    boxparam = sys.argv[5].split('_')
    nD_config = int(boxparam[0])
    pism_version = str(boxparam[1])
    picop_opt = str(boxparam[2])
    simple_form = None
    plume_form = None

if tide_opt == 'True':
    
    #### DOUBLE CHECK IF EVERYTHING WORKS!!
    tf.tuning_param_tides(option_param, tuning_approach, dom, 
                     file_TS_all, Nisf_all, u_tide_all, target_melt_all,
                     geometry_info_2D, geometry_info_1D, isf_stack_mask,
                     box_2D_all, box_1D_all, 
                     simple_form=simple_form, plume_form=plume_form, nD_config=nD_config, pism_version=pism_version)
else:
    
    #if tuning_approach == 'all_data':
    if tuning_approach == 'blabla':
    
        tf.tuning_param(option_param, tuning_approach, dom, 
                         file_TS_all, Nisf_all, target_melt_all,
                         geometry_info_2D, geometry_info_1D, isf_stack_mask,
                         box_2D_all, box_1D_all, 
                         plume_form=plume_form, nD_config=nD_config, pism_version=pism_version, picop_opt=picop_opt)
        
    else:
        #print('entered bootstrap')
        tf.tuning_param_BT(option_param, tuning_approach, dom, 
                 file_TS_all, random_isf_sample, time_idx, target_melt_all,
                 geometry_info_2D, geometry_info_1D, isf_stack_mask,
                 box_2D_all, box_1D_all, 
                 plume_form=plume_form, nD_config=nD_config, pism_version=pism_version, picop_opt=picop_opt,run_list=final_run_list)