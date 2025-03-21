# coding=utf-8
# Título: Exportar hoja electrónica a CSV con delimitador específico y revisar contenido
# Requerimientos: Visual Studio Code, Python 3x
# Librerías: pandas, openpyxl
# Autor: Equipo SIG / DATA | ACTED - REACH
# Fecha: 2024-08-21

# Importar librerías

import pandas as pd, os
pd.set_option('display.max_columns',200) # Cargar x columnas

# Carpeta de trabajo
carpeta = r'd:\\'

# Crear el data frame

df = pd.read_excel(os.path.join(carpeta, 'data_hsm.xlsx')) # Sintaxis: Libro, Hoja
print(f'Número de filas del Data frame: {df.shape[0]} | Número de columnas del Data frame: {df.shape[1]}\nArchivo cargado!') # Dimensionalidad del df
# print(df.head(3).to_string())

# Exportar el resultado a CSV

df.to_csv(os.path.join(carpeta, 'data_hsm.csv'),sep='|',index=False,encoding='utf-16')
print('Archivo exportado!')

# Revisar el archivo CSV exportado

df1=pd.read_csv(os.path.join(carpeta,'data_hsm.csv'),sep='|',encoding='utf-16') # Leer el archivo CSV con separador y codificación
print(f'{df1.head(3)}\nArchivo cargado!') # Imprimir el data frame completo