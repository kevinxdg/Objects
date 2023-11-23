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
            return make_header(decode_header(self._data.get_filename()))


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
        elif self.content_type.startswith(r'image'):
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

    def save_all_parts(self, dir_out, file_names=None):
        for iPart in range(len(self._parts)):
            part = self._parts[iPart]
            if file_names is None:
                if part.file_org_name is None:
                    file_path = dir_out + '\\part_{}'.format(iPart)
                else:
                    file_path = dir_out + '\\' + str(part.file_org_name)
            else:
                file_path = dir_out + "\\" + file_names[iPart]
            if part.content_type.startswith('text'):
                fp = open(file_path, 'w', encoding='utf-8')
                fp.write(part.content)
                fp.close()
            else:
                fp = open(file_path, 'wb')
                fp.write(part.content)
                fp.close()


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