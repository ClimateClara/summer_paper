
inputpath=/bettik/kittelc/clara
outputpath=/bettik/burgardc/DATA/SUMMER_PAPER/raw/CMIP_DATA/tas_data

#for mod in {ACCESS-ESM1-5}
mod=ACCESS-ESM1-5
#do
echo $mod
echo "historical"
cdo fldmean $inputpath/tas_Amon_"$mod"_historical_r11i1p1f1_gn_185001-201412.nc $outputpath/$mod/tas_Amon_"$mod"_historical_r11i1p1f1_gn_185001-201412_fldmean.nc
cdo yearmean $outputpath/$mod/tas_Amon_"$mod"_historical_r11i1p1f1_gn_185001-201412_fldmean.nc $outputpath/$mod/tas_Amon_"$mod"_historical_r11i1p1f1_gn_185001-201412_fldmean_ymean.nc
for scen in {ssp126,ssp245,ssp585}
do
echo $scen
cdo fldmean $inputpath/tas_Amon_"$mod"_"$scen"_r11i1p1f1_gn_201501-210012.nc $outputpath/$mod/tas_Amon_"$mod"_"$scen"_r11i1p1f1_gn_201501-210012_fldmean.nc
cdo yearmean $outputpath/$mod/tas_Amon_"$mod"_"$scen"_r11i1p1f1_gn_201501-210012_fldmean.nc $outputpath/$mod/tas_Amon_"$mod"_"$scen"_r11i1p1f1_gn_201501-210012_fldmean_ymean.nc
done
#done
