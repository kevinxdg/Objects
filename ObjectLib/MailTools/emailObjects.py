#coding=utf-8
import imaplib
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
            return self._data.get_filename()

    @property
    def file_new_name(self):
        if not hasattr(self, "_file_new_name"):
            self._file_new_name = self.file_org_name
        return self._file_new_name

    @file_new_name.setter
    def file_new_name(self, value):
        self._file_new_name = value

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