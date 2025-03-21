# coding=utf-8
# Título: Procesar geometrías adyacentes y unir por atributos y propiedades espciales con Arcpy y VStudio Code
# Requerimientos: ArcGIS Pro, Python 3x
# Librerías: arcpy, time, os
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2024-07-31

# Variables de usuario | User inputs
feature_in = 'hexa_mem'
population_threshold = 100
population_field = 'pop'

# Librerías
import os,arcpy
from time import strftime
arcpy.env.overwriteOutput = True

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Crea una copia en la memoria
memory_path = 'memory'
hexagon_fc = arcpy.management.CopyFeatures(feature_in,os.path.join(memory_path,feature_in + '_tmp'))

# Crea un campo temporal para la fusión
merge_group = 'MergeGr'
arcpy.AddField_management(hexagon_fc, merge_group, 'SHORT')

# Identifica hexágonos con baja población
low_pop_hexagons = []
with arcpy.da.SearchCursor(hexagon_fc, ['OID@', population_field]) as cursor:
    for row in cursor:
        if row[1] < population_threshold:
            low_pop_hexagons.append(row[0])

print(f"OID a procesar:{low_pop_hexagons}\nTotal de entidades: {len(low_pop_hexagons)}")

# Lógica de fusión
new_group_id = 1  # Inicializa un nuevo ID de grupo para la fusión

while low_pop_hexagons:
    # Repetir hasta que no haya más hexágonos adyacentes
    low_pop_hexagons_aux = low_pop_hexagons[:] # Crea una copia de la lista
    for low_hex in low_pop_hexagons_aux:
        # Obtiene la geometría del hexágono actual
        with arcpy.da.SearchCursor(hexagon_fc, ['OID@', 'SHAPE@']) as cursor:
            for row in cursor:
                if row[0] == low_hex:
                    low_hex_geom = row[1]
                    break

        # Crea un filtro espacial para encontrar hexágonos adyacentes
        print(f'Procesando grupo de geometría adyacente: {new_group_id}')
        with arcpy.da.SearchCursor(hexagon_fc, ['OID@', 'SHAPE@', population_field]) as cursor:
            for adj_hex in cursor:
                # Verifica si es adyacente (también puede usar relaciones espaciales)
                if low_hex_geom.overlaps(adj_hex[1]) or low_hex_geom.touches(adj_hex[1]):
                    if low_hex != adj_hex[0]:
                        total_pop = adj_hex[2]  # Usa la población del hexágono adyacente
                        if total_pop >= population_threshold:
                            # Asigna el mismo grupo para la fusión
                            with arcpy.da.UpdateCursor(hexagon_fc, ['OID@', merge_group]) as update_cursor:
                                for update_row in update_cursor:
                                    if update_row[0] == low_hex or update_row[0] == adj_hex[0]:
                                        update_cursor.updateRow([update_row[0], new_group_id])
                            new_group_id += 1  # Incrementa el ID de grupo para la próxima fusión
                            low_pop_hexagons.remove(low_hex) # Elimina el hexágono de baja población de la lista
                            break

    # Actualiza la lista de hexágonos adyacentes
    with arcpy.da.SearchCursor(hexagon_fc, ['OID@', population_field]) as cursor:
        for row in cursor:
            if row[1] < population_threshold and row[0] not in low_pop_hexagons:
                low_pop_hexagons.append(row[0])
                break
    break

(print("Grupos creados y preparando para exportar"))
# Prepara para exportar
arcpy.management.MakeFeatureLayer(hexagon_fc,'hexa_mem_group',f"{merge_group} is not null")

# Disuelve
arcpy.management.Dissolve('hexa_mem_group',r'memory\output_dis', merge_group,[[population_field,'SUM']])

# Campos
arcpy.management.AddField('output_dis',population_field,'SHORT')
arcpy.management.CalculateField('output_dis',population_field,f"!SUM_{population_field}!", 'PYTHON3')
arcpy.management.DeleteField('output_dis', f"SUM_{population_field}",method="DELETE_FIELDS")

# Seleccionar y borrar nuevos hexagonos
arcpy.management.SelectLayerByLocation('hexa_mem_tmp', 'HAVE_THEIR_CENTER_IN', 'output_dis')
arcpy.management.DeleteFeatures('hexa_mem_tmp')

# Unir capas y exportar
(print("Arhivo final exportado"))
arcpy.management.Merge(['output_dis','hexa_mem_tmp'],r'memory/salida_final')
arcpy.management.DeleteField('salida_final', merge_group,method="DELETE_FIELDS")

# Borrar capas temporales
list_delete_features = ['hexa_mem_group','output_dis','hexa_mem_tmp']
for a in list_delete_features: arcpy.Delete_management(a)
print('Archivos temporales borrados')

# Final script
print("Fin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))