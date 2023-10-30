
inputpath=/bettik/burgardc/DATA/SUMMER_PAPER/raw/CMIP_DATA/tas_data
outputpath=/bettik/burgardc/DATA/SUMMER_PAPER/interim/CMIP_TEMP

for mod in {CNRM-CM6-1,CNRM-ESM2-1,GISS_E2-1-H,CESM2-WACCM,CESM2,CanESM5,IPSL-CM6A-LR,MRI-ESM2-0,MPI-ESM1-2-HR,GFDL-CM4,GFDL-ESM4,UKESM1-0-LL} #ACCESS-CM2,ACCESS-ESM1-5} #,
for mod in {CESM2,MRI-ESM2-0} #ACCESS-CM2,ACCESS-ESM1-5} #,
do
echo $mod
echo "historical"
cdo mergetime $inputpath/tas_Amon_"$mod"_historical_*.nc $outputpath/$mod/tas_Amon_"$mod"_historical.nc
cdo fldmean $outputpath/$mod/tas_Amon_"$mod"_historical.nc $outputpath/$mod/tas_Amon_"$mod"_historical_fldmean.nc
cdo yearmean $outputpath/$mod/tas_Amon_"$mod"_historical_fldmean.nc $outputpath/$mod/tas_Amon_"$mod"_historical_fldmean_ymean.nc
for scen in {ssp126,ssp245,ssp585}
do
echo $scen
cdo mergetime $inputpath/tas_Amon_"$mod"_"$scen"_*.nc $outputpath/$mod/tas_Amon_"$mod"_"$scen".nc
cdo fldmean $outputpath/$mod/tas_Amon_"$mod"_"$scen".nc $outputpath/$mod/tas_Amon_"$mod"_"$scen"_fldmean.nc
cdo yearmean $outputpath/$mod/tas_Amon_"$mod"_"$scen"_fldmean.nc $outputpath/$mod/tas_Amon_"$mod"_"$scen"_fldmean_ymean.nc
done
done
