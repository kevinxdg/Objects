#coding=utf-8

from emailObjects import *
from Objects.ObjectLib.ConfigTools.configObjects import *
cf = ConfigureObject()
cf.filename = r'MailProj.ini'
cf.load_config()
cf.section = r'HZAU_Mail'

mo = SMTPMailBox()
mo.server_name = cf.get_option_value(option='smtp_server')
mo.server_port = cf.get_option_value(option='smtp_port')
mo.server_username = cf.get_option_value(option='username')
mo.server_password = cf.get_option_value(option='password')
mo.connect()


mo.compose()

mo.body_text_file = r'E:\教学\课件\清洁生产原理\作业\2023\答案与批复\第1次作业_回复.txt'
#mo.attach_images = [r'D:\Temp\Test.jpg']
mo.attach_files = [r'E:\教学\课件\清洁生产原理\作业\2023\答案与批复\第1次作业_参考答案.docx']
print(mo.body_text_file)
#

mo.sender = mo.server_username
mo.reciever = mo.server_username
mo.subject = 'Test'

mo.send()
print(eo)