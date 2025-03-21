# coding=utf-8
# Título: Procesar datos alfanuméricos y geográficos para indicadores JMMI en Arcpy y VStudio
# Requerimientos: ArcGIS Pro, Python 3x
# Librerías: arcpy, time, os
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2024-07-17

# Librerías
import os,arcpy
from time import strftime
arcpy.env.overwriteOutput = True

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Variables de usuario
fc = 'Admin2_UnodcOcha_01012009'
carpeta_mem = 'memory'
fc_puntos = 'adm2_pnt'
tabla_data = r'D:\data_mfs.csv'
tabla_view = 'data_mfs'
keep_field_list = ['OBJECTID','Shape','Shape_Length','Shape_Area','admin1Name_es',
                   'admin2Name_es','admin2Pcode', 'mfs_score','adm2code','classification']

# Crear centroide
arcpy.management.FeatureToPoint(fc, os.path.join(carpeta_mem,fc_puntos), 'INSIDE')

# Copiar tabla
arcpy.management.MakeTableView(tabla_data, tabla_view)

# Unir tabla
arcpy.management.JoinField(fc_puntos,'admin2pcode', tabla_view, 'adm2code')

# Borrar campos
field_list = arcpy.ListFields(fc_puntos)
for a in field_list:
    if a.name not in keep_field_list:
        print(f'Borrar: {a.name}')
        arcpy.management.DeleteField(fc_puntos, a.name)
    else:
        print(f'Mantener: {a.name}')

# Final script
print("Fin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))