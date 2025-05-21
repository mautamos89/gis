# coding=utf-8
# Título: Identificar y copiar feature classes de una carpeta a Base de Datos Geográfica (GDB)
# Requerimientos: ArcGIS Pro, Python 3x
# Librerías: arcpy, os, time
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2024-03-08 

# Librerías
try:
    import arcpy, os, time
    from time import strftime
    arcpy.env.overwriteOutput = True
except:
    print('Poblema importando librerías')
else:
    print('Librerías cargadas con éxito')

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Directorios
carpeta = r'D:\test' # Carpeta con archivos
gdb = r'D:\hola.gdb' # GDB destino

# Función para listar los feature class de una carpeta
def listar_feat(x):
    try:
        global feat_list
        feat_list = []
        arcpy.env.workspace = x
        for a in arcpy.ListFeatureClasses():
            #print(a[:-4]) # Listar los nombres de los archivos
            feat_list.append(a[:-4])
    except:
        print('Problema con la carpeta o los archivos')
    else:
        print(f'Total de archivos a copiar: {len(feat_list)}')

# Función para copiar feature classes a GDB
def copiar_gdb(y):
    i = []
    try:
        while len(feat_list) == 0:
            print('No hay archivos para copiar')
            break
        else:
            for n,a in enumerate(feat_list,start=1):
                arcpy.CopyFeatures_management(a,os.path.join(y,a))
                print(f'{n} | Archivo copiado en: {os.path.join(y,a)} | Número de entidades: {arcpy.GetCount_management(a)}')
                i.append(n)
                time.sleep(1)
    except:
        print('Problema al copiar los archivos. Revise las carpetas y permisos de escritura')
    else:
        print(f'Total de archivos copiados: {len(i)}')

# Ejecutando funciones
listar_feat(carpeta) # Ingrese la carpeta de interés
copiar_gdb(gdb) # La GDB de interés

# Final script
print("Fin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))