#coding=utf-8
from rasterDirFiles import *
from rasterTools import RasterTools

class RasterConvertor:

    def __init__(self, data_path = None, out_path =None):
        self._data_dir_tool = RasterDirTool()
        self._out_dir_tool = RasterDirTool()
        self._file_tool  = RasterFileTool()
        self._out_file_tool = RasterFileTool()
        self._ras_tool = RasterTools()
        self._data_dir = ''
        self._out_dir = ''
        if not data_path is None:
            self._data_dir_tool.set_path(data_path)
        if not out_path is None:
            self._out_dir_tool.set_path(out_path)

    def set_data_path(self, path):
        self._data_dir = path
        self._data_dir_tool.set_path(path)

    def set_out_path(self, path):
        self._out_dir = path
        self._out_dir_tool.set_path(path)

    def extract_band(self, band=0,prefix='xtr_',filter='*.hdf',outext='.tif'):
        rasters = self._data_dir_tool.select_files(filter=filter)
        print(self._out_dir_tool.path)
        for ras in rasters:
            self._file_tool.set_path(ras)
            self._file_tool.set_director(self._out_dir_tool.path)
            self._file_tool.set_file_name(prefix + \
                                          self._file_tool.file_name_without_ext + \
                                          outext)
            #self._ras_tool.extract_by_bands(ras,band,self._file_tool.path)
            print(self._file_tool.path)

    def extract_band_from_dir(self, band=0, prefix='xtr_', filter='*.hdf', has_sub_dir=True):
        self.extract_band(band=band, prefix=prefix, filter=filter)
        if has_sub_dir:
            sub_dirs = self._data_dir_tool.sub_dirs(full_path=False)
            d_dir = self._data_dir_tool.path
            o_dir = self._out_dir_tool.path
            for s_dir in sub_dirs:
                self._data_dir_tool.add_sub_dir(s_dir,d_dir)
                self._out_dir_tool.add_sub_dir(s_dir,o_dir)
                self._out_dir_tool.make_dir()
                self.extract_band(band=band, prefix=prefix, filter=filter)
            self._data_dir_tool.set_path(d_dir)
            self._out_dir_tool.set_path(o_dir)

    def set_data_path(self, path):
        self._data_dir = path
        self._data_dir_tool.set_path(path)

    def set_out_path(self, path):
        self._out_dir = path
        self._out_dir_tool.set_path(path)

    def mosaic_from_dir_including_sub(self, old_prefix='xtr_', new_prefix='Mosaic_', \
                        filter='*.tif', outext='.tif', \
                        raster_type = 'MODIS',\
                        pixeltype = "16_BIT_SIGNED", \
                        word_start = 8, \
                        word_end = 16, \
                        band=1, \
                        mosaicmethod='MEAN'):
        self.mosaic_from_dir(old_prefix=old_prefix, new_prefix=new_prefix, \
                        filter=filter, outext=outext, \
                        raster_type=raster_type, \
                        pixeltype=pixeltype, \
                        word_start=word_start, \
                        word_end=word_end, \
                        band=band, \
                        mosaicmethod=mosaicmethod)
        sub_dirs = self._data_dir_tool.sub_dirs(full_path=False)
        d_dir = self._data_dir_tool.path
        o_dir = self._out_dir_tool.path
        for s_dir in sub_dirs:
            self._data_dir_tool.add_sub_dir(s_dir, d_dir)
            self._out_dir_tool.add_sub_dir(s_dir, o_dir)
            self._out_dir_tool.make_dir()
            self.mosaic_from_dir(old_prefix=old_prefix, new_prefix=new_prefix, \
                                 filter=filter, outext=outext, \
                                 raster_type=raster_type, \
                                 pixeltype=pixeltype, \
                                 word_start=word_start, \
                                 word_end=word_end, \
                                 band=band, \
                                 mosaicmethod=mosaicmethod)
            self._data_dir_tool.set_path(d_dir)
            self._out_dir_tool.set_path(o_dir)

    def extract_to_region_from_dir(self,maskfile,filter='*.tif',\
                                   save_file=True,\
                                   prefix='Region_',\
                                   file_ext = '.tif',\
                                   startw=0,starte=-1):
        sub_dirs = self._data_dir_tool.sub_dirs(full_path=False)
        d_dir = self._data_dir_tool.path
        o_dir = self._out_dir_tool.path
        for s_dir in sub_dirs:
            self._data_dir_tool.add_sub_dir(s_dir, d_dir)
            self._out_dir_tool.add_sub_dir(s_dir, o_dir)
            self._out_dir_tool.make_dir()
            sub_files = self._data_dir_tool.select_files(filter=filter,\
                                                         full_path=False)
            for f in sub_files:
                if save_file:
                    if starte==-1:
                        starte = len(f)
                    outfile = self._out_dir_tool.path + prefix + f[startw:starte]+file_ext
                else:
                    outfile = None
                inras = self._data_dir_tool.path + f
                self._ras_tool.extract_by_mask(inRaster=inras,\
                                               maskfile=maskfile,\
                                               outfile=outfile)
        self._data_dir_tool.set_path(d_dir)
        self._out_dir_tool.set_path(o_dir)

    def NDVI_stard(self,filter='*.tif', prefix='FVC_',out_ext='.tif',startw=0,starte=-1):
        sub_dirs = self._data_dir_tool.sub_dirs(full_path=False)
        d_dir = self._data_dir_tool.path
        o_dir = self._out_dir_tool.path
        for s_dir in sub_dirs:
            self._data_dir_tool.add_sub_dir(s_dir, d_dir)
            self._out_dir_tool.add_sub_dir(s_dir, o_dir)
            self._out_dir_tool.make_dir()
            sub_files = self._data_dir_tool.select_files(filter=filter, \
                                                         full_path=False)
            for f in sub_files:
                if starte == -1:
                    starte = len(f)
                outfile = self._out_dir_tool.path + prefix + f[startw:starte] + out_ext

                inras = self._data_dir_tool.path + f
                fvc_ras = self._ras_tool.ndvi_to_fvc(inras)
                fvc_ras.save(outfile)
        self._data_dir_tool.set_path(d_dir)
        self._out_dir_tool.set_path(o_dir)

    def NDVI_to_FVC(self,filter='*.tif', prefix='FVC_',out_ext='.tif',startw=0,starte=-1):
        sub_dirs = self._data_dir_tool.sub_dirs(full_path=False)
        d_dir = self._data_dir_tool.path
        o_dir = self._out_dir_tool.path
        for s_dir in sub_dirs:
            self._data_dir_tool.add_sub_dir(s_dir, d_dir)
            self._out_dir_tool.add_sub_dir(s_dir, o_dir)
            self._out_dir_tool.make_dir()
            sub_files = self._data_dir_tool.select_files(filter=filter, \
                                                         full_path=False)
            for f in sub_files:
                if starte == -1:
                    starte = len(f)
                outfile = self._out_dir_tool.path + prefix + f[startw:starte] + out_ext

                inras = self._data_dir_tool.path + f
                fvc_ras = self._ras_tool.ndvi_to_fvc(inras)
                fvc_ras.save(outfile)
        self._data_dir_tool.set_path(d_dir)
        self._out_dir_tool.set_path(o_dir)













































