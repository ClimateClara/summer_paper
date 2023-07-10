#!/bin/bash

#########
#This script is to format the raw NEMO data for further use 
#It extracts the interesting variables and adds the right grid information needed to regrid it in the next step
########

homepath=/bettik/burgardc

#### name of NEMO run
#nemo_run=ctrl94
#nemo_run=isf94
nemo_run=isfru94

################# DECLARE THE PATHS ##############################
path1=$homepath/DATA/SUMMER_PAPER/raw/CHRISTOPH_DATA
path2=$homepath/DATA/SUMMER_PAPER/interim/CHRISTOPH_"$nemo_run"
path3=$homepath/DATA/SUMMER_PAPER/interim/NEMO_"$nemo_run"_ANT_STEREO
path5=$homepath/DATA/SUMMER_PAPER/raw
###################################################################

#cdo splityear $path1/fwfisf-eANT025.L121-"$nemo_run"-1y_1982-2013.nc $path2/fwfisf-eANT025.L121-"$nemo_run"_
#cdo splityear $path1/thetao-eANT025.L121-"$nemo_run"-1y_1982-2013.nc $path2/thetao-eANT025.L121-"$nemo_run"_
#cdo splityear $path1/so-eANT025.L121-"$nemo_run"-1y_1982-2013.nc $path2/so-eANT025.L121-"$nemo_run"_

cdo splityear $path1/fwfisf-eANT025.L121-"$nemo_run"-1y_2014-2100.nc $path2/fwfisf-eANT025.L121-"$nemo_run"_
cdo splityear $path1/thetao-eANT025.L121-"$nemo_run"-1y_2014-2100.nc $path2/thetao-eANT025.L121-"$nemo_run"_
cdo splityear $path1/so-eANT025.L121-"$nemo_run"-1y_2014-2100.nc $path2/so-eANT025.L121-"$nemo_run"_

#for yy in {1982..2013}
for yy in {2014..2100}
do 
echo $yy
cdo merge $path2/fwfisf-eANT025.L121-"$nemo_run"_"$yy".nc $path2/thetao-eANT025.L121-"$nemo_run"_"$yy".nc $path2/so-eANT025.L121-"$nemo_run"_"$yy".nc $path2/variables_of_interest-"$nemo_run"_"$yy".nc
done

cdo setgrid,$path2/variables_of_interest-"$nemo_run"_2015.nc $path1/domain_cfg_eANT025.L121.nc $path2/domain_cfg_eANT025.L121_setgrid.nc
#$path1/eANT025.L121_grid_T_cdo.nc

for yy in {2014..2100}
do 
echo $yy
cdo sellonlatbox,0,360,-90,-50 $path2/variables_of_interest-"$nemo_run"_"$yy".nc $path3/variables_of_interest_"$yy"_Ant.nc
done
cdo sellonlatbox,0,360,-90,-50 -selgrid,1 $path2/domain_cfg_eANT025.L121_setgrid.nc $path3/mask_variables_of_interest_Ant.nc

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