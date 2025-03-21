# coding=utf-8
# Título: Procesar archivo raster con remuestro y máscara a partir de polígono con Arcpy y VStudio
# Requerimientos: ArcGIS Pro, Python 3x
# Librerías: arcpy, time, os
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2024-06-26

import arcpy, os, time
from arcpy import env
from arcpy.sa import *
from time import strftime
arcpy.env.overwriteOutput = True

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Script # Calidad agua GIS

arcpy.conversion.RasterToPolygon('putumayo_waterquality_annual_2022_rcon.tif',r'memory\poly_2022', 'SIMPLIFY')
sis_prj = 'PROJCS["WGS_1984_UTM_Zone_18N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-75.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
arcpy.management.Project('poly_2022',r'memory\poly_2022_prj',sis_prj)
arcpy.cartography.AggregatePolygons('poly_2022_prj',r'memory\poly_2022_agr',20,10000,1000000)
#Union sin gaps
#Dissolve
#Multipart to singlepart
#Add & Calculate field AreaM2
#Sort descending AreaM2
#Select by attributes -> [SQL] OBJECTID = 1
#Smooth polygon [Opcional]
#Project raster
#Extract by mask [In-> Smooth + Project]

# Final script
print("Fin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))