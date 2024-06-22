# coding=utf-8
# Título: Identificar y copiar feature classes de una carpeta a Base de Datos Geográfica (GDB)
# Requerimientos: ArcGIS Pro, Python 3x
# Librerías: arcpy, os, time
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2024-03-08 

import arcpy,os,time
from time import strftime
from arcpy import env # type: ignore
arcpy.env.overwriteOutput = True

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Parámetros usuario
dpto = 'valle' # Must
capa_dpto = 'dv_Departamento' # Must
cobertura = 'cobertura_tierra2000_2002V2' # Must
campo_lvl3 = 'nivel3' # Must

# Parámetros fijos
memory = 'memory'
temporal = os.path.join(memory,cobertura + '_mem')
campo_cod = 'LCod'
campo_gtrans = 'GTransform'
dpto_tmp = os.path.join(memory,dpto + '_mem')
campo_ha = 'AreaHa'
campo_nom_dpto = 'NOM_DEPART'
dpto_dis = os.path.join(memory,dpto + '_dis')

# Diccionario Corine Land Cover y valores de transformación
dic_corine_trans = {'Natural': (311,312,313,314,315,321,322,323,331,332,333,335,411,412,413,421,422,423,511,512,521,522),
               'Semi-natural': (141,211,212,213,214,215,221,222,223,224,225,231,232,233,241,242,243,244,245,334,523),
               'Transformado': (111,112,121,122,123,124,125,131,132,142,513,514)}

# Función para regresar valor de transformación
def buscar_llave(valor, dic):
    for key, values in dic.items():
        if valor in values:
            return key
    return None #return 'No encontrado'

# Geoprocesamiento municipio
print('Iniciando geoprocesamiento')
arcpy.SelectLayerByAttribute_management(capa_dpto, 'NEW_SELECTION',f"lower({campo_nom_dpto}) LIKE '%{dpto.lower()}%'")
print('Cortando entidades geográficas')
arcpy.Clip_analysis(cobertura,capa_dpto,dpto_tmp)
arcpy.SelectLayerByAttribute_management(capa_dpto, 'CLEAR_SELECTION')
print('Agregando campos y calculando áreas')
arcpy.AddField_management(dpto_tmp,campo_ha,'DOUBLE')
arcpy.CalculateField_management(dpto_tmp,campo_ha,f'!shape.area@hectares!','PYTHON3')
print(f'Tabla: {dpto_tmp}, Número de registros: {arcpy.GetCount_management(dpto_tmp)}')

# Actualizando estructura de tabla y valores
print('Generando código de leyenda CLC')
arcpy.AddField_management(dpto_tmp,campo_cod, 'LONG')
arcpy.CalculateField_management(dpto_tmp, campo_cod,f"!{campo_lvl3}!.split(' ')[0].replace('.','')", 'PYTHON3') # Extraer código de leyenda nivel 3
#arcpy.DeleteIdentical_management(dpto_tmp, campo_lvl3) # Borrar repetidos
arcpy.AddField_management(dpto_tmp,campo_gtrans, 'TEXT',field_length= 25)
resultado = f'buscar_llave(!{campo_cod}!, {dic_corine_trans})' # Llamar la función
arcpy.CalculateField_management(dpto_tmp,campo_gtrans,resultado,'PYTHON3') # Calcular el campo aplicando función

# Disolviendo y calculando pocentajes de ocupación
arcpy.Dissolve_management(dpto_tmp,dpto_dis, campo_gtrans, [[campo_ha,'SUM']])
lista_area = []
with arcpy.da.SearchCursor(dpto_dis, 'SUM_AreaHa') as cursor:
    for row in cursor:
        lista_area.append(round(row[0],3))
arcpy.AddField_management(dpto_dis,'Porcentaje','FLOAT')
arcpy.CalculateField_management(dpto_dis,'Porcentaje',f"round((!SUM_AreaHa! / {sum(lista_area)})*100,3)")

# Exportar tabla
""" print('updating fields attributes finished\nexporting new table started'.upper())
arcpy.CopyRows_management(tmp,tgdb) # Change second argument for saving location [tfol=folder,tgdb=gdb]
print('exporting new table finished. location: {a}'.format(a=tgdb).upper()) # Change second argument for saving location [tfol=folder,tgdb=gdb] """

# Borrar archivos temporales
#arcpy.Delete_management(memory)
print('memory cleaned'.upper())

# Final script
print("Fin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))