#coding=utf-8
import imaplib
import os.path
import smtplib
from imapclient import imap_utf7
import email
from email.header import decode_header, make_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.message import MIMEMessage


class EmailMessagePart:
    def __init__(self,message_data=None):
        self._data = message_data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def file_org_name(self):
        if self._data is None:
            return None
        else:
            fname = self._data.get_filename()
            if fname is None:
                return None
            return str(make_header(decode_header(fname)))

    @property
    def content_string(self):
        return self._data['Content-Disposition']

    @property
    def content_type(self):
        if self._data is None:
            return None
        else:
            return self._data.get_content_type()

    @property
    def main_type(self):
        if self._data is None:
            return None
        else:
            return self._data.get_content_maintype()

    @property
    def charset(self):
        cset = self._data.get_content_charset()
        if cset is None:
            cset = self._data.get_charset()
        if not cset:
            cset = 'utf-8'
        return cset

    @property
    def content(self):
        if not hasattr(self,'_content'):
            self._content = None
        if self._data  is None:
            self._content = None

        elif self.content_type.startswith(r'text'):
            self._content = self._data.get_payload(decode=True).decode(self.charset)
        else:
            self._content = self._data.get_payload(decode=True)

        return self._content


    @property
    def sub_parts(self):
        sub_parts = []
        if self._data is None:
            return sub_parts
        elif not self._data.is_multipart():
            return sub_parts
        else:
            for sub_part in self._data.walk():
                sub_parts.append(EmailMessagePart(sub_part))
        return sub_parts

    def set_content_to_text(self,message_text,encoding='utf-8'):
        self._data = MIMEText(message_text,'plain',encoding)

    def set_content_to_html(self, message_text,encoding='utf-8'):
        self._data = MIMEText(message_text,'html',encoding)

    def set_content_to_attach_file(self, file_path):
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            self._data = MIMEApplication(f.read(),Name=file_name)
        self._data['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
        self._data["Content-Type"] = 'application/octet-stream'

    def set_content_to_img_file(self,file_path):
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            self._data = MIMEImage(f.read(), _subtype='octet-stream')
        self._data['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)

    def save_to_file(self, dir_out, file_name=None):
        if file_name is None:
            file_name = self.file_org_name
        file_path = dir_out + "\\" + file_name
        if self._data.is_multipart():
            sub_parts = self.sub_parts
            for isub in range(len(sub_parts)):
                sub_part = sub_parts[isub]
                sub_file_name = "sub_{}_".format(isub) + file_name
                if sub_part.content_type.startswith(r'image'):
                    sub_part.save_to_file(dir_out,sub_file_name)
        elif self.content_type.startswith('text'):
            fp = open(file_path, 'w', encoding='utf-8')
            fp.write(self.content)
            fp.close()
        else:
            fp = open(file_path, 'wb')
            fp.write(self.content)
            fp.close()

class EmailObject:

    def __init__(self, email_data=None):
        if email_data is None:
            self._raw_email = MIMEMultipart()
        else:
            self._raw_email = email_data
            #self._parse()

    @property
    def data(self):
        return self._raw_email

    @data.setter
    def data(self, value):
        if not value is None:
            self.__init__(value)

    @property
    def parts(self):
        self._parts = []
        for part in self._raw_email.walk():
            self._parts.append(EmailMessagePart(part))
        return self._parts

    @property
    def sender(self):
        return make_header(decode_header(self._raw_email["From"]))

    @sender.setter
    def sender(self, value):
        self._raw_email['From'] =  value

    @property
    def receiver(self):
        return make_header(decode_header(self._raw_email["To"]))

    @receiver.setter
    def receiver(self, value):
        self._raw_email['To'] = value

    @property
    def subject(self):
        return make_header(decode_header(self._raw_email["Subject"]))

    @subject.setter
    def subject(self, value):
        self._raw_email['Subject'] = value

    def save_body_text(self, dir_out, file_name, part=None):
        if part is None:
            for t_part in self.parts:
                if t_part.content_type == r'text/plain':
                    part = t_part
                    break
            part.save_to_file(dir_out, file_name)


    def save_all_parts(self, dir_out, file_names=None,html_on=False):
        for iPart in range(len(self.parts)):
            part = self.parts[iPart]
            if file_names is None:
                if part.file_org_name is None:
                    if part.content_type == r'text/plain':
                        suffix = '.txt'
                    elif part.content_type == r'text/html':
                        suffix = '.html'
                    elif part.content_type.startswith('image'):
                        suffix = '.png'
                    else:
                        suffix = '.png'
                    file_name = 'part_{}'.format(iPart) + suffix
                else:
                    file_name = str(part.file_org_name)
            else:
                file_name = file_names[iPart]
            if part.content_type != r'text/html' or html_on:
                part.save_to_file(dir_out,file_name)





class MailBoxBase:

    def __init__(self):
        self._mail_server = None
        self._server_name = None
        self._server_port = None
        self._server_username = None
        self._server_password = None
        self._mail_dirs = []
        self._mail_messages = None
        self._mail_ids = []
        self._subjects = []

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


class MailBoxObject(MailBoxBase):
    pass
