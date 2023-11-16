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



