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

# Variables de usuario
# Shape de máscara
capa_mascara = r'D:\ACTED\IMPACT COL - General\5_GIS\1_Spatial_Data\6_Geographic_Information\4_Cartografia_basica_IGAC\dv_Municipio\dv_Municipio.shp'
# Layer de máscara
layer_mascara = arcpy.MakeFeatureLayer_management(capa_mascara,'layer_mascara_lyr',"lower(NOM_MUNICI) LIKE 'puerto as%'")
# Carpeta de entrada
ruta_carpeta_in = r"D:\ACTED\IMPACT COL - General\5_GIS\2_Projects\2024_XXX_ECHO\ABA\COL2301_PUTUMAYO\1.DATOS\Colombia_Imagery\EarthEngineImages"
# Carpeta de salida
ruta_carpeta_out = r'D:\rtest\ras'
# Filtro por prefijo
filtro_nombre = 'Putumayo_WaterQuality_Annual_'
# Sistema de referencia de destino UTM-18N
sis_prj = 'PROJCS["WGS_1984_UTM_Zone_18N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-75.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
# Tamaño de celda para remuestreo en metros
tamano_celda = '1'
# Valor clasificar agua
valor_agua = -0.25
# Definir el índice de la banda espectral a leer
indice_banda = 11 # MNDWI




# Definir la ruta del raster de entrada



# Leer la banda espectral del raster de entrada
""" raster_desc = arcpy.Describe(raster_input)
banda_espectral = raster_desc.children[indice_banda] """

# Clasificar el raster a partir de un condicional de dos valores
arcpy.env.workspace = r'memory'

# Geoprocesamiento
arcpy.env.workspace = ruta_carpeta_in
rasterlist = arcpy.ListDatasets(f"{filtro_nombre}*", "Raster")
for n,i in enumerate(rasterlist, start=1):
    # Extraer la banda de interés
    ras_lyr = arcpy.ia.ExtractBand(i, indice_banda)
    output_raster = os.path.join('memory',f"{i[:-4].lower()}_{tamano_celda}m_prj")
    # Proyectar el raster
    arcpy.management.ProjectRaster(ras_lyr,output_raster,sis_prj,'CUBIC',tamano_celda)
    # Condicional con la calculadora raster
    raster_clasificado = arcpy.sa.Con(Raster(output_raster) > valor_agua, 1, None)
    # Almacenar el archivo
    out_filename = os.path.join(ruta_carpeta_out, f"{i[:-4].lower()}_rcon.tif")
    raster_clasificado.save(out_filename)
    
    """ outExtractByMask = arcpy.sa.ExtractByMask(output_raster, layer_mascara, 'INSIDE')
    outExtractByMask.save(out_filename) """
    print(f'Raster procesado: {n}-{i}')
    time.sleep(0.5)
print("Proceso completado")

# Final script
print("Fin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

