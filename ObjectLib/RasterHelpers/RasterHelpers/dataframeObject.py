# coding=utf-8
# ======================================
# |         DataFrame 数据结构          |
# |         Version 2.1                |
# |         Date 2021-12-28            |
# ======================================
import numpy as np
import pandas as pd
class DataFrameClass(pd.DataFrame):
   #-----------Basic properties------------------
   @property
   def matrix(self):
      return np.mat(self.values)

   @property
   def dataframe(self):
      return pd.DataFrame(self.values,columns=self.columns,index=self.index)

   #-----------Data Operation---------------------

   def __add__(self, other):
      tmp = np.mat(other)
      if tmp.shape[0] == 1:
         tmp = tmp.repeat(self.shape[0], axis=1)
      if tmp.shape[1] == 1:
         tmp = tmp.repeat(self.shape[1], axis=0)
      result = np.add(self.matrix, tmp)
      return DataFrameClass(result, columns=self.columns, index=self.index)

   def __sub__(self, other):
      tmp = np.mat(other)
      if tmp.shape[0] == 1:
         tmp = tmp.repeat(self.shape[0], axis=1)
      if tmp.shape[1] == 1:
         tmp = tmp.repeat(self.shape[1], axis=0)
      result = np.subtract(self.matrix, tmp)
      return DataFrameClass(result, columns=self.columns, index=self.index)

   def __mul__(self, other):
      tmp = np.mat(other)
      if tmp.shape[0] == 1:
         tmp = tmp.repeat(self.shape[0], axis=0)
      if tmp.shape[1] == 1:
         tmp = tmp.repeat(self.shape[1], axis=1)
      result = np.multiply(self.matrix, tmp)
      return DataFrameClass(result, columns=self.columns, index=self.index)

   def __truediv__(self, other):
      tmp = np.mat(other)
      if tmp.shape[0] == 1:
         tmp = tmp.repeat(self.shape[0], axis=1)
      if tmp.shape[1] == 1:
         tmp = tmp.repeat(self.shape[1], axis=0)
      result = np.divide(self.matrix, tmp)
      return DataFrameClass(result, columns=self.columns, index=self.index)

   def copy(self,deep=True):
      if deep:
         tmp = pd.DataFrame.copy(self,deep)
         return DataFrameClass(tmp.values, columns=tmp.columns, index=tmp.index)
      else:
         return self

   def duplicate(self,times,axis=0):
      dflist = list([])
      for i in range(times):
         tmpDF = self.copy()
         dflist.append(tmpDF)
      df = pd.concat(dflist,axis=axis)
      return DataFrameClass(df.values,columns=df.columns,index=df.index)

   def subDataFrame(self,rstart,cstart,rend=-1,cend=-1):
      if rend==-1:
         rend = self.shape[0] - 1
      if cend==-1:
         cend = self.shape[1] - 1
      values = self.matrix[rstart:rend+1,cstart:cend+1]
      names = list(self.columns[cstart:cend+1])
      indexes = list(self.index[rstart:rend+1])
      return DataFrameClass(data=values,columns=names, index=indexes)

   def colDataFrame(self, cindex, rstart = 0, rend = -1):
      return self.subDataFrame(rstart=rstart, cstart=cindex, rend = rend, cend=cindex)

   def colsDataFrame(self, cindexes, rstart = 0, rend = -1):
      tmp = DataFrameClass()
      for i in cindexes:
         sdf = self.colDataFrame(rstart=rstart, cindex=i, rend = rend)
         tmp = tmp.concat(sdf)
      return tmp

   def rowDataFrame(self, rindex, cstart = 0, cend = -1):
      return self.subDataFrame(rstart=rindex, cstart=cstart, rend=rindex, cend=cend)

   def rowsDataFrame(self, rindexes, cstart = 0, cend = -1):
      tmp = DataFrameClass()
      for i in rindexes:
         sdf = self.rowDataFrame(rindex=i, cstart=cstart, cend=cend)
         tmp = tmp.append(sdf)
      return tmp

   def rows(self,index):
      return DataFrameClass(self.iloc[index,:])

   def cols(self, columns):
      return DataFrameClass(self.iloc[:,columns])

   def concat(self,sourceDFC, axis=1):
      tmp = pd.concat([self.dataframe,sourceDFC.dataframe], axis=axis)
      self.__init__(tmp)
      return self

   def clone(self,sourceDFC):
      if isinstance(sourceDFC,np.matrix):
         self.__init__(sourceDFC)
      elif isinstance(sourceDFC,pd.DataFrame) or isinstance(sourceDFC,DataFrameClass):
         self.__init__(sourceDFC.values,index=sourceDFC.index,columns=sourceDFC.columns)
      else:
         self.__init__(sourceDFC)
      return self

   def reInit(self,rows,cols,initValue=0,columns=None,index=None):
      tmp = []
      for i in range(rows):
         tmp.append([initValue] * cols)
      self.__init__(tmp, columns=columns, index=index)

   def append(self,df):
      self.concat(df,axis=0)
      return self

   def reverse(self,axis=0):
      tmp = self.copy()
      maxrow = tmp.shape[0]
      maxcol = tmp.shape[1]
      if axis==0:
         for i in range(maxrow):
            tmp = tmp.drop(index=self.index[maxrow-i-1])
            tmp = tmp.append(self.rows([maxrow-i-1]))
         self.__init__(tmp)
         return self
      else:
         for i in range(maxcol):
            tmp = DataFrameClass(tmp.drop(axis=1,columns=self.columns[maxcol-i-1]))
            tmp.concat(self.cols([maxcol-i-1]))
         self.__init__(tmp)
         return self
   #--------------Stat--------------------------------








