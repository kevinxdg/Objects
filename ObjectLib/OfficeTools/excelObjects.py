#coding=utf-8
import openpyxl as xl
from Objects.ObjectLib.dataTools.dataObjects import DataFrameClass



class Sheet:
    def __init__(self):
        self._data = DataFrameClass()
        # 自定义类属性 book 用以存放 excel 数据表
        self._sheetname = ""


class Book:
    pass

class ExcelObjects:
    pass
