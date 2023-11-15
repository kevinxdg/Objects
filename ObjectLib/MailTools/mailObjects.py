#coding=utf-8
import imaplib
from imapclient import imap_utf7
import email
from email.header import decode_header, make_header


class EmailObject:
    _raw_email = None
    def __init__(self, raw_email = None):
        self._raw_email =  raw_email

    @property
    def raw_email(self):
        return self._raw_email

    @property
    def sender(self):
        email_from = make_header(decode_header(self._raw_email["From"]))
        return email_from

    @property
    def receiver(self):
        email_to = make_header(decode_header(self._raw_email["To"]))
        return email_to

    @property
    def subject(self):
        subject = make_header(decode_header(self._raw_email["Subject"]))
        return subject

    def _get_att(self, msg):
        attachment_files = []

        for part in msg.walk():
            file_name = part.get_filename()  # 获取附件名称类型
            contType = part.get_content_type()

            if file_name:
                h = email.header.Header(file_name)
                dh = email.header.decode_header(h)  # 对附件名称进行解码
                filename = dh[0][0]
                if dh[0][1]:
                    filename = decode_str(str(filename, dh[0][1]))  # 将附件名称可读化
                    print(filename)
                    # filename = filename.encode("utf-8")
                data = part.get_payload(decode=True)  # 下载附件
                att_file = open('D:\\数模作业\\' + filename, 'wb')  # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
                attachment_files.append(filename)
                att_file.write(data)  # 保存附件
                att_file.close()
        return attachment_files


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
    _subjects = []

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


    def connect(self, servername=None, port=None, username=None, password=None):
        if not servername is None:
            self._server_name = servername
        if not port is None:
            self._server_port = port
        if not username is None:
            self._server_username = username
        if not password is None:
            self._server_password = password
        try:
            self._mail_server = imaplib.IMAP4_SSL(self._server_name, self._server_port)
            self._mail_server.login(self._server_username, self._server_password)

        except Exception as err:
            print('Failure in connection to ' + servername, err)


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
        prompt = r'Totally {} mails in ' + folder
        print(prompt.format(num_msgs))
        status, message_ids = self._mail_server.search(None,criteria)
        self._mail_ids = message_ids[0].split()
        return self._mail_ids

    @property
    def subjects(self):
        self._subjects = []
        for message_id in self._mail_ids:
            try:
                status, message_data = self._mail_server.fetch(message_id,"(RFC822)")
            except Exception as err:
                print("获取邮件失败：%s" % str(err))
            raw_email = message_data[0][1]
            email_message = email.message_from_bytes(raw_email)
            subject = make_header(decode_header(email_message["Subject"]))
            self._subjects.append(subject)
        return self._subjects
#-------------------------------------------------------------------
    def get_raw_email(self, email_id):
        try:
            status, data = self._mail_server.fetch(email_id, "(RFC822)")
        except Exception as err:
            print("获取邮件失败：%s" % str(err))
        if status == 'OK':
            raw_email = email.message_from_bytes(data[0][1])
        else:
            raw_email = None
        return EmailObject(raw_email)




    def _decode_str(self, s):  # 字符编码转换
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value





#----

