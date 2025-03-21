import arcpy, time,os
from time import strftime

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

#########################################
# MÉTODO 1: ÁREA PREDOMINANTE POR CELDA #
#########################################

##################
# MALLA CUADRADO #
##################

# Capas
capa_entrada = 'malla_cuadrado'
# Areas
area_cuadrado = 0.998

# Intersectar capas
arcpy.analysis.Intersect([capa_entrada,'zonificacion'],r'memory\malla_inter')

# Calcular áreas
arcpy.management.CalculateField('malla_inter','AreaHa',"round(!shape!.getArea('GEODESIC', 'SQUAREKILOMETERS'),3)", 'PYTHON3')

# Calcular porcentaje
arcpy.management.AddField('malla_inter','Porcen', 'SHORT')
arcpy.management.CalculateField('malla_inter', 'Porcen',f"round(!AreaHa!/{area_cuadrado}*100,0)", 'PYTHON3') # Para cuadrado

# Ordenar y eliminar por áreas
arcpy.management.CopyRows('malla_inter',r'memory\table_malla_inter')
arcpy.management.Sort(in_dataset="table_malla_inter", out_dataset=r"memory\table_malla_sort", sort_field="id ASCENDING;AreaHa DESCENDING")
#arcpy.management.Sort(in_dataset="malla_inter", out_dataset=r"memory\malla_sort", sort_field="id ASCENDING;AreaHa DESCENDING", spatial_sort_method="UR")
arcpy.management.DeleteIdentical('table_malla_sort', 'id')

# Unir campo a malla original
arcpy.management.JoinField(capa_entrada, 'id', 'table_malla_sort', 'id',['nivel','score','Porcen'])

##################
# MALLA HEXAGONO #
##################

# Capas
capa_entrada = 'malla_hexagono'
# Areas
area_hexagono = 0.865

# Intersectar capas
arcpy.analysis.Intersect([capa_entrada,'zonificacion'],r'memory\malla_inter')

# Calcular áreas
arcpy.management.CalculateField('malla_inter','AreaHa',"round(!shape!.getArea('GEODESIC', 'SQUAREKILOMETERS'),3)", 'PYTHON3')
# Disolver y sumar áreas
arcpy.management.Dissolve('malla_inter', r'memory\malla_dis', dissolve_field=['id','nivel','score'], statistics_fields=[['AreaHa','SUM']], multi_part=True)

# Calcular porcentaje
arcpy.management.AddField('malla_dis','Porcen', 'SHORT')
arcpy.management.CalculateField('malla_dis', 'Porcen',f"round(!SUM_AreaHa!/{area_hexagono}*100,0)", 'PYTHON3') # Para hexágono

# Ordenar y eliminar por áreas
arcpy.management.CopyRows('malla_dis',r'memory\table_malla_inter')
arcpy.management.Sort(in_dataset="table_malla_inter", out_dataset=r"memory\table_malla_sort", sort_field="id ASCENDING;SUM_AreaHa DESCENDING")
#arcpy.management.Sort(in_dataset="malla_inter", out_dataset=r"memory\malla_sort", sort_field="id ASCENDING;AreaHa DESCENDING", spatial_sort_method="UR")
arcpy.management.DeleteIdentical('table_malla_sort', 'id')

# Unir campo a malla original
arcpy.management.JoinField(capa_entrada, 'id', 'table_malla_sort', 'id',['nivel','score','Porcen'])

# Final script
print("\nFin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

###############################
# MÉTODO 2: PUNTAJE POR CELDA #
###############################

import arcpy, time,os
from time import strftime

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

##################
# MALLA CUADRADO #
##################

# Capas
capa_entrada = 'malla_cuadrado'

# Intersectar capas
arcpy.analysis.Intersect([capa_entrada,'zonificacion'],r'memory\malla_inter')

# Disolver capas y calcular estadística
arcpy.management.Dissolve('malla_inter', r'memory\malla_dis', dissolve_field='id', statistics_fields=[['score','MEAN'], ['score','MEDIAN']], multi_part=True)

# Unir campo a malla original
arcpy.management.JoinField(capa_entrada, 'id', 'malla_dis', 'id',['MEAN_score','MEDIAN_score'])

##################
# MALLA HEXAGONO #
##################

arcpy.env.overwriteOutput = True

# Capas
capa_entrada = 'malla_hexagono'

# Intersectar capas
arcpy.analysis.Intersect([capa_entrada,'zonificacion'],r'memory\malla_inter')

# Disolver capas y calcular estadística
arcpy.management.Dissolve('malla_inter', r'memory\malla_dis', dissolve_field='id', statistics_fields=[['score','MEAN'], ['score','MEDIAN'], ['score','MAX']], multi_part=True)

# Unir campo a malla original
arcpy.management.JoinField(capa_entrada, 'id', 'malla_dis', 'id',['MEAN_score','MEDIAN_score','MAX_score'])

# Final script
print("\nFin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))


# Calcular nivel de acceso al agua (categórico)

# Asignar campo de nivel de urbanización y score
arcpy.AddField_management('malla_hexagono_m2','nivel','TEXT',field_length=50)

# Ingresar valor de grado de urbanización
with arcpy.da.UpdateCursor('malla_hexagono_m2', ['MEAN_score', 'nivel']) as cursor:
    for row in cursor:
        if row[0] <= 1:
            row[1] = 'Zona de fácil acceso'
        elif row[0] <= 3:
            row[1] = 'Zona de acceso con restricción baja'
        elif row[0] <= 5:
            row[1] = 'Zona de acceso moderado'
        else:
            row[1] = 'Zona de muy difícil acceso'
        cursor.updateRow(row) # Impactar cambios en la tabla
print('Valores de zonificación calculados correctamente!'.title())

# Calcular descripción de zona en campo a partir de tipo

with arcpy.da.UpdateCursor('malla_hexagono_m2_max', ['nivel', 'descripcion']) as cursor:
    for row in cursor:
        if 'moderado' in row[0]:
            row[1] = 'Zonas con presencia de fuentes hídricas y acceso a ellas, pero los factores de sensibilidad como minería, deforestación, cultivos de uso ilícito, presencia de MAP, etcétera, representan un grado de dificultad para hacer uso de ellas.'
        elif 'fácil' in row[0]:
            row[1] = 'Zonas con presencia de fuentes hídricas y en donde los factores de sensibilidad como minería, deforestación, cultivos de uso ilícito, presencia de MAP, etcétera, no tienen presencia o su presencia es baja.'
        elif 'difícil' in row[0]:
            row[1] = 'Zonas sin cuerpos de agua y con acceso limitado a recursos, como vías o áreas urbanas con posibilidad de inversión en desarrollo de acueducto y alcantarillado, pero son sensibles por factores como minería, deforestación, cultivos de uso ilícito, etcétera.'
        else:
            row[1] = 'Zonas con presencia de fuentes hídricas, es fácil acceder a ellas pero que se pueden ver afectadas por algún factor de sensibilidad como minería, deforestación, cultivos de uso ilícito, presencia de MAP, etcétera.'
        cursor.updateRow(row) # Impactar cambios en la tabla
print('Descripción de zonas calculados correctamente!'.title())