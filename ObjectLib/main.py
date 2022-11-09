import ast
from datetime import datetime
from matplotlib.pyplot import axis
from dataTools.dataObjects import *
from timeTools.timeObjects import *

x = DataFrameClass([[1,2,3],[4,5,6]])
y = DataFrameClass([1,2])
z = y.matrix.repeat(3,axis=1)
(r,c) = y.matrix.shape
print(r)
print(x.matrix)

print(r'----------multi----------')
print(x.T * y.T)

print(x*x)


#o = x.size_ajust(1,amend_method='col')
#x.amend_value = True
o = (x + 5 - 2.1)/2.5
print('------------')
print(x)
print(y)
print(o.subDataFrame(rstart=1))
print(o.colDataFrame(1))
print(o.colsDataFrame([0,2]))
print(o.concat(x,inplace=True))
print(o)
o.clone([8])
print(o)
o.value_init(5,5,8)
print(o)
o.continuous_value_init(5,3,4,3)
print(o)
o.random_value_init(5,5,v_max = 10, dtype=float)
print(o)
o.normal_random_value_init(3,3,10,1)
print(o)

o.append(o)
o.append(o)
print(o)
o.resize(20,5)
print(o)
o.drop(columns=o.columns[2],axis=1, inplace=True)
o.drop_row(3, inplace=True)
print(o)
print(o.reverse(axis=0,inplace=True))
print(o.rowDataFrame(1))
o = o.iloc[:,::-1]
print(o)

import timeTools.timeObjects as to
tt = to.timeTool()
tt.time = datetime.now()
print(tt.month_name)
print(tt.month_name_to_int('Aug',True))
print(tt.formatted_string_to_time('','a%s%t'))

import stringTools.stringObjects as so
astr = so.stringTool()
astr.string = '.123a5.5b0.064c123.005n1'
print(astr.string)
print(astr.find_decimal())
print(astr.find_all_decimals())
ds = astr.find_all_decimals()
print(ds[0][0])
a = '0.356'
print(a.isnumeric())
print(astr.string[3])
print(astr.find_all_floats())
print(astr.find_all_numbers())

tm = timeTool()
m = tm.time
print(tm.formatted_string())
