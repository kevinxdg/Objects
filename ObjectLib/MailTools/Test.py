#coding=utf-8
import sys
sys.path.append(r'H:\Python\GITProjects\Objects\ObjectLib\ConfigTools')

from mailObjects import *
from configObjects import *

cf = ConfigureObject()
cf.filename = r'MailProj.ini'
cf.load_config()
cf.section = r'HZAU_Mail'

mo = MailBoxObject()
mo.server_name = cf.get_option_value(option='imap_server')
mo.server_port = cf.get_option_value(option='imap_port')
mo.server_username = cf.get_option_value(option='username')
mo.server_password = cf.get_option_value(option='password')
mo.connect()

mo.find_mails_in_folder(r'教学事务/清洁生产原理')
eo = mo.get_raw_email(1)
print(eo)
