# coding=utf-8
# Título: Procesar datos alfanuméricos y geográficos para rutas CALP con Arcpy y VStudio Code
# Requerimientos: ArcGIS Pro, Python 3x
# Librerías: arcpy, time, os
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2024-07-29

# Librerías
import os,arcpy
from time import strftime
arcpy.env.overwriteOutput = True

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Variables de usuario
capa_rutas_identificadas = 'OSM_vias_principales_mapa_base_Ecuador-DPI'
capa_admin2 = 'peru_adm2_dis'
campo_admin1 = 'NAME_1'
campo_admin2 = 'NAME_2'
carpeta_memoria = 'memory'
archivo_salida = 'peru_ruta'
campo_id_ruta = 'IdRuta'
campo_longitud_km = 'LonKm'
carpeta_destino = r'D:\ACTED\IMPACT COL - General\5_GIS\2_Projects\2024_XXX_ECHO\REG2401-CALP\1. DATA\SHP\RUTAS MAPEO'

#Procesamiento geográfico CALP
# Intersectar rutas con admin2
arcpy.analysis.Intersect([capa_rutas_identificadas, capa_admin2], os.path.join(carpeta_memoria, archivo_salida + '_int'))
# Calcular campo IdRuta (Selección interactiva con usuario y tramo de ruta)
arcpy.management.CalculateField(archivo_salida + '_int',campo_id_ruta,"""'A1'""", 'PYTHON3')
# Disolver a nivel administrativo por tramo de ruta
arcpy.management.Dissolve(archivo_salida + '_int', os.path.join(carpeta_memoria, archivo_salida + '_dis'), [campo_id_ruta, campo_admin1, campo_admin2])
# Agregar campo longitud en kilómetros
arcpy.management.AddField(archivo_salida + '_dis', campo_longitud_km, 'DOUBLE')
# Calcular longitud en kilómetros
arcpy.management.CalculateField(archivo_salida + '_dis',campo_longitud_km,"!shape!.getLength('geodesic','kilometers')")
# Copiar archivo a carpeta destino
arcpy.management.CopyFeatures(archivo_salida + '_dis', os.path.join(carpeta_destino, archivo_salida + strftime("%Y%m%d") + '.shp'))

# Final script
print("Fin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))