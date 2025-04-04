# coding=utf-8
# Título: Identificar el grado de transformación de cobertura de la tierra por unidad político-administrativa
# Requerimientos: ArcGIS Pro, Python 3x
# Librerías: arcpy, os, time
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2024-03-18 

import arcpy, os, time, re
from time import strftime
from arcpy import env # type: ignore
arcpy.env.overwriteOutput = True

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Parámetros usuario
cobertura = 'cobertura_tierra_clc_2018' # Capa de coberturas de la tierra a usar
capa_dpto = 'dv_Municipio' # Capa político administrativa a usar
dpto = 'puerto asís' # Entidad de interés

# Parámetros condicionales
nums = re.findall(r'\d+', cobertura)
cob_year = f"cob_{'_'.join(nums)}"
if cobertura == 'cobertura_tierra_clc_2018':
    campo_lvl3 = 'nivel_3'
elif cobertura == 'Cobertura_tierra_2010_2012':
    campo_lvl3 = 'leyenda3n'
else:
    campo_lvl3 = 'nivel3'

# Parámetros fijos
campo_nom_dpto = 'NOM_MUNICI' # 'NOM_DEPART' analizar nivel departamental; 'NOM_MUNICI' analizar nivel municipal
memory = 'memory'
temporal = os.path.join(memory,cobertura + '_mem')
campo_cod = 'LCod'
campo_gtrans = 'GTransform'
dpto_tmp = os.path.join(memory,dpto.lower().replace(' ','_') + '_'  + cob_year + '_mem')
campo_ha = 'AreaHa'
dpto_dis = os.path.join(memory,dpto.lower().replace(' ','_') + '_' + cob_year + '_dis')

# Diccionario Corine Land Cover y valores de transformación
dic_corine_trans = {'Natural': (311,312,313,314,315,321,322,323,331,332,333,335,411,412,413,421,422,423,511,512,521,522),
               'Semi-natural': (141,211,212,213,214,215,221,222,223,224,225,231,232,233,241,242,243,244,245,334,523),
               'Transformado': (111,112,121,122,123,124,125,131,132,142,513,514)}

# Función para regresar valor de transformación
def buscar_llave(valor, dic):
    """
    Función que regresa la categría de la cobertura
    """
    for key, values in dic.items():
        if valor in values:
            return key
    #return None #return 'No encontrado'
    return 'Nubes' # Valores no encontrados son nubes

# Geoprocesamiento municipio
print(f'Iniciando geoprocesamiento\nCapa: {cobertura}, Campo: {campo_lvl3}')
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
print('Disolviendo y calculando porcentajes de ocupación')
arcpy.Dissolve_management(dpto_tmp,dpto_dis, campo_gtrans, [[campo_ha,'SUM']])
lista_area = []
with arcpy.da.SearchCursor(dpto_dis, 'SUM_AreaHa') as cursor:
    for row in cursor:
        lista_area.append(row[0])
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