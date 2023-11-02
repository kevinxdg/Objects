#coding=utf-8

from genModule import *
from rasterObject import RasterObject
from dataframeObject import DataFrameClass
class RasterGroup():
    def __init__(self):
        self._raster_group = []
        self._group_name = ''

    @property
    def group_length(self):
        return len(self._raster_group)

    # 计算 求和
    @property
    def raster_sum(self):
        result = 0
        for ras in self._raster_group:
            ras_obj = RasterObject(ras)
            result = ras_obj + result
        return RasterObject(result)

    # 计算 平均值
    @property
    def raster_mean(self):
        result = self.raster_sum / self.group_length
        return RasterObject(result)

    def _find_item(self,str):
        for ras in self._raster_group:
            ras_obj = RasterObject(ras)
            if ras_obj.raster.name == str:
                return ras
        return None

    def __getitem__(self, index):
        if isinstance(index,int):
            ras_obj = RasterObject(self._raster_group[index])
            return ras_obj
        elif isinstance(index,str):
            return self._find_item(index)

    def add_raster(self,newRaster):
        self._raster_group.append(newRaster)

    def remove_raster(self,index):
        if index >=0 and index < self.group_length:
            self._raster_group.remove(index)

    def remove_all(self):
        self._raster_group = []

    def set_group_name(self,group_name):
        self._group_name = group_name

    def load_rasters(self, paths):
        for p in paths:
            self.add_raster(p)

    # 图像处理
    def extract_bands(self, out_dir, out_names, index_collection):
        bands = []
        for i in range(self.group_length):
            ras_obj = RasterObject(self._raster_group[i])
            outfile = out_dir + out_names[i]
            robj = ras_obj.sub_raster_by_bands(outfile, index_collection)
            bands.append(robj)
            print('[Extract Bands]' + outfile)
        return bands

    def mosaic(self, out_dir, out_name, mosaic_method='MEAN' ):
        ras_obj = RasterObject(self._raster_group[0])
        band = ras_obj.raster.bandCount
        out_ras = arcpy.MosaicToNewRaster_management(self._raster_group, out_dir, out_name,\
                                                     number_of_bands=band, \
                                                     mosaic_method=mosaic_method)
        return RasterObject(out_ras)

    def extract_by_mask(self, mask_file, out_dir=None,out_names=None):
        extr_group = RasterGroup()
        for i in range(self.group_length):
            obj = RasterObject(self._raster_group[i])
            extr = obj.sub_raster_by_mask(mask_file)
            if not out_dir is None:
                extr.save(out_dir+out_names[i])
            extr_group.add_raster(out_dir+out_names[i])
        return extr_group


    def cal_fvc_index(self, out_dir=None, out_names=None):
        fvc_group = RasterGroup()
        for i in range(self.group_length):
            obj = RasterObject(self._raster_group[i])
            fvc = obj.FVC_index
            fvc_group.add_raster(out_dir+out_names[i])
            if not out_dir is None:
                fvc.save(out_dir + out_names[i])
        return fvc_group

    @property
    def statistics(self):
        columns = ['pct05', 'pct25', 'pct50', 'pct75', 'pct95', \
                   'mean', 'std', 'top', 'left', 'right', 'bottom', \
                   'cellsizex', 'cellsizey']
        raster_stat = DataFrameClass(columns=columns)
        ras_obj = RasterObject()
        for ras in self._raster_group:
            print('-------------------')
            print(ras)
            ras_obj.load(ras)
            ras_properties = ras_obj.value_properties
            raster_stat.append(ras_properties)
        return raster_stat




































