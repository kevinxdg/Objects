#coding=utf-8

from wordObjects import *

dir_pool = r'H:\Python\Worksapce\Pools\Objects\OfficeTools'

wo = WordObject()
wo.print_hi()
print(wo.doc_path)
wo.insert_txt_file(dir_pool + r'\a.txt')
wo.insert_img(dir_pool + r'\a.jpg')
wo.save(dir_pool + r'\a.docx')
print(wo.doc.inline_shapes[0].height)
print(wo.doc.sections[0].page_width)

wco = WordConvertor()
wco.doc_to_docx(dir_pool + r'\b.doc')
wco.doc_to_pdf(dir_pool + r'\b.doc')
