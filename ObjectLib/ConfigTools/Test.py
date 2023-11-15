#coding=utf-8

import os

from configObjects import *
co = ConfigureObject()
co.filename = r'MailProj.ini'
co.load_config()
print(co.sections)
co.section = 'Lib_Dirs'
items = co.all_items
print(items)
print(co.get_option_value(option='dir_mail_objects'))
co.set_option_value(option='Test', value='Good')
co.remove_option(option='test')

