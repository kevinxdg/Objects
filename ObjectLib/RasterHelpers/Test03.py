#coding=utf-8

import RasterHelpers.rasterGroup as rg
import RasterHelpers.rasterDirFiles as rdf

dir_tool = rdf.RasterDirTool()
dir_tool.set_path(r"H:\Python\Projects\YZRiver\Data\FVC\2003")
files = dir_tool.select_files("*.tif")
g = rg.RasterGroup()
print(len(files))
g.load_rasters(files)
print(g.statistics)

