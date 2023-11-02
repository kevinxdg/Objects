#coding=utf-8
import imaplib
from imapclient import imap_utf7
import email
from email.header import decode_header


class MailBoxObject:
    """邮箱对象"""
    _mail_server = None
    _server_name = None
    _server_port = None
    _server_username = None
    _server_password = None
    _mail_dirs = []
    _mail_messages = None
    _mail_ids = []

    @property
    def server(self):
        return self._mail_server

    @property
    def server_name(self):
        return self._server_name

    @server_name.setter
    def server_name(self, value):
        self._server_name = value

    @property
    def server_port(self):
        return self._server_port

    @server_port.setter
    def server_port(self, value):
        self._server_port = value

    @property
    def server_username(self):
        return self._server_username

    @server_username.setter
    def server_username(self, value):
        self._server_username = value

    @property
    def server_password(self):
        return self._server_password

    @server_password.setter
    def server_password(self, value):
        self._server_password = value

    def connect_mail_server(self, servername, port, username,password):
        try:
            self._mail_server = imaplib.IMAP4_SSL(servername, port)
            self._mail_server.login(username, password)
            self._server_name = servername
            self._server_port = port
            self._server_username = username
            self._server_password = password
        except Exception as err:
            print('Failure in connection to ' + servername, err)

    def connect(self):
        self.connect_mail_server(self.server_name, self.server_port, self.server_username, self.server_password)



    @property
    def dirs(self):
        rv, folders = self._mail_server.list()
        self._mail_dirs = []
        for folder in folders:
            dirstr = imap_utf7.decode(folder)
            last_str = dirstr.split(r'"')
            self._mail_dirs.append(last_str[3])
        return self._mail_dirs

    def list_server_dirs(self):
        iDir = 0
        for folder in self.dirs:
            iDir = iDir + 1
            print('[%d] %s' %(iDir,folder))


    def find_mails_in_folder(self, folder, criteria='ALL'):
        searched = imap_utf7.encode(folder)
        typ, self._mail_messages = self._mail_server.select(searched)
        num_msgs = int(self._mail_messages[0])
        prompt = r'There are {} messages in ' + folder
        print(prompt.format(num_msgs))
        status, message_ids = self._mail_server.search(None,criteria)
        self._mail_ids = message_ids[0].split()
        print(self._mail_ids)

        for message_id in self._mail_ids:
            try:
                status, message_data = self._mail_server.fetch(self._mail_ids[0],"(RFC822)")
            except Exception as err:
                print("获取邮件失败：%s" % str(err))
            raw_email = message_data[0][1]
            email_message = email.message_from_bytes(raw_email)
            subject = decode_header(email_message["Subject"][0][0])
            sender = decode_header(email_message["From"][0][0])
            recipient = decode_header(email_message["To"][0][0])
            print(subject)






    #def mail_dirs()


#----
mo = MailBoxObject()
imap_server = 'mail.hzau.edu.cn'
imap_port = 993
username = 'gexd@mail.hzau.edu.cn'
password ='Dearxiao915'
mo.connect_mail_server(imap_server, imap_port, username, password)
mo.list_server_dirs()
mo.find_mails_in_folder(r"教学事务/环境法_2021")

