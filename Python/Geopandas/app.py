# coding=utf-8
# Título: Práctica 4-Programación de geoprocesos
# Requerimientos: Python 3x
# Librerías: geopandas, time
# Autor: Mauricio Tabares Mosquera
# Fecha: 2026-03-02

import geopandas as gpd
from function.functions import cargar_capa_gpkg, crear_buffer, edificio_afectado, exportar_resultado, comprobar_archivo
from time import strftime

# Inicio de script
print("\nScript iniciado: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Variables de usuario

# Ruta de archivo GPKG
ruta_archivo = r"D:\msc\8_analisis_espacial_python\practica_4\datos_p4.gpkg"
# Capa de río
capa_rio = 'onyar'
# Distancia para buffer
buffer_metros = int(input("Ingrese la distancia del buffer en metros: "))
# Capa edificio
capa_edificio = 'edificios'
# Nombre archivo salida
nombre_salida = 'edificio_afectado'

# Ejecutar funciones

# Cargar datos
capas = cargar_capa_gpkg(ruta_archivo)
# Crear buffer
buffer = crear_buffer(capas, capa_rio, buffer_metros)
# Seleccionar edificios afectados
afectado = edificio_afectado(capas, capa_edificio, buffer)
# Exportar resultado
exportar = exportar_resultado(afectado, nombre_salida)
# Comprobar archivo exportado
comprobar_archivo(exportar)

# Fin script
print("\nScript terminado: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))