#coding=utf-8
import imaplib
from imapclient import imap_utf7
import email
from email.header import decode_header


class MailObject:
    """邮箱对象"""
    _mail_server = None
    _mail_dirs = []
    _mail_messages = None

    def connect_mail_server(self, server, port, username,password):
        try:
            self._mail_server = imaplib.IMAP4_SSL(server, port)
            self._mail_server.login(username, password)
        except Exception as err:
            print('Failure in connection to ' + server, err)

    def list_server_dirs(self, show=True):
        rv, folders = self._mail_server.list()
        self._mail_dirs = []
        for folder in folders:
            dirstr = imap_utf7.decode(folder)
            self._mail_dirs.append(dirstr)
            if show:
                print(dirstr)

    def find_mails(self,mailbox):
        searched = imap_utf7.encode(mailbox)
        typ, self._mail_messages = self._mail_server.select(searched)
        num_msgs = int(self._mail_messages[0])
        prompt = r'There are {} messages in ' + mailbox
        print(prompt.format(num_msgs))



    #def mail_dirs()


#----
mo = MailObject()
imap_server = 'mail.hzau.edu.cn'
imap_port = 993
username = 'gexd@mail.hzau.edu.cn'
password ='Dearxiao915'
mo.connect_mail_server(imap_server,imap_port,username,password)
mo.list_server_dirs()
mo.find_mails(r"教学事务/环境法_2021")