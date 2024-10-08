"""
Created on Wed Jan 25 17:41 2022

This script is to train a NN on the whole dataset

Author: Clara Burgard
"""

import numpy as np
import xarray as xr
import pandas as pd
from tqdm.notebook import trange, tqdm
import glob
import datetime
import time
import sys

import tensorflow as tf
from tensorflow import keras
import basal_melt_neural_networks.model_functions as modf
import basal_melt_neural_networks.prep_input_data as indat

######### READ IN OPTIONS

mod_size = str(sys.argv[1]) #'mini', 'small', 'medium', 'large', 'extra_large'
TS_opt = str(sys.argv[2]) # extrap, whole, thermocline
norm_method = str(sys.argv[3]) # std, interquart, minmax
exp_name = str(sys.argv[4])
seed_nb = int(sys.argv[5])

np.random.seed(seed_nb)
tf.random.set_seed(seed_nb)


if exp_name == 'newbasic2':
    var_list = ['dGL','dIF','corrected_isfdraft','bathy_metry','slope_bed_lon','slope_bed_lat','slope_ice_lon','slope_ice_lat','theta_in','salinity_in','T_mean', 'S_mean', 'T_std', 'S_std','melt_m_ice_per_y']

    
# INPUT
# onlyTSdraft: 'corrected_isfdraft','theta_in','salinity_in'
# TSdraftbotandiceddandwcd: 'corrected_isfdraft','theta_in','salinity_in','water_col_depth','theta_bot','salinity_bot'
# TSdraftbotandiceddandwcdreldGL: 'corrected_isfdraft','theta_in','salinity_in','water_col_depth','theta_bot','salinity_bot','rel_dGL'
# onlyTSdraftandslope : 'corrected_isfdraft','theta_in','salinity_in','slope_ice_lon','slope_ice_lat'
# onlyTSdraft2 : same as onlyTSdraft, just to check that everything is working well
# TSTfdGLdIFwcd : 'corrected_isfdraft','theta_in','salinity_in','dGL','dIF','slope_ice_lon','slope_ice_lat','water_col_depth'
# TSdraftslopereldGL : 'corrected_isfdraft','theta_in','salinity_in','slope_ice_lon','slope_ice_lat','rel_dGL'
# allbutconstants : 'dGL','dIF','corrected_isfdraft','bathy_metry','slope_bed_lon','slope_bed_lat','slope_ice_lon','slope_ice_lat','isfdraft_conc','theta_in','salinity_in','u_tide'

######### READ IN DATA

inputpath_data = '/bettik/burgardc/DATA/NN_PARAM/interim/INPUT_DATA/'
outputpath_nn_models = '/bettik/burgardc/DATA/SUMMER_PAPER/interim/NN_MODELS/'

tblock_dim = np.arange(1,14).tolist()+np.arange(21,50).tolist()
isf_dim = [10,11,12,13,18,22,23,24,25,30,31,33,38,39,40,42,43,44,45,47,48,51,52,53,54,55,58,61,65,66,69,70,71,73,75]


path_model = outputpath_nn_models

if TS_opt == 'extrap':
    inputpath_CVinput = inputpath_data+'EXTRAPOLATED_ISFDRAFT_CHUNKS/'
elif TS_opt == 'whole':
    inputpath_CVinput = inputpath_data+'WHOLE_PROF_CHUNKS/'
elif TS_opt == 'thermocline':
    inputpath_CVinput = inputpath_data+'THERMOCLINE_CHUNKS/'


if TS_opt == 'extrap':
    
    data_train_orig_norm = xr.open_dataset(inputpath_CVinput + 'train_data_wholedataset_origexcept26_christoph.nc')
    data_val_orig_norm = xr.open_dataset(inputpath_CVinput + 'train_data_wholedataset_origexcept26_christoph.nc') 

    data_train_norm = data_train_orig_norm[var_list]
    data_val_norm = data_val_orig_norm[var_list]

    
    ## prepare input and target
    y_train_norm = data_train_norm['melt_m_ice_per_y'].load() #.sel(norm_method=norm_method)
    x_train_norm = data_train_norm.drop_vars(['melt_m_ice_per_y']).to_array().load() #.sel(norm_method=norm_method)
    #print('here4')
    #x_train_norm = data_train_norm[['corrected_isfdraft','water_col_depth','theta_in','salinity_in','theta_bot','salinity_bot']].sel(norm_method=norm_method).to_array().load()
    
    y_val_norm = data_val_norm['melt_m_ice_per_y'].load() #.sel(norm_method=norm_method)
    x_val_norm = data_val_norm.drop_vars(['melt_m_ice_per_y']).to_array().load() #.sel(norm_method=norm_method)
    #print('here6')
    #x_val_norm = data_val_norm[['corrected_isfdraft','water_col_depth','theta_in','salinity_in','theta_bot','salinity_bot']].sel(norm_method=norm_method).to_array().load()


else:
    print('Sorry, I dont know this option for TS input yet, you need to implement it...')


######### TRAIN THE MODEL

input_size = x_train_norm.values.shape[0]
activ_fct = 'relu' #LeakyReLU
epoch_nb = 100
batch_siz = 512

model = modf.get_model(mod_size, input_size, activ_fct,1)


reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5,
                              patience=5, min_lr=0.0000001, min_delta=0.0005) #, min_delta=0.1
            
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    #min_delta=0.000001,
    patience=10,
    verbose=0,
    mode="auto",
    baseline=None,
    restore_best_weights=True,
)

time_start = time.time()
time_start0 = datetime.datetime.now()
print(time_start0)

history = model.fit(x_train_norm.T.values,
                    y_train_norm.values,
                    epochs          = epoch_nb,
                    batch_size      = batch_siz,
                    verbose         = 2,
                    validation_data = (x_val_norm.T.values, y_val_norm.values),
                   callbacks=[reduce_lr, early_stop])
time_end = time.time()
timelength = time_end - time_start

time_end0 = datetime.datetime.now()
print(time_end0)

#with open(new_path_doc+'info_'+timetag+'.log','a') as file:
#    file.write('\n Reduce_lr: True')
#    file.write('\n Early_stop: True')
#    file.write('\n Training time (in s): '+str(timelength))
model.save(path_model + 'model_nn_'+mod_size+'_'+exp_name+'_wholedataset_'+str(seed_nb).zfill(2)+'_TS'+TS_opt+'_norm'+norm_method+'.h5')

# convert the history.history dict to a pandas DataFrame:     
hist_df = pd.DataFrame(history.history) 

hist_csv_file = path_model + 'history_'+mod_size+'_'+exp_name+'_wholedataset_'+str(seed_nb).zfill(2)+'_TS'+TS_opt+'_norm'+norm_method+'.csv'
with open(hist_csv_file, mode='w') as f:
    hist_df.to_csv(f)