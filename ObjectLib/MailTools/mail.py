#coding=utf-8
import imaplib
from imapclient import imap_utf7
import email
from email.header import decode_header

imap_server = 'mail.hzau.edu.cn'
imap_port = 993
username = 'gexd@mail.hzau.edu.cn'
password ='Dearxiao915'

mail = imaplib.IMAP4_SSL(imap_server,imap_port)
mail.login(username, password)

#----------------------------------
rv, folders = mail.list()
print(folders)
for folder in folders:
    str = imap_utf7.decode(folder)
    print(str)


# 对街检索邮箱名称进行编码，并检索对应主题邮件
searched = imap_utf7.encode(r"教学事务/环境法_2021")
print(searched)
mail.select(searched)
tmp, mails = mail.search(None,'SUBJECT "环境法"'.encode('utf-8'))
print(mails)
ids = mails[0].split()
print(ids)

# 获取邮件主题或内容

subjects = []
for id in ids:
    type, datas = mail.fetch(id,'(RFC822)')
    txt = datas[0][1]
    message = email.message_from_bytes(txt)
    subject = message.get('subject')
    dh = decode_header(subject)
    result = dh[0][0].decode(dh[0][1])
    subjects.append(result)

print(subjects)
print(len(subjects))
#------------
mail.close()
mail.logout()