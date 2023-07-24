#!/bin/bash

#########
#This script is to move the CMIP data to my folder and separate it by years
########

homepath=/bettik/burgardc

mod=CNRM-CM6-1
scenario=historical
ensrun=r1i1p1f2

path1=/bettik/jourdai1/OCEAN_DATA_CMIP6_STEREO/$mod
path2=$homepath/DATA/SUMMER_PAPER/raw/CMIP_DATA/$mod
path3=$homepath/DATA/SUMMER_PAPER/interim

#######

cdo splityear $path1/thetao_Oyr_"$mod"_"$scenario"_"$ensrun"_185001_194912.nc $path2/thetao_Oyr_"$mod"_"$scenario"_"$ensrun"_
cdo splityear $path1/so_Oyr_"$mod"_"$scenario"_"$ensrun"_185001_194912.nc $path2/so_Oyr_"$mod"_"$scenario"_"$ensrun"_

cdo splityear $path1/thetao_Oyr_"$mod"_"$scenario"_"$ensrun"_195001_201412.nc $path2/thetao_Oyr_"$mod"_"$scenario"_"$ensrun"_
cdo splityear $path1/so_Oyr_"$mod"_"$scenario"_"$ensrun"_195001_201412.nc $path2/so_Oyr_"$mod"_"$scenario"_"$ensrun"_

