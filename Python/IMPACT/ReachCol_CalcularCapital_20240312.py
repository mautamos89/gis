# coding=utf-8
# Título: Calcular el valor entero para la evaluación de capitales por feature class y el campo texto "APT"
# Requerimientos: ArcGIS Pro, Python 3x
# Librerías: arcpy, time
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2024-03-12 

# Variables
fc = 'capital_natural_1' # Ruta al archivo, puede ser parcial o absoluta
field_int = 'APT_Int' # Campo a crear con aptitud en número entero
field_apt = 'APT_CNatur' # Campo referencia con aptitud en texto

# Librerías
try:
    import arcpy
    from time import strftime
    arcpy.env.overwriteOutput = True
except:
    print('Poblema importando librerías'.upper())
else:
    print('Librerías cargadas con éxito'.upper())

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Crear campo APT
arcpy.management.AddField(fc, field_int, 'SHORT')

# Función
def apt(a):
    if 'baj' in a.lower():
        return '3'
    elif 'med' in a.lower():
        return '2'
    elif 'alt' in a.lower():
        return '1'
    else:
        return None

# Calcular campo
arcpy.management.CalculateField(fc, field_int, f'apt(!{field_apt}!)', 'PYTHON3')

# Final script
print("Fin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))