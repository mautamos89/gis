# coding=utf-8
# Título: Identificar el campo con el valor máximo por filas en Arcpy en el campo texto "resultado"
# Requerimientos: ArcGIS Pro, Python 3x
# Librerías: arcpy, time
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2024-06-08

# Variables de usuario
capa = 'pto_mzn'
campos = ['TP19_EE_E1','TP19_EE_E2','TP19_EE_E3','TP19_EE_E4','TP19_EE_E5','TP19_EE_E6','TP19_EE_E9']
resultado = 'resultado'

# Librerías
import arcpy, time
from time import strftime

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Función
def campo_maximo_valor(lista_campos, capa_in, valor_final):
    """
    Función para identificar el campo con el valor máximo por filas
    """
    arcpy.AddField_management(capa_in,valor_final,'text',field_length=50)
    with arcpy.da.UpdateCursor(capa_in, lista_campos + [valor_final]) as cursor:
        for row in cursor:
            max_value = max(row[:-1])
            max_index = row.index(max_value)
            if max_value == 0:
                row[-1] = 'N/A'
                cursor.updateRow(row)
            else:
                row[-1] = lista_campos[max_index]#.split('_')[-1]
                cursor.updateRow(row)

# Llamar la función
campo_maximo_valor(campos, capa, resultado)

# Final script
print("Fin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))