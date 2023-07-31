"""
This script is to do the preparation of csv-input as a job
"""

import numpy as np
import xarray as xr
import summer_paper.data_formatting_NN as dfmt
import sys

mod = str(sys.argv[1]) # 'EPM026','EPM031', 'EPM034'
scenario = str(sys.argv[2])
to2300 = bool(sys.argv[3])

if scenario == 'historical':
    yystart = 1850
    yyend = 2014
else:
    if to2300:
        yystart = 2015
        yyend = 2300
    else:
        yystart = 2015
        yyend = 2100   
    
##### READ IN DATA
inputpath_data='/bettik/burgardc/DATA/SUMMER_PAPER/interim/'
inputpath_mask='/bettik/burgardc/DATA/SUMMER_PAPER/interim/ANTARCTICA_IS_MASKS/BedMachine_4km/'
inputpath_profiles='/bettik/burgardc/DATA/SUMMER_PAPER/interim/T_S_PROF/CMIP/'+mod+'/'
inputpath_boxes = '/bettik/burgardc/DATA/SUMMER_PAPER/interim/BOXES/BedMachine_4km/'
inputpath_plumes = '/bettik/burgardc/DATA/SUMMER_PAPER/interim/PLUMES/BedMachine_4km/'

outputpath_nn = '/bettik/burgardc/DATA/SUMMER_PAPER/interim/INPUT_DATA/CMIP/'+mod+'/'

outputpath = '/bettik/burgardc/DATA/SUMMER_PAPER/interim/'

map_lim = [-3000000,3000000]

# dIF, dGL
inputpath_isf='/bettik/burgardc/DATA/SUMMER_PAPER/interim/ANTARCTICA_IS_MASKS/BedMachine_4km/'
file_isf_orig = xr.open_dataset(inputpath_isf+'BedMachine_4km_isf_masks_and_info_and_distance_oneFRIS.nc')
nonnan_Nisf = file_isf_orig['Nisf'].where(np.isfinite(file_isf_orig['front_bot_depth_max']), drop=True).astype(int)
file_isf_nonnan = file_isf_orig.sel(Nisf=nonnan_Nisf)
rignot_isf = file_isf_nonnan.Nisf.where(np.isfinite(file_isf_nonnan['isf_area_rignot']), drop=True)
file_isf = file_isf_nonnan.sel(Nisf=rignot_isf)

# bathymetry, ice draft, concentration
BedMachine_orig = xr.open_dataset(inputpath_data+'BedMachine_v3_aggregated4km_allvars.nc')
BedMachine_orig_cut = dfmt.cut_domain_stereo(BedMachine_orig, map_lim, map_lim)
file_bed_goodGL = -1*BedMachine_orig_cut['bed']
file_draft = (BedMachine_orig_cut['thickness'] - BedMachine_orig_cut['surface']).where(file_isf['ISF_mask'] > 1)
file_isf_conc = BedMachine_orig_cut['isf_conc']

# ice and bed slopes
file_slope = xr.open_dataset(inputpath_mask+'BedMachine_4km_slope_info_bedrock_draft_latlon_oneFRIS.nc')

for tt in tqdm(range(yystart,yyend+1)): #yyend+1)): #continue at 2070
    print(tt)
    
    # T and S extrapolated to ice draft depth
    T_S_2D_isfdraft = xr.open_dataset(inputpath_profiles+'T_S_2D_fields_isf_draft_'+mod+'_'+scenario+'_'+str(tt)+'.nc').squeeze().drop('time')
    
    # T and S mean and std
    T_S_2D_meanstd = xr.open_dataset(inputpath_profiles + 'T_S_2D_meanstd_isf_draft_'+mod+'_'+scenario+'_'+str(tt)+'.nc')
    
    time_dpdt_in = file_isf[['dGL', 'dIF']].merge(file_draft.rename('corrected_isfdraft')
                                                 ).merge(file_bed_goodGL.rename('bathy_metry')
                                                        ).merge(file_slope).merge(file_isf_conc).merge(T_S_2D_isfdraft[['theta_in','salinity_in']]).merge(T_S_2D_meanstd)
                                                         
    time_dpdt_in['dIF'] = time_dpdt_in['dIF'].where(np.isfinite(time_dpdt_in['dIF']), np.nan)
    
    for kisf in file_isf.Nisf:
        ds_kisf = time_dpdt_in.where(file_isf['ISF_mask'] == kisf, drop=True)

        df_kisf = ds_kisf.drop('longitude').drop('latitude').to_dataframe()
        # remove rows where there are nans
        clean_df_kisf = df_kisf.dropna()
        clean_df_kisf = clean_df_kisf.where(clean_df_kisf['salinity_in']!=0).dropna()
        clean_df_kisf['time'] = clean_df_kisf['time'].dt.year
        clean_df_kisf.to_csv(outputpath_nn + 'dataframe_input_isf'+str(kisf.values).zfill(3)+'_'+mod+'_'+scenario+'_'+str(tt)+'.csv')