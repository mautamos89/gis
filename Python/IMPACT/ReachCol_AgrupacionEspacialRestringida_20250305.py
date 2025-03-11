# coding=utf-8
# Título: Agrupar entidades espaciales por proximidad y cuotas con Arcpy y VStudio Code
# Requerimientos: ArcGIS Pro, Python 3x
# Librerías: arcpy, time, os
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2025-03-05

import arcpy
from time import strftime

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Definir variables
capa = 'construccion_union_punto'

# Selección iterativa por el número de bloques
for a in range(1, 5):
    seleccion = arcpy.management.SelectLayerByAttribute(capa, 'NEW_SELECTION', f"hexa_id = {a}")
    
    # Get the count as an integer
    count = arcpy.da.TableToNumPyArray(seleccion, ['OID@']).shape[0]
    
    # Condicional si el número de puntos es >= a la cuota mínima de cluster
    if count > 7:
        print(f"Procesando hexa_id: {a}")
        arcpy.stats.SpatiallyConstrainedMultivariateClustering(
            in_features="construccion_union_punto",
            output_features=rf"memory\cluster_py_{a}",
            analysis_fields="latitud;longitud",
            size_constraints="NONE",
            constraint_field=None,
            number_of_clusters=7,
            spatial_constraints="TRIMMED_DELAUNAY_TRIANGULATION",
            weights_matrix_file=None,
            number_of_permutations=0,
            output_table=None
        )
    else:
        continue

# Final script
print("\nFin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))