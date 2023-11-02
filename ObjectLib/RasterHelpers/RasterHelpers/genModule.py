#coding=utf-8
import arcpy as arcpy
import numpy as np
arcpy.CheckOutExtension('Spatial')
arcpy.CheckOutExtension("ImageAnalyst")  # 检查许可
arcpy.env.overwriteOutput = True
