#coding=utf-8
from genModule import *
import rasterObject as ro

class RasterTools:
    def print_hi(self):
        print(r'Hi')

    # 提取指定波段
    def extract_by_bands(self, inRaster, index_collection, outfile):
        data = arcpy.ExtractSubDataset_management(inRaster, outfile, index_collection)
        return (ro.RasterObject(data))

    def extract_by_bands_for_groups(self,in_rasters, index_collection, outdir, outfiles):
        extract_list = []
        for i in range(len(in_rasters)):
            ras = in_rasters[i]
            tmp_obj = self.extract_by_bands(inRaster=ras,index_collection=index_collection,\
                                            outfile=outdir+outfiles[i])
            extract_list.append(tmp_obj)
        return extract_list


    # 按属性值提取子集
    def extract_by_attributes(self,inRaster,where_clause, outfile=None):
        out_ras = arcpy.sa.ExtractByAttributes(inRaster, where_clause)
        if not outfile is None:
            out_ras.save(outfile)
        return ro.RasterObject(out_ras)


    # 图幅拼接
    def mosaic(self,inRasters, outDir, outName, \
                    pixeltype="16_BIT_SIGNED", \
                    band=1, \
                    mosaicmethod='MEAN'):
        out_ras = arcpy.MosaicToNewRaster_management(inRasters, outDir, outName, \
                                           pixel_type=pixeltype, \
                                           number_of_bands=band, \
                                           mosaic_method=mosaicmethod)
        return ro.RasterObject(out_ras)



    def mosaic_for_groups(self, in_ras_groups, out_dir,out_names,\
                                      pixeltype="16_BIT_SIGNED", \
                                      band=1, \
                                      mosaicmethod='MEAN'):
        ras_list = []
        for i in range(len(in_ras_groups)):
            g_ras = in_ras_groups[i]
            ras_obj=self.mosaic(inRasters=g_ras,\
                                outDir = out_dir,\
                                outName= out_names[i],\
                        pixeltype=pixeltype,\
                        band=band,\
                        mosaicmethod=mosaicmethod)
            ras_list.append(ras_obj)

        return ras_list


    # 图幅剪切
    def extract_by_mask(self,inRaster, maskfile, outfile=None):
        out_ras = arcpy.sa.ExtractByMask(inRaster, maskfile)  # 裁剪
        if not outfile is None:
            out_ras.save(outfile)
        return ro.RasterObject(out_ras)

    def extract_by_mask_for_groups(self,in_raster_groups, mask_file, outdir=None,out_files=None):
        extract_list = []
        for i in range(len(in_raster_groups)):
            ras = in_raster_groups[i]
            if isinstance(out_files,list):
                outfile = outdir + out_files[i]
            else:
                outfile = None
            tmp_obj = self.extract_by_mask(inRaster=ras,maskfile=mask_file,outfile=outfile)
            extract_list.append(tmp_obj)
        return extract_list

    # NDVI 计算 FVC
    def ndvi_to_fvc(self, inRaster):
        if isinstance(inRaster,str):
            tmp_ras = ro.RasterObject(inRaster)
        elif isinstance(inRaster,arcpy.Raster):
            tmp_ras = ro.RasterObject(inRaster)
        elif isinstance(inRaster,ro.RasterObject):
            tmp_ras = inRaster
        tmp_in = (tmp_ras.raster - tmp_ras.value_percentile_05) / \
                 (tmp_ras.value_percentile_95 - tmp_ras.value_percentile_05)
        tmp_in_1 = arcpy.sa.Con(tmp_in, 0, tmp_in, "value < 0")
        result = arcpy.sa.Con(tmp_in_1, 1, tmp_in_1, "value > 1")
        return ro.RasterObject(result)

    def ndvi_to_fvc_for_groups(self,in_raster_groups):
        fvc_list = []
        for ras in in_raster_groups:
            tmp_obj = self.ndvi_to_fvc(ras)
            fvc_list.append(tmp_obj)
        return fvc_list

    # 计算 求和
    def sum(self, inRasters):
        result = 0
        for ras in inRasters:
            result = result + ras
        return ro.RasterObject(result)

    # 计算 平均值
    def mean(self,inRasters):
        result = self.sum(inRasters) / len(inRasters)
        return ro.RasterObject(result)

    def mean_for_groups(self,in_raster_groups):
        mean_list = []
        for group in in_raster_groups:
            m_obj = self.mean(group)
            mean_list.append(m_obj)
        return mean_list














