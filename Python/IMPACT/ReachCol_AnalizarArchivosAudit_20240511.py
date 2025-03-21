# coding=utf-8
# Título: Descargar archivos audit en formato texto, contar el número de líneas de cada uno y calcular estadísticas resumen.
# Requerimientos: Python 3x, Archivo texto con URL de Audit
# Librerías: os, requests, time, glob, statistics, multiprocessing
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2024-05-11

import os, requests, glob, statistics # type: ignore
from time import strftime
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Variables de usuario
directory = r'D:\audit' # Carpeta de trabajo
down_folder= r'D:\audit\download' # Carpeta de descargas
txt_file = 'url_file.txt' # Archivo con lista de URL
lineas = 66 # Límite de líneas aceptadas de presuntos archivos incompletos

# Definición de funciones
def conteo_archivos(a):
    """
    Función que cuenta archivos del directorio.
    """
    global list_of_files
    list_of_files = glob.glob(f'{a}/*.txt')
    #print(f"Total de archivos: {len(list_of_files)}.")

def conteo(a):
    """
    Función que compara los archivos encontrados con los esperados.
    """
    list_of_files = glob.glob(f'{a}/*.txt')
    print(f"\nArchivos encontrados: {len(list_of_files)}/{len(lista_descarga)}.\n")
    exclude_list, include_list, analisis_list=[], [], []
    for fileName in list_of_files:
        with open(fileName, 'r') as file:
            lines = file.readlines()
            line_count = len(lines)
            analisis_list.append(line_count)
            fullname = os.path.basename(fileName[:-4])
            promedio = round(statistics.mean(analisis_list),1)
            desv = round(statistics.pstdev(analisis_list),1)
            if line_count >= lineas:
                exclude_list.append(fullname)
            else:
                include_list.append(fullname)
                print(f'Audit UUID: {fullname}, Número de líneas: {line_count}.')
    print(f"\nEstadísticas:\nMínimo de líneas: {min(analisis_list)} | Máximo de líneas: {max(analisis_list)}\n\
Promedio de líneas: {promedio} | Mediana de líneas: {statistics.median(analisis_list)}\n\
Desviación estándar: {desv} | Cola[-]: {round(promedio-(2*desv),1)} | Cola[+]: {round(promedio+(2*desv),1)}\n\
Quantiles: {statistics.quantiles(analisis_list, n=5, method='exclusive')}\n")
    print(f"Resumen:\nArchivos audit con menos de {lineas} líneas: {len(include_list)}.")
    print(f"Archivos audit con más de {lineas} líneas: {len(exclude_list)}.")

def crear_descarga(a,b):
    """
    Función que crea la lista de archivos a descargar desde el archivo de texto.
    """
    global lista_descarga
    lista_descarga = []
    archivo_url = open(os.path.join(a, b), 'r')  
    for line in archivo_url:
        url = line.strip() # Retirar el salto de línea
        lista_descarga.append(url) 
    
def descarga_archivos(url):
    """
    Función que descarga y guarda los archivos listados.
    """
    file_name = os.path.join(down_folder, f"{(url.split('%')[3])[2:]}.txt")
    r = requests.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        with open(file_name, 'wb') as f:
            for data in r:
                f.write(data)
                #time.sleep(0.1) # Necesario si falla la lectura/escritura en disco
    return url

# Ejecutar funciones
crear_descarga(directory, txt_file)
conteo_archivos(down_folder)
if len(lista_descarga) != len(list_of_files):
    print(f"\nArchivos encontrados: {len(list_of_files)}/{len(lista_descarga)}.")
    print("\nDescargando archivos audit.\n".upper())
    crear_descarga(directory, txt_file)
    print(f"Total enlaces generados: {len(lista_descarga)} | Hilos de descarga paralelos: {cpu_count()}.\n")
    results = ThreadPool(cpu_count()).imap_unordered(descarga_archivos, lista_descarga) # Multiprocesamiento utiliza las CPU disponibles
    for i, r in enumerate(results, start=1):
        print(f"{i}-{r}")
print("\nAnalizando archivos audit.".upper())
conteo(down_folder) 

# Final script
print("\nFin de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))