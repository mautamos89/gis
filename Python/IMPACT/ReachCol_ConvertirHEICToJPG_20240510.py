# coding=utf-8
# Título: Listar y convertir las imágenes HEIC (iPhone) de una carpeta a JPG
# Requerimientos: Python 3x
# Librerías: pathlib, os, PIL, pillow_heif, time
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2024-05-10

# Importar librerías requeridas
import pathlib, os
from time import strftime
from PIL import Image
from pillow_heif import register_heif_opener
register_heif_opener()

# Variables de usuario
ruta_heic = r'D:\fotos\heic' # Carpeta de entrada
ruta_jpg = r'D:\fotos\jpg' # Carpeta de salida

# Inicio script
print("inicio de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Función para listar archivos e iniciar proceso de conversión
def conv_heic_jpg(ruta_in, ruta_out):
    """
    Función que convierte las fotos del directorio seleccionado.
    """
    files = list(pathlib.Path(ruta_in).glob("*.heic"))# + list(Path(".").glob("*.HEIC"))
    print(f'Convirtiendo {len(files)} archivos'.upper())
    for f in files:
        image = Image.open(str(f))
        file_name = os.path.join(ruta_out, f.name.split('.')[0] + '.jpg')
        image.convert('RGB').save(file_name)

# Ejecutar la función
conv_heic_jpg(ruta_heic, ruta_jpg)

# Final script
print("Final de script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))