#coding=utf-8
from datetime import datetime
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
from Objects.ObjectLib.OfficeTools.wordObjects_V2 import *


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
        file_paths = []
        if file_name is None:
            file_name = self.file_org_name
        file_path = os.path.join(dir_out, file_name)
        if self._data.is_multipart():
            sub_parts = self.sub_parts
            for isub in range(len(sub_parts)):
                sub_part = sub_parts[isub]
                sub_file_name = "sub_{}_".format(isub) + file_name
                if sub_part.content_type.startswith(r'image'):
                    sub_file_paths = sub_part.save_to_file(dir_out, sub_file_name)
                    file_paths.extend(sub_file_paths)
        elif self.content_type.startswith('text'):
            fp = open(file_path, 'w', encoding='utf-8')
            fp.write(self.content)
            fp.close()
            file_paths.append(file_path)
        else:
            fp = open(file_path, 'wb')
            fp.write(self.content)
            fp.close()
            file_paths.append(file_path)
        return file_paths

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
        return str(make_header(decode_header(self._raw_email["From"])))

    @sender.setter
    def sender(self, value):
        self._raw_email['From'] =  value

    @property
    def receiver(self):
        return str(make_header(decode_header(self._raw_email["To"])))

    @receiver.setter
    def receiver(self, value):
        self._raw_email['To'] = value

    @property
    def subject(self):
        return str(make_header(decode_header(self._raw_email["Subject"])))

    @subject.setter
    def subject(self, value):
        self._raw_email['Subject'] = value

    @property
    def date(self):
        dayt = self._raw_email['Date'][5:25].replace(' ','')
        result = datetime.strptime(dayt, "%d%b%Y%H:%M:%S")
        return result


    def save_body_text(self, dir_out, file_name, part=None):
        if part is None:
            for t_part in self.parts:
                if t_part.content_type == r'text/plain':
                    part = t_part
                    break
            part.save_to_file(dir_out, file_name)


    def save_all_parts(self, dir_out, file_names=None,html_on=False):
        file_paths = []
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
                    file_name = file_name.replace(r'：','')
                else:
                    file_name = str(part.file_org_name).replace(r'：','')
            else:
                file_name = file_names[iPart].replace(r'：','')
            if part.content_type != r'text/html' or html_on:
                part_file_paths = part.save_to_file(dir_out,file_name)
                file_paths.extend(part_file_paths)
        return file_paths

    def save_email(self, dir_pool, dir_result, file_name, html_on=False, overwrite=False):
        file_paths = self.save_all_parts(dir_pool, html_on=html_on)
        file_result = os.path.join(dir_result, file_name)
        if os.path.exists(file_result) and not overwrite:
            print('邮件文件已经存在，且不允许覆盖, {}'.format(file_result))
        else:
            doc = WordObject()
            doc_covertor = WordConvertor()
            for file in file_paths:
                ext = os.path.splitext(file)[1]
                if ext == '.txt':
                    doc.insert_txt_file(file)
            doc.save(file_result)

            for file in file_paths:
                root_path, file_exe = file.rsplit('.', 1)
                if file_exe == 'doc':
                    new_path = doc_covertor.doc_to_docx(file)
                    doc.insert_docx(new_path)

                elif file_exe == 'docx':
                    doc.insert_docx(file)

                elif file_exe in ['jpg', 'bmp', 'jpge', 'png']:
                    doc.insert_img(file)
                elif file_exe == 'pdf':
                    new_path = doc_covertor.pdf_to_doc(file)
                    doc.insert_docx(new_path)
                # doc.delete_blank_pages()
            doc.save(file_result)
            print('作业文档已生成，{}'.format(file_result))


    def insert_body_text(self, text, text_type='plain'):
        msg_part = MIMEText(text, text_type, 'utf-8')
        self._raw_email.attach(msg_part)


    def insert_body_text_file(self, file_path, file_type='plain'):
        with open(file_path,'r',encoding='utf-8') as f:
            msg_part = MIMEText(f.read(),file_type,'utf-8')
            f.close()
        self._raw_email.attach(msg_part)

    def insert_attach_files(self, file_paths):
        for file in file_paths:
            f = open(file,'rb')
            part = MIMEApplication(f.read(), Name=os.path.basename(file))
            part['Content_Type'] = 'application/octet-stream'
            part["Content-Disposition"] = 'attachment; filename="{}"'.format(os.path.basename(file))
            self._raw_email.attach(part)
            f.close()

    def insert_attach_images(self, file_paths):
        for file in file_paths:
            f = open(file,'rb')
            part = MIMEImage(f.read(), _subtype='octet-stream')
            part["Content-Disposition"] = 'attachment; filename="{}"'.format(os.path.basename(file))
            self._raw_email.attach(part)
            f.close()

class MailBoxBase:

    def __init__(self):
        self._mail_server = None
        self._server_name = None
        self._server_port = None
        self._server_username = None
        self._server_password = None

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
        pass


class IMAPMailBox(MailBoxBase):

    def __init__(self):
        super().__init__()
        self._mail_dirs = []
        self._mail_ids = []
        self._subjects = []

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

    def find_mails_in_folder(self, folder, criteria='ALL'):
        searched = imap_utf7.encode(folder)
        typ, self._mail_messages = self._mail_server.select(searched)
        num_msgs = int(self._mail_messages[0])
        prompt = r'Totally {} mails in ' + folder
        print(prompt.format(num_msgs))
        status, message_ids = self._mail_server.search(None,criteria)
        self._mail_ids = message_ids[0].split()
        return self._mail_ids

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

class SMTPMailBox(MailBoxBase):

    def __init__(self):
        super().__init__()
        self._msg = EmailObject()
        self._body_text_file = ''
        self._body_text = ''
        self._body_imgs = []
        self._attachfiles = []
        self._attach_imgs = []

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
            self._mail_server = smtplib.SMTP_SSL(self._server_name, self._server_port)
            self._mail_server.login(self._server_username, self._server_password)

        except Exception as err:
            print('Failure in connection to ' + servername, err)

    @property
    def sender(self):
        return str(self._msg.sender)

    @sender.setter
    def sender(self, value):
        self._msg.sender = value

    @property
    def reciever(self):
        return str(self._msg.receiver)

    @reciever.setter
    def reciever(self, value):
        self._msg.receiver = value

    @property
    def subject(self):
        return self._msg.subject
    @subject.setter
    def subject(self, value):
        self._msg.subject = value

    @property
    def body_text_file(self):
        return self._body_text_file

    @body_text_file.setter
    def body_text_file(self, value):
        self._body_text_file = value

    @property
    def body_text(self):
        return self._body_text

    @body_text.setter
    def body_text(self, value):
        self._body_text = value

    @property
    def attach_images(self):
        return self._attach_imgs

    @attach_images.setter
    def attach_images(self, value):
        self._attach_imgs = value

    @property
    def attach_files(self):
        return self._attachfiles

    @attach_files.setter
    def attach_files(self, value):
        self._attachfiles = value

    def create_new_mail(self):
        self._msg = EmailObject()
        self._body_text_file = ''
        self._body_text = ''
        self._body_imgs = []
        self._attachfiles = []
        self._attach_imgs = []

    def compose(self):
        self.create_new_mail()



    def send(self):
        if self._body_text != '':
            self._msg.insert_body_text(self._body_text, text_type='plain')

        if self._body_text_file != '':
            self._msg.insert_body_text_file(self._body_text_file, file_type='plain')

        self._msg.insert_attach_files(self.attach_files)
        self._msg.insert_attach_images(self.attach_images)
        try:
            self._mail_server.sendmail(self.sender, self.reciever,self._msg.data.as_string())
            print('邮件发送成功! From [%s] To [%s]'%(self.sender, self.reciever))
            return True
        except smtplib.SMTPException as err:
            print('邮件发送失败：{}'.format(err))
            return False







