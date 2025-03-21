# coding=utf-8
# Título: Procesar la zonificación multicriterio de sensibilidad y acceso con capas de entrada y puntaje score.
# Requerimientos: ArcGIS Pro, Python 3x
# Librerías: arcpy, time, os
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2024-11-08

import arcpy, time, os
#from arcpy import sa
from time import strftime
# Parámetros de entorno
arcpy.env.overwriteOutput = True

################
# SENSIBILIDAD #
################

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
print('\ncalculando sensibilidad!'.upper())

# Variables de usuario
carpeta_memoria = r'memory' # Carpeta de trabajo
# Capas de entrada y salida
capa_union = 'suce_union'
capa_disolver = 'suce_dis'
capa_final = 'sensibilidad_amc'
# Campo de interés
campo_puntaje = 'sensi_score'

# Unión de capas
arcpy.analysis.Union(['mineria_amc','densidad_coca','tasa_evento_violento','deforestacion','dapre_map'],os.path.join(carpeta_memoria, capa_union),gaps=True)
print('Unión de capas realizada!'.title())

# Llave única de coordenadas
arcpy.management.CalculateField(capa_union,'llave', "str(!shape!.truecentroid.x) + '-' + str(!shape!.truecentroid.y)", 'PYTHON3','', 'TEXT')
print('Llave única de polígonos generada!'.title())

# Calcular el puntaje en nuevo campo
fields = arcpy.ListFields(capa_union) # Identificar campos de la capa
score_fields = [field.name for field in fields if field.name.startswith('score')] # Obtener la lista de campos que comienzan con "score"
expression = ' + '.join([f'!{field}!' for field in score_fields]) # Construir la expresión para la suma
arcpy.management.CalculateField(capa_union, campo_puntaje, expression, 'PYTHON3', '', 'SHORT') # Calcular campo con suma de campos de interés
print('Puntaje calculado correctamente!'.title())

# Disolver y sumar
arcpy.management.Dissolve(capa_union, os.path.join(carpeta_memoria, capa_disolver), dissolve_field='llave', statistics_fields=[[campo_puntaje, 'SUM']], multi_part=False)
print('Disolución de capas por llave realizada!'.title())

# Disolver por categoría y dar puntaje
# Asignar campo de nivel de urbanización y score
arcpy.AddField_management(capa_disolver,'nivel','TEXT',field_length=50)
arcpy.AddField_management(capa_disolver,'score','SHORT')
print('Campos creados correctamente!'.title())

# Ingresar valor de grado de urbanización
with arcpy.da.UpdateCursor(capa_disolver, [f'SUM_{campo_puntaje}', 'nivel', 'score']) as cursor:
    for row in cursor:
        if row[0] == 0:
            row[1] = 'Áreas no sensibles'
            row[2] = 0
        elif row[0] < 5:
            row[1] = 'Sensibilidad baja'
            row[2] = 1
        elif row[0] < 10:
            row[1] = 'Sensibilidad moderada'
            row[2] = 2
        else:
            row[1] = 'Sensibilidad alta'
            row[2] = 3
        cursor.updateRow(row) # Impactar cambios en la tabla
print('Valores de nivel de sensibilidad calculados correctamente!'.title())

# Disolver por nivel de sensibilidad
arcpy.management.Dissolve(capa_disolver, os.path.join(carpeta_memoria, capa_disolver + "_2"), dissolve_field=['nivel','score'], multi_part=False)
print('Disolución de capas por nivel de sensibilidad realizada!'.title())

# Calcular área en hectáreas
arcpy.AddField_management(capa_disolver + "_2",'AreaHa','DOUBLE')
arcpy.management.CalculateField(capa_disolver + "_2" ,'AreaHa',"!shape!.getArea('GEODESIC', 'HECTARES')", 'PYTHON3')
print('Área en hectárea calculada correctamente!'.title())

# Eliminar por UMC
arcpy.management.SelectLayerByAttribute(capa_disolver + "_2", 'NEW_SELECTION',"AreaHa < 1")
arcpy.management.Eliminate(capa_disolver + "_2", os.path.join(carpeta_memoria, capa_final), 'AREA')
arcpy.management.CalculateField(capa_final,'AreaHa',"!shape!.getArea('GEODESIC', 'HECTARES')", 'PYTHON3')
arcpy.management.SelectLayerByAttribute(capa_disolver + "_2", 'CLEAR_SELECTION') # Limpiar la selección
print('Eliminar polígonos por Unidad Mínima Cartografiable realizado!'.title())

# Final script
print("\nFin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

##########
# ACCESO #
##########

import arcpy, time, os
#from arcpy import sa
from time import strftime
# Parámetros de entorno
arcpy.env.overwriteOutput = True

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
print('\ncalculando acceso!'.upper())

# Variables de usuario
carpeta_memoria = r'memory' # Carpeta de trabajo
# Capas de entrada y salida
capa_union = 'acce_union'
capa_disolver = 'acce_dis'
capa_final = 'acceso_amc'
# Campo de interés
campo_puntaje = 'acce_score'

# Unión de capas
arcpy.analysis.Union(['poblacion_urbanizacion','cuerpo_de_agua','via'],os.path.join(carpeta_memoria, capa_union),gaps=True)
print('Unión de capas realizada!'.title())

# Llave única de coordenadas
arcpy.management.CalculateField(capa_union,'llave', "str(!shape!.truecentroid.x) + '-' + str(!shape!.truecentroid.y)", 'PYTHON3','', 'TEXT')
print('Llave única de polígonos generada!'.title())

# Calcular el puntaje en nuevo campo
fields = arcpy.ListFields(capa_union) # Identificar campos de la capa
score_fields = [field.name for field in fields if field.name.startswith('score')] # Obtener la lista de campos que comienzan con "score"
expression = ' + '.join([f'!{field}!' for field in score_fields]) # Construir la expresión para la suma
arcpy.management.CalculateField(capa_union, campo_puntaje, expression, 'PYTHON3', '', 'SHORT') # Calcular campo con suma de campos de interés
print('Puntaje calculado correctamente!'.title())

# Disolver y sumar
arcpy.management.Dissolve(capa_union, os.path.join(carpeta_memoria, capa_disolver), dissolve_field='llave', statistics_fields=[[campo_puntaje, 'SUM']], multi_part=False)
print('Disolución de capas por llave realizada!'.title())

# Disolver por categoría y dar puntaje
# Asignar campo de nivel de urbanización y score
arcpy.AddField_management(capa_disolver,'nivel','TEXT',field_length=50)
arcpy.AddField_management(capa_disolver,'score','SHORT')
print('Campos creados correctamente!'.title())

# Ingresar valor de grado de urbanización
with arcpy.da.UpdateCursor(capa_disolver, [f'SUM_{campo_puntaje}', 'nivel', 'score']) as cursor:
    for row in cursor:
        if row[0] == 10:
            row[1] = 'Áreas sin acceso'
            row[2] = 4
        elif row[0] <= 9 and row[0] > 6:
            row[1] = 'Acceso muy restringido'
            row[2] = 3
        elif row[0] <= 6 and row[0] > 3:
            row[1] = 'Acceso restringido'
            row[2] = 2
        else:
            row[1] = 'Acceso sin restricción'
            row[2] = 1
        cursor.updateRow(row) # Impactar cambios en la tabla
print('Valores de nivel de acceso calculados correctamente!'.title())

# Disolver por nivel de acceso
arcpy.management.Dissolve(capa_disolver, os.path.join(carpeta_memoria, capa_disolver + "_2"), dissolve_field=['nivel','score'], multi_part=False)
print('Disolución de capas por nivel de acceso realizada!'.title())

# Calcular área en hectáreas
arcpy.AddField_management(capa_disolver + "_2",'AreaHa','DOUBLE')
arcpy.management.CalculateField(capa_disolver + "_2" ,'AreaHa',"!shape!.getArea('GEODESIC', 'HECTARES')", 'PYTHON3')
print('Área en hectárea calculada correctamente!'.title())

# Eliminar por UMC
arcpy.management.SelectLayerByAttribute(capa_disolver + "_2", 'NEW_SELECTION',"AreaHa < 1")
arcpy.management.Eliminate(capa_disolver + "_2", os.path.join(carpeta_memoria, capa_final), 'AREA')
arcpy.management.CalculateField(capa_final,'AreaHa',"!shape!.getArea('GEODESIC', 'HECTARES')", 'PYTHON3')
arcpy.management.SelectLayerByAttribute(capa_disolver + "_2", 'CLEAR_SELECTION') # Limpiar la selección
print('Eliminar polígonos por Unidad Mínima Cartografiable realizado!'.title())

# Final script
print("\nFin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

################
# ZONIFICACION #
################

import arcpy, time, os
#from arcpy import sa
from time import strftime
# Parámetros de entorno
arcpy.env.overwriteOutput = True

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
print('\ncalculando zonificación!'.upper())

# Variables de usuario
carpeta_memoria = r'memory' # Carpeta de trabajo
# Capas de entrada y salida
capa_sensibilidad = 'sensibilidad'
capa_acceso = 'acceso'

capa_union = 'zona_union'
capa_disolver = 'zona_dis'
capa_final = 'zona_amc'
# Campo de interés
campo_puntaje = 'zona_score'

# Unión de capas
arcpy.analysis.Union([capa_sensibilidad, capa_acceso],os.path.join(carpeta_memoria, capa_union),gaps=True)
print('Unión de capas realizada!'.title())

# Llave única de coordenadas
arcpy.management.CalculateField(capa_union,'llave', "str(!shape!.truecentroid.x) + '-' + str(!shape!.truecentroid.y)", 'PYTHON3','', 'TEXT')
print('Llave única de polígonos generada!'.title())

# Calcular el puntaje en nuevo campo
fields = arcpy.ListFields(capa_union) # Identificar campos de la capa
score_fields = [field.name for field in fields if field.name.startswith('score')] # Obtener la lista de campos que comienzan con "score"
expression = ' + '.join([f'!{field}!' for field in score_fields]) # Construir la expresión para la suma
arcpy.management.CalculateField(capa_union, campo_puntaje, expression, 'PYTHON3', '', 'SHORT') # Calcular campo con suma de campos de interés
print('Puntaje calculado correctamente!'.title())

# Disolver y sumar
arcpy.management.Dissolve(capa_union, os.path.join(carpeta_memoria, capa_disolver), dissolve_field='llave', statistics_fields=[[campo_puntaje, 'SUM']], multi_part=False)
print('Disolución de capas por llave realizada!'.title())

# Disolver por categoría y dar puntaje
# Asignar campo de nivel de urbanización y score
arcpy.AddField_management(capa_disolver,'nivel','TEXT',field_length=50)
arcpy.AddField_management(capa_disolver,'score','SHORT')
print('Campos creados correctamente!'.title())

# Ingresar valor de grado de urbanización
with arcpy.da.UpdateCursor(capa_disolver, [f'SUM_{campo_puntaje}', 'nivel', 'score']) as cursor:
    for row in cursor:
        if row[0] <= 7:
            row[1] = 'Zona de muy difícil acceso'
            row[2] = row[0]
        elif row[0] == 6:
            row[1] = 'Zona de muy difícil acceso'
            row[2] = row[0]
        elif row[0] == 5:
            row[1] = 'Zona de acceso moderado'
            row[2] = row[0]
        elif row[0] == 4:
            row[1] = 'Zona de acceso moderado'
            row[2] = row[0]
        elif row[0] == 3:
            row[1] = 'Zona de acceso con restricción baja'
            row[2] = row[0]
        elif row[0] == 2:
            row[1] = 'Zona de acceso con restricción baja'
            row[2] = row[0]
        else:
            row[1] = 'Área de fácil acceso'
            row[2] = row[0]
        cursor.updateRow(row) # Impactar cambios en la tabla
print('Valores de zonificación calculados correctamente!'.title())

# Disolver por nivel de zonificación
arcpy.management.Dissolve(capa_disolver, os.path.join(carpeta_memoria, capa_disolver + "_2"), dissolve_field=['nivel','score'], multi_part=False)
print('Disolución de capas por nivel de zonificación realizada!'.title())

# Calcular área en hectáreas
arcpy.AddField_management(capa_disolver + "_2",'AreaHa','DOUBLE')
arcpy.management.CalculateField(capa_disolver + "_2" ,'AreaHa',"!shape!.getArea('GEODESIC', 'HECTARES')", 'PYTHON3')
print('Área en hectárea calculada correctamente!'.title())

# Eliminar por Unidad Mínima Cartografiable
arcpy.management.SelectLayerByAttribute(capa_disolver + "_2", 'NEW_SELECTION',"AreaHa < 1")
arcpy.management.Eliminate(capa_disolver + "_2", os.path.join(carpeta_memoria, capa_final), 'AREA')
arcpy.management.CalculateField(capa_final,'AreaHa',"!shape!.getArea('GEODESIC', 'HECTARES')", 'PYTHON3')
arcpy.management.SelectLayerByAttribute(capa_disolver + "_2", 'CLEAR_SELECTION') # Limpiar la selección
print('Eliminar polígonos por Unidad Mínima Cartografiable realizado!'.title())

# Final script
print("\nFin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))