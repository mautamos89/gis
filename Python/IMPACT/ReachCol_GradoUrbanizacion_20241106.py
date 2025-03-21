# coding=utf-8
# Título: Procesar el nivel de urbanización con datos poblacionales de Kontur.
# Requerimientos: ArcGIS Pro, Python 3x
# Librerías: arcpy, time, os
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2024-11-06

import arcpy, time, os
from arcpy import sa
from time import strftime

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Variables de usuario
carpeta_memoria = r'memory' # Carpeta de trabajo

# Capas de entrada y salida
capa_poblacion = 'Kontur_Population_Barbacoas'
capa_urbanizacion = 'grado_urbanizacion'

# Lista consultas SQL y rangos
lista_sql_rangos = ["population < 50", "population >= 50 and population < 300", "population >= 300 and population < 1500", "population >= 1500"]
# Rangos y valores [Agrupaciones rurales de muy baja densidad, Agrupaciones rurales de baja densidad, Agrupaciones urbanas semidensas, Centros urbanos]

# Agrupación regional
celdas_region = "EIGHT"

# Parámetros de entorno
arcpy.env.overwriteOutput = True

# Iniciar procesamiento iterativo
for consulta in lista_sql_rangos:

    # Imprimir el elemento actual
    print(f"\nCláusula SQL aplicada: {consulta}")

    # Realizar nueva capa por condición
    arcpy.management.MakeFeatureLayer(capa_poblacion,'kontur_data', consulta)
    print('\nEntidades seleccionadas!'.title())

    # Convertir Kontur datos a raster
    arcpy.conversion.FeatureToRaster('kontur_data', 'population', os.path.join(carpeta_memoria,'kontur_pop'),10)
    print('Datos convertidos a raster!'.title())

    # Agrupación regional
    out_raster = arcpy.sa.RegionGroup(os.path.join(carpeta_memoria,'kontur_pop'), celdas_region, "CROSS","ADD_LINK",excluded_value=None)
    out_raster.save(os.path.join(carpeta_memoria,'kontur_pop_reg'))
    print('Agrupación regional realizada!'.title())

    # Convertir región a vector
    arcpy.conversion.RasterToPolygon(os.path.join(carpeta_memoria,'kontur_pop_reg'),os.path.join(carpeta_memoria,'vec_region'),'SIMPLIFY',create_multipart_features= 'MULTIPLE_OUTER_PART')
    print('Datos convertidos a vector!'.title())

    # Selección espacial
    arcpy.analysis.SpatialJoin(capa_poblacion, 'vec_region', os.path.join(carpeta_memoria, 'kontur_data_sjoin'), 'JOIN_ONE_TO_ONE', 'KEEP_COMMON', match_option='HAVE_THEIR_CENTER_IN')
    print('Selección espacial de región y datos Kontur realizada!'.title())

    # Sumar población de la región
    arcpy.management.Dissolve('kontur_data_sjoin',os.path.join(carpeta_memoria, f'kontur_data_dis_{consulta}'.replace('<','').replace('>','').replace('=','').replace(' ','_')), dissolve_field='gridcode', statistics_fields=[['population','SUM']], multi_part=False)
    print('Suma del dato de población realizado!'.title())

    # Limpiar la selección
    arcpy.management.SelectLayerByAttribute(capa_poblacion, 'CLEAR_SELECTION')

# Procesamiento final de capas
arcpy.env.workspace = carpeta_memoria

# Listar y unir capas de interés
lista_merge = arcpy.ListFeatureClasses('kontur_data_dis*')
print(f"Objetos a unir: {lista_merge}")
arcpy.Merge_management(lista_merge,os.path.join(carpeta_memoria,capa_urbanizacion))
print('Unión de capas de interés realizado!'.title())

# Asignar campo de nivel de urbanización y score
arcpy.AddField_management(capa_urbanizacion,'nivel','TEXT',field_length=50)
arcpy.AddField_management(capa_urbanizacion,'score','SHORT')
print('Campos creados correctamente!'.title())

# Ingresar valor de grado de urbanización
with arcpy.da.UpdateCursor(capa_urbanizacion, ['SUM_population', 'nivel', 'score']) as cursor:
    for row in cursor:
        if row[0] < 50:
            row[1] = 'Agrupaciones rurales de muy baja densidad'
            row[2] = 3
        elif row[0] < 300:
            row[1] = 'Agrupaciones rurales de baja densidad'
            row[2] = 3
        elif row[0] < 1500:
            row[1] = 'Agrupaciones urbanas semidensas'
            row[2] = 2
        else:
            row[1] = 'Centros urbanos'
            row[2] = 1
        cursor.updateRow(row) # Impactar cambios en la tabla
print('Valores de grado de urbanización y puntaje calculados correctamente!'.title())

# Limpiar TOC del proyecto
aprx = arcpy.mp.ArcGISProject("CURRENT")
for m in aprx.listMaps():
    print(f"Map: {m.name}")
    for lyr in m.listLayers():
        if lyr.isBasemapLayer == False and lyr.name != capa_urbanizacion and lyr.name != capa_poblacion:
            print(f"Eliminando capa: {lyr.name}")
            m.removeLayer(lyr)
print('Limpieza de proyecto terminada.'.title())

# Final script
print("\nFin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))