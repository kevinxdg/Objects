#coding=utf-8

from wordObjects import *
wo = WordObject()
wo.print_hi()
print(wo.doc_path)
wo.insert_txt_file(r'D:\a.txt')
wo.insert_img(r'D:\a.jpg')
wo.insert_img(r'D:\三角.jpg')
wo.save(r'D:\a.docx')
print(wo.doc.inline_shapes[0].height)
print(wo.doc.sections[0].page_width)