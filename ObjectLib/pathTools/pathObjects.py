#coding=utf-8
import os, glob
class PathTool:
    def __init__(self, path=''):
        self._path = path

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self,path):
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
    
    @director.setter
    def director(self, dirpath):
        dirs = self.dir_and_object
        last_c = dirpath[-1]
        if last_c != os.path.sep:
            dirpath = dirpath + os.path.sep
        self._path = dirpath + dirs[1]

    @property
    def object(self):
        dirs =self.dir_and_object
        return dirs[1]
    
    @object.setter
    def object(self,objname):
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
    def parent(self):
        pa = PathTool(self.path)
        pa.set_is_object()   
        do = DirTool(pa.director)
        return do

    @property
    def parent_name(self):
        pa = self.parent
        pa.set_is_object()        
        return pa.object

class FileTool(PathTool):
    def __init__(self, path=''):
        PathTool.__init__(self,path)
        self.set_is_object()

    @property
    def is_file(self):
        return os.path.isfile(self.path)

    @property
    def file_exists(self):
        return os.path.exists(self.path)

    @property
    def file_name(self):
        return self.object
    
    @file_name.setter
    def file_name(self,fname):
        self.object = fname

    @property
    def file_ext(self):
        tmp_names = self.file_name.split('.')
        return '.' + tmp_names[-1]

    @property
    def file_name_without_ext(self):
        ext_len = len(self.file_extention)
        return self.file_name[:-ext_len]

    def file_remove(self):
        os.remove(self.path)

class DirTool(PathTool):
    def __init__(self,path=''):
        PathTool.__init__(self,path=path)
        self.set_is_path()
        
    @property
    def is_dir(self):
        return os.path.isdir(self.path)

    def set_is_object(self):
        pass

    def set_path(self,path):        
        PathTool.set_path(self,path=path)
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
            if(os.path.isfile(self.path + obj)):
                if full_path:
                    s_files.append(self.path + obj)
                else:
                    s_files.append(obj)
        return s_files
    
    def sub_files_with_new_path(self, inpath):
        files = self.sub_files(full_path=False)
        new_files = []
        for f in files:
            new_file = inpath + f
            new_files.append(new_file)
        return new_files
    
    def sub_dirs(self,full_path=True):
        s_objs = self.sub_objects
        s_dirs = []
        for obj in s_objs:
            if(os.path.isdir(self.path + obj)):
                if full_path:
                    s_dirs.append(self.path + obj)
                else:
                    s_dirs.append(obj)
        return s_dirs
    
    def sub_dirs_with_new_path(self, inpath):
        dirs = self.sub_dirs(full_path=False)
        new_dirs = []
        for d in dirs:
            new_dir = inpath + d
            new_dirs.append(new_dir)
        return new_dirs        

    def select_files(self,filter='*.*', full_path=True):
        files = glob.glob1(self.path, filter)
        if full_path:
            for i in range(len(files)):
                files[i] = self.director + files[i]
        return files

    def append_file(self, filename):
        fo = FileTool(self.path + filename)
        return fo
    
    def append_dir(self,dirname):
        do = DirTool(self.path + dirname)
        return do

