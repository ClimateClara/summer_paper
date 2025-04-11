#!/bin/bash

#########
#This script is to format the raw NEMO data for further use 
#It extracts the interesting variables and adds the right grid information needed to regrid it in the next step
########

homepath=/bettik/burgardc

#### name of NEMO run
nemo_run=ctrl94fut
#nemo_run=isf94
#nemo_run=isfru94

################# DECLARE THE PATHS ##############################
path1=/bettik/kittelc/clara/FOLDER_LINKS_SUMMER_PAPER/"$nemo_run"/raw/
path2=/bettik/kittelc/clara/FOLDER_LINKS_SUMMER_PAPER/"$nemo_run"/interim/
path3=/bettik/kittelc/clara/FOLDER_LINKS_SUMMER_PAPER/"$nemo_run"/interim/ #NEMO_"$nemo_run"_ANT_STEREO
path5=$homepath/DATA/SUMMER_PAPER/raw
path6=/bettik/kittelc/clara/ #isfru
path7=/bettik/burgardc/DATA/SUMMER_PAPER/raw/CHRISTOPH_DATA/
###################################################################

#cdo setgrid,$path1/var_grid_wo_nans.txt $path1/fwfisf-eANT025.L121-"$nemo_run"-1y_1982-2013.nc $path2/fwfisf-eANT025.L121-"$nemo_run"-1y_setgrid.nc
#cdo setgrid,$path1/var_grid_wo_nans.txt $path1/thetao-eANT025.L121-"$nemo_run"-1y_1982-2013.nc $path2/thetao-eANT025.L121-"$nemo_run"-1y_setgrid.nc
#cdo setgrid,$path1/var_grid_wo_nans.txt $path1/so-eANT025.L121-"$nemo_run"-1y_1982-2013.nc $path2/so-eANT025.L121-"$nemo_run"-1y_setgrid.nc

for yy in {2014..2100}
do
echo $yy
cdo setgrid,$path7/var_grid_wo_nans.txt $path1/fwfisf-eANT025.L121-"$nemo_run"-1y_"$yy".nc $path2/fwfisf-eANT025.L121-"$nemo_run"_"$yy".nc
cdo setgrid,$path7/var_grid_wo_nans.txt $path1/thetao-eANT025.L121-"$nemo_run"-1y_"$yy".nc $path2/thetao-eANT025.L121-"$nemo_run"_"$yy".nc
cdo setgrid,$path7/var_grid_wo_nans.txt $path1/so-eANT025.L121-"$nemo_run"-1y_"$yy".nc $path2/so-eANT025.L121-"$nemo_run"_"$yy".nc
done

#cdo splityear $path1/fwfisf-eANT025.L121-"$nemo_run"-1y_2014-2100.nc $path2/fwfisf-eANT025.L121-"$nemo_run"_
#cdo splityear $path1/thetao-eANT025.L121-"$nemo_run"-1y_2014-2100.nc $path2/thetao-eANT025.L121-"$nemo_run"_
#cdo splityear $path1/so-eANT025.L121-"$nemo_run"-1y_2014-2100.nc $path2/so-eANT025.L121-"$nemo_run"_

#for yy in {1982..2013}
for yy in {2014..2100}
do 
echo $yy
\rm $path2/variables_of_interest-"$nemo_run"_"$yy".nc
cdo merge $path2/fwfisf-eANT025.L121-"$nemo_run"_"$yy".nc $path2/thetao-eANT025.L121-"$nemo_run"_"$yy".nc $path2/so-eANT025.L121-"$nemo_run"_"$yy".nc $path2/variables_of_interest-"$nemo_run"_"$yy".nc
done


cdo ifthenc,1 -vertsum -selvar,tmask $path1/mesh_mask.nc $path2/tmask_sum_withmiss.nc 
cdo setmisstoc,0 $path2/tmask_sum_withmiss.nc $path2/tmask_sum.nc

cdo ifthenc,1 -selvar,tmask $path1/mesh_mask.nc $path2/tmask_3d_withmiss.nc 
cdo setmisstoc,0 $path2/tmask_3d_withmiss.nc $path2/tmask_3d.nc 

for vvar in {nav_lon,nav_lat,isf_draft,bathy_metry,e3w_0}
do
    cdo selvar,$vvar $path1/domain_cfg_eANT025.L121.nc  $path2/mask_$vvar.nc
done

cdo merge $path2/mask_nav_lon.nc $path2/mask_nav_lat.nc $path2/tmask_sum.nc $path2/tmask_3d.nc $path2/mask_isf_draft.nc $path2/mask_bathy_metry.nc $path2/mask_e3w_0.nc  $path2/mask_variables_of_interest.nc

#####
# ipython
# import xarray as xr
# cd /bettik/burgardc/DATA/SUMMER_PAPER/interim/CHRISTOPH_ #isf94
# mask_file = xr.open_dataset('mask_variables_of_interest.nc')
# mfile_wo_time = mask_file.squeeze().drop('time_counter')  
# mfile_wo_time.to_netcdf('mask_variables_of_interest_wotime.nc')

cdo setgrid,$path1/var_grid_wo_nans.txt $path2/mask_variables_of_interest_wotime.nc $path2/mask_variables_of_interest_setgrid.nc 
#$path1/eANT025.L121_grid_T_cdo.nc


cdo sellonlatbox,0,360,-90,-50 $path2/mask_variables_of_interest_setgrid.nc $path3/mask_variables_of_interest_Ant.nc


cdo ifthenc,2 -subc,1 -selvar,tmask $path3/mask_variables_of_interest_Ant.nc $path3/lsmask_0-2_Ant_withmiss.nc  
cdo setmisstoc,0 $path3/lsmask_0-2_Ant_withmiss.nc $path3/lsmask_0-2_Ant.nc 

cdo ifthenc,1 -selvar,isf_draft $path3/mask_variables_of_interest_Ant.nc $path3/isfmask_1_Ant_withmiss.nc 
cdo setmisstoc,0 $path3/isfmask_1_Ant_withmiss.nc $path3/isfmask_1_Ant.nc 

cdo add $path3/lsmask_0-2_Ant.nc $path3/isfmask_1_Ant.nc $path3/lsmask_0-1-2_andsome3s_Ant.nc
cdo mul -lec,2 $path3/lsmask_0-1-2_andsome3s_Ant.nc $path3/lsmask_0-1-2_andsome3s_Ant.nc $path3/lsmask_0-1-2_Ant_nonfloat.nc
cdo mulc,1.0 $path3/lsmask_0-1-2_Ant_nonfloat.nc $path3/lsmask_0-1-2_Ant.nc 

#cdo gtc,0 -selvar,tmask_2 $path3/mask_variables_of_interest_Ant.nc $path3/lsmask_0-1_3d_Ant.nc

#for yy in {1982..2013}
for yy in {2014..2100}
do 
echo $yy
cdo  sellonlatbox,0,360,-90,-50 $path2/variables_of_interest-"$nemo_run"_"$yy".nc $path3/variables_of_interest_"$yy"_Ant_wolandmask.nc
done

################################ STOP HERE ###########
#### USING SO TO DO THE MASK BUT LED TO A LINE NEAR AMERY
cdo gtc,0 -selvar,bathy_metry $path3/mask_variables_of_interest_Ant.nc $path2/mask_ocean.nc
cdo subc,1 $path2/mask_ocean.nc $path3/lsmask_-1-0_Ant_withmiss.nc
cdo ifthenc,2 $path3/lsmask_-1-0_Ant_withmiss.nc $path3/lsmask_0-2_Ant_withmiss.nc  
cdo setmisstoc,0 -seltimestep,1 $path3/lsmask_0-2_Ant_withmiss.nc $path3/lsmask_0-2_Ant.nc 

cdo ifthenc,1 -selvar,isf_draft $path3/mask_variables_of_interest_Ant.nc $path3/isfmask_1_Ant_withmiss.nc 
cdo setmisstoc,0 $path3/isfmask_1_Ant_withmiss.nc $path3/isfmask_1_Ant.nc 

cdo add $path3/lsmask_0-2_Ant.nc $path3/isfmask_1_Ant.nc $path3/lsmask_0-1-2_andsome3s_Ant.nc
cdo lec,2 $path3/lsmask_0-1-2_andsome3s_Ant.nc $path3/lsmask_below2s_Ant.nc
cdo mul $path3/lsmask_below2s_Ant.nc $path3/lsmask_0-1-2_andsome3s_Ant.nc $path3/lsmask_0-1-2_Ant_nonfloat.nc
cdo mulc,1.0 $path3/lsmask_0-1-2_Ant_nonfloat.nc $path3/lsmask_0-1-2_Ant.nc 
