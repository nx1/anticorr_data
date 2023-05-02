echo making dirs...
mkdir supplementary_data/lightcurves/xrt/csv/ -p -v
mkdir supplementary_data/lightcurves/uvot/fits -p -v
mkdir supplementary_data/lightcurves/joined/fits -p -v
mkdir supplementary_data/lightcurves/joined/all -p -v
mkdir supplementary_data/tables/csv -p -v


echo copying readme...
cp supplementary_readme.txt supplementary_data/ 

echo copying to lightcurves/xrt/csv ...
cp lightcurves/xrt/*.csv supplementary_data/lightcurves/xrt/csv #-v 

echo copying to lightcurves/uvot/fits ...
cp lightcurves/uvot/*.fits supplementary_data/lightcurves/uvot/fits -v

echo copying to lightcurves/joined/fits/ ...
cp lightcurves/joined/*.fits supplementary_data/lightcurves/joined/fits/ -v

echo copying to lightcurves/joined/all/ ...
cp lightcurves/joined_all/*.csv supplementary_data/lightcurves/joined/all/ -v

#echo copying to tables/tex ...
#cp tables/*.tex supplementary_data/tables/tex -v

echo copying to tables/csv ...
cp tables/*.csv supplementary_data/tables/csv -v

echo removing junk csvs ...
rm supplementary_data/tables/csv/xrt_lc_analysis.csv
rm supplementary_data/tables/csv/xmmmaster_n_obs.cs
rm supplementary_data/tables/csv/xmmmaster.csv
rm supplementary_data/tables/csv/uvot_n_obs.csv
rm supplementary_data/tables/csv/uvot_lc_analysis.csv
rm supplementary_data/tables/csv/numaster_n_obs.csv
rm supplementary_data/tables/csv/nustarmaster.csv
rm supplementary_data/tables/csv/query_local_sources.csv
rm supplementary_data/tables/csv/query_simbad.csv
rm supplementary_data/tables/csv/query_simbad_earnshaw.csv
rm supplementary_data/tables/csv/simulation_n_obs.csv

echo zipping files ...
zip -r supplementary.zip supplementary_data/
