#coding=utf-8
import arcpy

from genModule import  *
import dataframeObject as dfo

class RasterObject:
    def print_hi(self):
        print(self)

    def __init__(self, in_raster=None):
        self.load(in_raster)

    # 文件操作相关方法
    # ------------------------------
    def save(self, path = None):
        if path is None:
            path = self.raster.path
        self.raster.save(path)

    def load(self, in_raster):
        if isinstance(in_raster,str):
            self.raster = arcpy.Raster(in_raster)
        elif isinstance(in_raster,arcpy.Raster):
            self.raster = in_raster
        else:
            self.raster = None
        if hasattr(self, '_list'):
            delattr(self, '_list')
        if hasattr(self, '_array'):
            delattr(self, '_array')
        if hasattr(self, '_value_list'):
            delattr(self, '_value_list')

    # 栅格文件相关属性
    #----------------------------------------------------------------

    @property
    def path(self):
        if isinstance(self.raster,arcpy.Raster):
            return self.raster.path
        else:
            return ''


    # 栅格数据相关属性
    # ----------------------------------
    # --------------------------------
    #获取栅格数据的各类属性
    # --------------------------------
    #像元最小值
    @property
    def minimum(self):
        result = arcpy.GetRasterProperties_management(self.raster,"MINIMUM")
        return result.getOutput(0)

    #像元最大值
    @property
    def maximum(self):
        result = arcpy.GetRasterProperties_management(self.raster,"MAXIMUM")
        return result.getOutput(0)


    #像元平均值
    @property
    def mean(self):
        result =  arcpy.GetRasterProperties_management(self.raster,"MEAN")
        return result.getOutput(0)

    # 像元标准差
    @property
    def std(self):
        result = arcpy.GetRasterProperties_management(self.raster, "STD")
        return result.getOutput(0)

    @property
    def top(self):
        result = arcpy.GetRasterProperties_management(self.raster, "TOP")
        return result.getOutput(0)

    @property
    def left(self):
        result = arcpy.GetRasterProperties_management(self.raster, "LEFT")
        return result.getOutput(0)

    @property
    def right(self):
        result = arcpy.GetRasterProperties_management(self.raster, "RIGHT")
        return result.getOutput(0)

    @property
    def bottom(self):
        result = arcpy.GetRasterProperties_management(self.raster, "BOTTOM")
        return result.getOutput(0)

    @property
    def cell_size_x(self):
        result = arcpy.GetRasterProperties_management(self.raster, "CELLSIZEX")
        return result.getOutput(0)

    @property
    def cell_size_y(self):
        result = arcpy.GetRasterProperties_management(self.raster, "CELLSIZEY")
        return result.getOutput(0)

    @property
    def value_type(self):
        result = arcpy.GetRasterProperties_management(self.raster, "VALUETYPE")
        return result.getOutput(0)

    @property
    def value_properties(self):
        values = [self.value_percentile_05,self.value_percentile_25,\
                  self.value_percentile_50,self.value_percentile_75, \
                  self.value_percentile_95,\
                  self.mean, self.std, self.top, self.left, \
                  self.right, self.bottom, self.cell_size_x,\
                  self.cell_size_y]
        columns = ['pct05', 'pct25', 'pct50', 'pct75', 'pct95', \
                   'mean', 'std','top','left','right','bottom',\
                   'cellsizex','cellsizey']
        value_dataframe = dfo.DataFrameClass(data=[values],columns=columns)
        return(value_dataframe)


    # 运算相关方法
    def __add__(self, other):
        tmp_ras = self.raster + other
        return RasterObject(tmp_ras)

    def __mul__(self, other):
        tmp_ras = self.raster * other
        return RasterObject(tmp_ras)

    def __sub__(self, other):
        tmp_ras = self.raster - other
        return RasterObject(tmp_ras)

    def __div__(self, other):
        tmp_ras = self.raster / other
        return RasterObject(tmp_ras)

    def __radd__(self, other):
        return self.__add__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def set_float(self):
        self.raster = arcpy.sa.Float(self.raster)
        return self

    def set_int(self):
        self.raster = arcpy.sa.Int(self.raster)
        return self

    def self_add(self,value):
        self.raster = self.raster + value
        return self

    def self_sub(self,value):
        self.raster = self.raster - value
        return self

    def self_mul(self,value):
        self.raster = self.raster * value
        return self

    def self_div(self,value):
        self.raster = self.raster / value
        return self

    # 栅格数据生成二维数组
    @property
    def to_array(self):
        if not hasattr(self,'_array'):
            self._array = arcpy.RasterToNumPyArray(self.raster)
        return self._array

    # 栅格数据生成一维列表
    @property
    def to_list(self):
        if not hasattr(self,'_list'):
            __list = self.to_array.tolist()
            self._list = [i for item in __list for i in item]
        return self._list

    # 栅格数据去除
    @property
    def value_list(self):
        if not hasattr(self,'_value_list'):
            self._value_list = self.get_list_by_values(\
                value_min=self.raster.minimum, \
                value_max=self.raster.maximum)
            self._value_list.sort()
        return self._value_list

    # 不同分位数对应的值
    @property
    def value_percentile_05(self):
        return self.get_percentile(5)

    @property
    def value_percentile_25(self):
        return self.get_percentile(25)

    @property
    def value_percentile_50(self):
        return self.get_percentile(50)

    @property
    def value_percentile_75(self):
        return self.get_percentile(75)

    @property
    def value_percentile_95(self):
        return self.get_percentile(95)

    @property
    def value_percentiles(self):
        return [self.value_percentile_05,\
                self.value_percentile_25,\
                self.value_percentile_50,\
                self.value_percentile_75,\
                self.value_percentile_95]

    def get_list_by_values(self,value_min, value_max):
        tmp_list = []
        for value in self.to_list:
            if (value >= value_min) and (value <= value_max):
                tmp_list.append(value)
        return tmp_list

    def get_percentile(self,percent):
        return np.percentile(self.value_list,percent)

    # 按属性值提取子集
    def sub_raster_by_attributes(self,where_clause):
        out_ras = arcpy.sa.ExtractByAttributes(self.raster, where_clause)
        return RasterObject(out_ras)

    def sub_raster_by_mask(self,mask_file):
        out_ras = arcpy.sa.ExtractByMask(self.raster, mask_file)  # 裁剪
        return RasterObject(out_ras)


    def sub_raster_by_bands(self, outfile, index_collection):
        arcpy.ExtractSubDataset_management(self.raster, outfile, index_collection)
        return (RasterObject(outfile))

    def set_value_under_condition(self,t_value,f_value,str_conditon):
        self.raster = arcpy.sa.Con(self.raster, t_value, f_value, str_conditon)
        return self



    # 特别指标
    @property
    def FVC_index(self):
        tmp_ras = (self.raster - self.value_percentile_05) / \
                 (self.value_percentile_95 - self.value_percentile_05)
        ras = arcpy.sa.Con(tmp_ras, 0, tmp_ras, "value < 0")
        result = arcpy.sa.Con(ras, 1, ras, "value > 1")
        return RasterObject(result)


# 图像处理
















