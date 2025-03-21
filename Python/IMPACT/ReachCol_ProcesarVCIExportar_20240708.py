# coding=utf-8
# Título: Procesar indicador VCI y exportar sus cálculos en formato geográfico y alfanumérico
# Requerimientos: ArcGIS Pro, Python 3x
# Librerías: arcpy, time, os
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2024-07-08

import arcpy, os
from arcpy.sa import *
from time import strftime
arcpy.env.overwriteOutput = True

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Variables
nombre_capa = 'vci_2015'
nombre_capa_dis = 'vci_2015_dis'
nombre_capa_rs = 'vci_2015_rs_80_23'
nombre_capa_int = 'vci_2015_clc_int'
nombre_capa_vci = 'vci_2015_clc_80_23'
capa_agricola = 'sanmiguel_2_agricola'
campo_area = 'AreaHa'
#rutas
ruta_final = r'D:\ACTED\IMPACT COL - General\5_GIS\2_Projects\2024_XXX_ECHO\ABA\COL2301_PUTUMAYO\2.WORKSPACE\Indicadores\SAN_MIGUEL\VCI'

# Correr script
#Raster mascara resample

#Raster reclassify
remap_range = RemapRange([[0,10,1],[10,20,2],[20,30,3],[30,40,4],[40,50,5],[50,60,6],[60,70,7],[70,80,8],[80,90,9],[90,100,10]])
out_class = arcpy.sa.Reclassify('vegseason_vci_2015_50m_mask.tif', 'VALUE', remap_range, missing_values= "NODATA")
out_class.save(r'memory/out_class')

#Feature to polygon
arcpy.conversion.RasterToPolygon('vegseason_vci_2015_50m_mask.tif',r'memory\vci_2015_shp', 'SIMPLIFY','value')

# Dissolve
arcpy.management.Dissolve('vci_2015_class_shp',r'memory\vci_2015_class_shp_dis', 'gridcode')

# Agregar campo
arcpy.management.AddField(nombre_capa_dis,campo_area , 'DOUBLE')

# Calcular campo
arcpy.management.CalculateField(nombre_capa_dis,campo_area,"!shape.area@hectares!", 'PYTHON3')

# Copiar en carpeta
arcpy.management.CopyFeatures(nombre_capa_dis, os.path.join(ruta_final,nombre_capa_rs + '.shp'))

# Intersectar
arcpy.analysis.Intersect([nombre_capa_rs,capa_agricola],os.path.join(r'memory', nombre_capa_int))

# Listar campos
fields = arcpy.ListFields(nombre_capa_int)
for a in fields: print(a.name)

# Eliminar campos
print('started'.upper())
import time 
kf = ['OBJECTID_1','Shape','gridcode','AreaHa']
fc = nombre_capa_int
lf = arcpy.ListFields(fc)
for a in lf:
 if a.name not in kf:
  print('Drop: {x}'.format(x=a.name))
  arcpy.DeleteField_management(fc,a.name)
  time.sleep(0.5)
 else:
  print('Keep: {x}'.format(x=a.name))
print('finished'.upper())

# Calcular campos intersectados
arcpy.management.CalculateField(nombre_capa_int, campo_area,"!shape.area@hectares!", 'PYTHON3')

# Exportar como tabla
arcpy.conversion.TableToExcel(nombre_capa_int, os.path.join(ruta_final, nombre_capa_vci + '.xls'))

# Copiar shapefile final
arcpy.management.CopyFeatures(nombre_capa_int,os.path.join(ruta_final, nombre_capa_vci + '.shp'))

# Final script
print("Fin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))