import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import Firefox
#-----
sys.path.append(r"H:\Python\GITProjects")
from Objects.ObjectLib.ConfigTools.configObjects import *

class CrawObject:

    _web_site = ""
    _web_directory = ""
    _web_page = ""
    __webdriver_list = ['firefox','edge', 'chrome']
    _webdriver = ""
    _driver = None

    def __init__(self):
        self._web_site = ""
        self._config = ConfigureObject()

    @property
    def web_site(self):
        return self._web_site

    @web_site.setter
    def web_site(self, value):
        self._web_site = value

    @property
    def web_directory(self):
        return self._web_directory

    @web_directory.setter
    def web_directory(self, value):
        self._web_directory = value

    @property
    def web_page(self):
        return self._web_page

    @web_page.setter
    def web_page(self, value):
        self._web_page = value

    @property
    def web_path(self):
        path_parts = [self.web_site,self.web_directory, self.web_page]
        return os.path.join(*path_parts)

    def load_config(self, file_name, section):
        return self._config.load_config_from_file(file_name, section)
    
    @property
    def webdriver(self):
        return self._webdriver
    
    @webdriver.setter
    def webdriver(self, value):
        if value in self.__webdriver_list:
           self._webdriver = value
           if value == r'firefox':
               pass
               
          
           
        
            
        
    

    


    







