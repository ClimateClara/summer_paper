"""
Prepare T and S profiles for CMIP data
"""


import xarray as xr
import numpy as np
import sys
import glob
import distributed

mod = str(sys.argv[1])
scenario = str(sys.argv[2])

print(mod)
print(str(sys.argv[1]))

if mod == 'CNRM-CM6-1':
    ens_run = 'r1i1p1f2'
    
inputpath_data_orig='/bettik/jourdai1/OCEAN_DATA_CMIP6_STEREO/'+mod+'/'
inputpath_profiles='/bettik/burgardc/DATA/SUMMER_PAPER/interim/T_S_PROF/CMIP/'
inputpath_isf='/bettik/burgardc/DATA/SUMMER_PAPER/interim/ANTARCTICA_IS_MASKS/BedMachine_8km/'
inputpath_BedMachine='/bettik/burgardc/DATA/SUMMER_PAPER/interim/'

# make the domain a little smaller to make the computation even more efficient - file isf has already been made smaller at its creation
map_lim = [-3000000,3000000]

mask_domain_distkm = 50000


dist_to_front_file = xr.open_mfdataset(inputpath_profiles+'dist_to_ice_front_only_contshelf_8km.nc',chunks={'x': 400, 'y': 400, 'Nisf': 30})
T_ocean_files = xr.open_mfdataset(inputpath_data_orig+'thetao_Oyr_'+mod+'_'+scenario+'_'+ens_run+'_*.nc', chunks={'x': 400, 'y': 400, 'depth': 50, 'time': 5}, parallel=True)
S_ocean_files = xr.open_mfdataset(inputpath_data_orig+'so_Oyr_'+mod+'_'+scenario+'_'+ens_run+'_*.nc', chunks={'x': 400, 'y': 400, 'depth': 50, 'time': 5}, parallel=True)
file_BedMachine_orig = xr.open_mfdataset(inputpath_BedMachine+'BedMachine_v3_aggregated8km_allvars.nc').sel(x=dist_to_front_file.x,y=dist_to_front_file.y).chunk({'x': 400, 'y': 400})

dist_to_front = dist_to_front_file['dist_from_front']
ocean_conc = file_BedMachine_orig['ocean_conc']

mask_km = dist_to_front <= mask_domain_distkm

mask_sum = xr.open_mfdataset(inputpath_profiles + 'mask_sum.nc', chunks={'x': 400, 'y': 400, 'Nisf': 30})

for tt in T_ocean_files['thetao'].time:
    print(tt.values)
    ds_T_sum = (T_ocean_files['thetao'].sel(time=tt) * mask_km * ocean_conc).sum(['x','y'])
    ds_S_sum = (S_ocean_files['so'].sel(time=tt) * mask_km * ocean_conc).sum(['x','y'])

    ds_T_mean = (ds_T_sum/mask_sum['mask_sum'])
    ds_S_mean = (ds_S_sum/mask_sum['mask_sum'])
    
    ds_T_mean.to_dataset(name='thetao').to_netcdf(inputpath_profiles + mod + '/T_mean_prof_50km_contshelf_'+mod+'_'+scenario+'_'+str(tt.values)[0:4]+'.nc')
    ds_S_mean.to_dataset(name='so').to_netcdf(inputpath_profiles + mod + '/S_mean_prof_50km_contshelf_'+mod+'_'+scenario+'_'+str(tt.values)[0:4]+'.nc')

    
