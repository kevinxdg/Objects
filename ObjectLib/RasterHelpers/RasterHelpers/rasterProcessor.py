#coding=utf-8
from rasterDirFiles import *
from rasterTools import *
from rasterGroup import *
from rasterTiming import *

class RasterProcessor:
    def __init__(self):
        self._data_dir_tool = RasterDirTool()
        self._out_dir_tool = RasterDirTool()
        self._file_tool  = RasterFileTool()
        self._ras_tool = RasterTools()
        self._ras_group = RasterGroup()
        self._timer = timer()


    def set_data_path(self, path):
        self._data_dir_tool.set_path(path)

    def set_out_path(self, path):
        self._out_dir_tool.set_path(path)

    def key_words(self, ras_names, key_start, key_end, prefix='', ext='', full_path=True):
        keys = []
        for f in ras_names:
            if full_path:
                self._file_tool.set_path(f)
                fname = self._file_tool.file_name_without_ext
            else:
                fs  = f.split('.')
                flast = fs[-1]
                index = len(f) - len(flast)
                fname = f[0:index]
            key = prefix + fname[key_start:key_end + 1] + ext
            keys.append(key)
        return keys


    # 数据文件名称识别及分类
    def modis_date_info(self, file_name, key_start, mode='days'):
        p_list = file_name[key_start:key_start+7]
        m_year = int(p_list[0:4])
        m_month_or_days = int(p_list[4:7])
        if mode=='days':
            new_day =  self._timer.year_days_to_date(m_year,m_month_or_days)
            result = [new_day.year,new_day.month,new_day.day]
        elif mode=='month':
            result = [m_year,m_month_or_days,0]
        else:
            result = []
        return(result)

    def gimms_filename_info(self, file_name, key_start):
        fname = file_name[key_start:key_start+8]
        g_year = int(fname[0:2])
        if g_year < 30:
            g_year = 2000 + g_year
        else:
            g_year = 1900 + g_year
        g_month = self._timer.abbr_name_to_month(fname[2:5])
        if fname[-1]=='a':
            g_half = 0
        else:
            g_half = 1
        return [g_year,g_month,g_half]

    def filename_to_month(self,file_name,key_start, year,month,day,\
                          prefix='',file_ext='.tif',left_part=False,right_part=False):
        #
        new_day = self._timer.new_day(year,month,day)
        fname = self._timer.formated_time_string(new_day,pattern='%04Y%03m')
        if (not left_part) or (key_start==0):
            lpart = ''
        else:
            lpart = file_name[0:key_start]

        fnames = file_name.split('.')
        fext = fnames[-1]
        flen = len(file_name) - 1 - len(fext)
        if (not right_part) or (key_start + 8 > flen):
            rpart = ''
        else:
            rpart = file_name[key_start+8:flen]
        return (prefix + lpart + fname + rpart + file_ext)

    def modis_filename_to_month(self, file_name, key_start, \
                          prefix='', file_ext='.tif', left_part=False, right_part=False):
        [y, m, d] = self.modis_date_info(file_name=file_name, key_start=key_start)
        new_fname = self.filename_to_month(file_name=file_name,key_start=key_start,\
                                           year=y,month=m,day=1,\
                                           prefix=prefix,file_ext=file_ext,\
                                           left_part=left_part,right_part=right_part)
        return new_fname

    def gimms_filename_to_month(self, file_name, key_start, \
                          prefix='', file_ext='.tif', left_part=False, right_part=False):
        [y, m, d] = self.gimms_filename_info(file_name=file_name, key_start=key_start)
        new_fname = self.filename_to_month(file_name=file_name,key_start=key_start,\
                                           year=y,month=m,day=1,\
                                           prefix=prefix,file_ext=file_ext,\
                                           left_part=left_part,right_part=right_part)
        return new_fname

    def group_files_by_name(self, key_start, key_end, filter='*.*', full_path=True):
        files = self._data_dir_tool.select_files(filter=filter, full_path=full_path)
        key_words_list = []
        groups = []
        for f in files:
            key_words = f[key_start:key_end]
            if full_path:
                f_path = self._data_dir_tool.director + f
            else:
                f_path = f
            if key_words=='' or (not key_words in key_words_list):
                key_words_list.append(key_words)
                tmp_f_list = [f_path]
                groups.append(tmp_f_list)
            else:
                index = key_words_list.index(key_words)
                groups[index].append(f_path)
        return [groups, key_words_list]


    def extract_bands(self,key_start = 0, key_end = -2, filter='*.tif', index_collection = 0, prefix='extr_', file_ext='.tif' ):
        ras_files = self._data_dir_tool.select_files(filter=filter)
        ras_group = RasterGroup()
        ras_group.load_rasters(ras_files)
        ras_names = self.key_words(ras_names=ras_files, \
                                   key_start=key_start,\
                                   key_end = key_end,\
                                   prefix=prefix,ext=file_ext)


        ras_group.extract_bands(out_dir=self._out_dir_tool.path,\
                                out_names=ras_names,\
                                index_collection=index_collection)

    def mosaic_modis(self,key_start = 0, key_end = -2, filter='*.tif', prefix='mosaic_', file_ext='.tif' ):
        [groups, keywords] = self.group_files_by_name(key_start=key_start,key_end=key_end,filter=filter)
        ras_group = RasterGroup()
        for i in range(len(groups)):
            group = groups[i]
            key_word = keywords[i]
            ras_group.load_rasters(group)
            out_dir = self._out_dir_tool.path
            out_name = prefix + key_word + file_ext
            ras_group.mosaic(out_dir=out_dir,out_name=out_name)

    def process(self,task, **kwargs):
        s_dirs = self._data_dir_tool.sub_dirs(full_path=False)
        inpath = self._data_dir_tool.path
        outpath = self._out_dir_tool.path
        for s_dir in s_dirs:
            self._data_dir_tool.set_path(inpath + s_dir)
            self._out_dir_tool.set_path(outpath + s_dir)
            self._out_dir_tool.make_dir()
            if task.lower() == 'extract':
                self.extract_bands(**kwargs)
            elif task.lower() == 'mosaic':
                self.mosaic_modis(**kwargs)











