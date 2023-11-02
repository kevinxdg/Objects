#from RasterHelpers import rasterObject as ro
#from RasterHelpers import rasterTools as rt
#from RasterHelpers.genModule import *
#arcpy.env.overwriteOutput = True

#t = rt.RasterTools()
#r = ro.RasterObject(r'H:\Python\Projects\YZRiver\Data\FVC\2003\season\FVC.A20030.spring.tif')
#r1 = t.extract_by_attributes(r'H:\Python\Projects\YZRiver\Data\FVC\2003\season\FVC.A20030.spring.tif','VALUE = 1')
#ndvi_f = r'H:\Python\Projects\YZRiver\Data\NDVI_mosaic\2003\NDVI.Mosaic.A2003001.tif'
#fvc_f = r'H:\Python\Projects\YZRiver\Data\Test\fvc.tif'
#fvc = t.ndvi_to_fvc(ndvi_f)
#fvc.raster.save(fvc_f)
#print(0+fvc.raster)

#ndvi_f = r'H:\Python\Projects\YZRiver\Data\NDVI_mosaic\2003\NDVI.Mosaic.A2003001.tif'
#fvc_f = r'H:\Python\Projects\YZRiver\Data\Test\fvc.tif'
#test = r'H:\Python\Projects\YZRiver\Data\HDF\2003\MOD13A3.A2003135.h28v06.006.2015154062157.hdf'
#import RasterHelpers.rasterDirFiles as df

#ph = df.RasterFileTool(test)
#print(ph.norm_path)
#print(ph.parent_path)
#print(ph.parent_name)
#info = ph.get_info_from_modis_filename()
#print(info)
#ph.set_modis_filename_to_month('MODIS')
#print(ph.path)

#ph.set_parent_name('2004')
#print(ph.path)
#ph.set_file_name('test.tif')
#print(ph.path)

#import RasterHelpers.rasterTiming as rt
#tm = rt.timer()
#t = datetime.datetime.now()
#print(tm.formated_time_string(t,'full_abbr_date_time'))
#t2 = datetime.datetime(1922,8,1,13,7,25)
#print(t2)
#print(tm.year_days_to_date(2003,52))
#ph.set_time_stamp_file_name('NDVI',pattern='ymd')
#print(ph.path)

#ps = df.RasterDirTool(r'H:\Python\Projects\YZRiver\Data\HDF\2003')
#print(ps.path)
#print(ps.sub_objects)
#print(ps.select_files('*.hdf'))
#print(ps.group_files_by_name(7,16,'*.hdf'))

#from RasterHelpers.rasterConvertor import RasterConvertor
#ps.set_is_object()
#rco = RasterConvertor()
#rco.set_data_path(r'H:\Python\Projects\YZRiver\Data\HDF')
#rco.set_out_path(r'H:\Python\Projects\YZRiver\Data\Test')




rco.extract_band_from_dir()
ps.add_sub_dir('Hello')
print (ps.parent_path)
rco.set_data_path(r'H:\Python\Projects\YZRiver\Data\Test')
rco.set_out_path(r'H:\Python\Projects\YZRiver\Data\Test2')
rco.mosaic_from_dir_including_sub()