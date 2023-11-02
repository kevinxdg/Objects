#coding=utf-8
import os
import glob
from rasterTiming import timer

class RasterPathTool:
    def __init__(self, path=''):
        self._path = path

    @property
    def path(self):
        return self._path


    def set_path(self,path):
        self._path = path

    @property
    def norm_path(self):
        return os.path.normpath(self._path)

    @property
    def dir_and_object(self):
        if len(self._path)==0:
            return ['','']
        [dirpath, objname] = os.path.split(self._path)
        last_c = dirpath[-1]
        if last_c != os.path.sep:
            dirpath = dirpath + os.path.sep
        return  [dirpath, objname]

    @property
    def director(self):
        dirs = self.dir_and_object
        return dirs[0]

    def set_director(self, dirpath):
        dirs = self.dir_and_object
        last_c = dirpath[-1]
        if last_c != os.path.sep:
            dirpath = dirpath + os.path.sep
        self._path = dirpath + dirs[1]

    @property
    def object_name(self):
        dirs =self.dir_and_object
        return dirs[1]

    def set_object_name(self,objname):
        dirs = self.dir_and_object
        self._path = dirs[0] + objname


    @property
    def is_object(self):
        if len(self._path)<=0:
            return False
        last_c = self.path[-1]
        if last_c == os.sep:
            return False
        return True

    @property
    def is_path(self):
        return not self.is_object

    def set_is_object(self):
        if not self.is_object:
            self._path = self._path[:-1]

    def set_is_path(self):
        if self.is_object:
            self._path = self._path + os.sep

    @property
    def is_abstract(self):
        return os.path.isabs(self._path)

    @property
    def parent_path(self):
        pa = RasterPathTool(self.path)
        pa.set_is_object()
        return pa.director

    @property
    def parent_name(self):
        do = RasterPathTool(self.parent_path)
        do.set_is_object()
        return do.object_name

    def set_parent_name(self, pname):
        do = RasterPathTool(self.parent_path)
        do.set_is_object()
        do.set_object_name(pname)
        self.set_director(do.path)

    def replace_root(self,old_root,new_root,o_string=None):
        if o_string is None:
            o_string = self._path
        r_string = o_string.replace(old_root,new_root)
        return r_string

class RasterFileTool(RasterPathTool):
    def __init__(self, path=''):
        RasterPathTool.__init__(self,path)
        self.set_is_object()

    @property
    def is_file(self):
        return os.path.isfile(self.path)

    @property
    def file_exists(self):
        return os.path.exists(self.path)

    @property
    def file_name(self):
        return self.object_name

    def set_file_name(self,fname):
        self.set_object_name(fname)

    @property
    def file_extention(self):
        tmp_names = self.file_name.split('.')
        return '.' + tmp_names[-1]

    @property
    def file_name_without_ext(self):
        ext_len = len(self.file_extention)
        return self.file_name[:-ext_len]

    @property
    def file_extent(self):
        f_list = self.path.split('.')
        return '.' + f_list[-1]

    def file_remove(self):
        os.remove(self.path)

    def set_time_stamp_file_name(self,prefix='', file_ext='.tif', t_time=None, pattern='full_underline'):
        tm = timer(t_time)
        f_name = prefix + tm.formated_time_string(t_time,pattern=pattern) \
            + file_ext
        self.set_file_name(f_name)



class RasterDirTool(RasterPathTool):

    def __init__(self,path=''):
        RasterPathTool.__init__(self,path=path)
        self.set_is_path()

    @property
    def is_dir(self):
        return os.path.isdir(self.path)

    def set_is_object(self):
        pass

    def set_path(self,path):
        RasterPathTool.set_path(self,path=path)
        self.set_is_path()

    @property
    def dir_exists(self):
        return os.path.exists(self.path)

    def make_dir(self,path=None):
        if path is None:
            path = self.path
        if not os.path.exists(path):
            os.makedirs(path)

    @property
    def sub_objects(self):
        sub_objs = os.listdir(self.path)
        return sub_objs

    def sub_files(self,full_path=True):
        s_objs = self.sub_objects
        s_files = []
        for obj in s_objs:
            if(os.path.isfile(obj)):
                if full_path:
                    s_files.append(self.director + obj)
                else:
                    s_files.append(obj)
        return s_files

    def sub_dirs(self,full_path=True):
        s_objs = self.sub_objects
        s_dirs = []
        for obj in s_objs:
            if(os.path.isdir(self.director + obj)):
                if full_path:
                    s_dirs.append(self.director + obj)
                else:
                    s_dirs.append(obj)
        return s_dirs

    def select_files(self,filter='*.*', full_path=True):
        files = glob.glob1(self.path, filter)
        if full_path:
            for i in range(len(files)):
                files[i] = self.director + files[i]
        return files

    def filename_to_path(self, filenames):
        paths = []
        for f in filenames:
            path = self.director + f
            paths.append(path)
        return paths

    def add_sub_dir(self, sub_dir, root=None):
        if root is None:
            root = self.director
        self.set_path(root)
        self.set_object_name(sub_dir)
        self.set_is_path()
        return self.path






















