#coding=utf-8
from docx import Document

class WordObject:

    def __init__(self):
        self._doc_path = None
        self._doc = Document()

    def print_hi(self):
        print(type(self._doc))

    @property
    def doc(self):
        return self._doc


    def load_doc(self, doc_path):
        self._doc_path = doc_path
        self._doc = Document(doc_path)

    @property
    def doc_path(self):
        return self._doc_path

    @doc_path.setter
    def doc_path(self, value):
        self._doc_path = value
        self.load_doc(self._doc_path)

    def insert_txt_file(self, txt_path):
        with open(txt_path, 'r') as file:
            txt_lines = file.readlines()
        for txt_line in txt_lines:
            self._doc.add_paragraph(txt_line)

    def insert_img(self, img_path):
        section = self._doc.add_section()
        img = self._doc.add_picture(img_path)
        page_width = section.page_width - section.left_margin -  section.right_margin
        page_height = section.page_height - section.top_margin - section.bottom_margin
        rw = img.width / page_width
        rh = img.height / page_height
        print(rw)
        print(rh)
        if (rw < 1) and (rh < 1):
            pass
        elif rw >= rh:
            img.width = int(img.width / rw)
            img.height = int(img.height / rw)
        else:
            img.width = int(img.width / rh)
            img.height = int(img.height / rh)
        self._doc.add_page_break()



    def save(self, file_path = None):
        if file_path is None:
            file_path = self._doc_path
        self._doc.save(file_path)
        self._doc_path = file_path



