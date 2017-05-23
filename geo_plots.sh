here=$PWD
cd ..
cp *.stl* $here/
cd $here
gzip -d *.gz
cp /net/fs1/data_1/home/work/AERO/Utilities/Aero_system/make_plot_geo/plot_geo.java .
/net/c3m/opt/CD-adapco/STAR-CCM+6.04.014/star/bin/starccm+ -rsh ssh -batch plot_geo.java
rm -f *.stl*

cp ../membrain.csv .
ln -s /net/fs1/data_1/home/work/AERO/Utilities/Sh/mem_csv_to_txt_v2/membrain_table.sh .

#copy above depower to figure out if it was morphed
cp ../JIBDEPOWER .
cp ../MAINDEPOWER .

sh membrain_table.sh

zip -r *.zip *.png geo.sce *.txt
