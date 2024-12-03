#coding=utf-8
import socket
import configparser
class ConfigureObject:

    def __init__(self, file_name = None):
        if self.hostname == 'KevinG-CPT':
            self._root_configs = r'H:\Python\Configs'
        elif self.hostname == 'KevinG-Office':
            self._root_configs = r'F:\WorkRooms\python\Configs'
        else:
            self._root_configs = r'.'
        self._filename = file_name
        self._conf = configparser.ConfigParser()
        self._section = ''
        self._option = ''
        self._sub_dir = ''


    def load_config(self):
        #self._path_configs = self._root_configs + '\\' + self._filename
        self._conf.read(self.file_path, encoding='utf-8')

    def load_config_from_file(self, file_name, section):
        self.filename = file_name
        self.load_config()
        self.section = section ##self._conf.hostname
        return dict(self.all_items)

    @property
    def hostname(self):
        return socket.gethostname()

    @property
    def root_configs(self):
        return self._root_configs

    @root_configs.setter
    def root_configs(self, value):
        self._root_configs = value

    @property
    def sub_dir(self):
        return self._sub_dir

    @sub_dir.setter
    def sub_dir(self, value):
        self._sub_dir = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def file_path(self):
        file_p = ''
        if self._sub_dir == '':
            file_p = self._root_configs + '\\' + self._filename
        else:
            file_p = self._root_configs + '\\' + self.sub_dir + "\\" + self._filename
        return file_p

    @property
    def sections(self):
        return self._conf.sections()

    @property
    def section(self):
        return self._section

    @section.setter
    def section(self, value):
        self._section = value

    @property
    def options(self):
        return self._conf.options(self._section)

    @property
    def option(self):
        return self._option

    @option.setter
    def option(self, value):
        self._option = value

    @property
    def all_items(self):
        return self._conf.items(self._section)

    @property
    def items(self):
        return dict(self.all_items)

    def _write(self):
        with open(self.file_path,'w', encoding='utf-8') as fp:
            self._conf.write(fp)

    def get_option_value(self, section=None, option=None):
        if section is None:
            section = self._section
        if option is None:
            option = self._option
        return self._conf.get(section, option)

    def set_option_value(self, value, section=None, option=None):
        if section is None:
            section = self._section
        if option is None:
            option = self._option
        self._conf.set(section,option,value)
        self._write()

    def add_section(self, section_name):
        self._conf.add_section(section_name)
        self._write()

    def remove_section(self, section_name):
        self._conf.remove_section(section_name)
        self._write()

    def remove_option(self, section=None, option=None):
        if section is None:
            section = self._section
        if option is None:
            option = self._option
        self._conf.remove_option(section,option)
        self._write()







