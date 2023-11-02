import RasterHelpers.rasterGroup as rg
import RasterHelpers.rasterDirFiles as df
import RasterHelpers.rasterObject as ro
import arcpy
g = rg.RasterGroup()
ps = df.RasterDirTool(r'H:\Python\Projects\YZRiver\Data\HDF\2003')
files = ps.select_files('*.hdf')


o = ro.RasterObject()
o.load(files[1])
o1 = o.sub_raster_by_bands(r'H:\Python\Projects\YZRiver\Data\Test\2003\a.tif',0)
#print(o1.filename)
#o1.set_float()
print(type(o1.raster))
print(o1.path)
print(o1.maximum)
print(o1.minimum)
print(o1.mean)
o2 = o1 * 2
print(o2.set_float().self_mul(3.0).value_properties)
print(o1.raster.name)



