import geopandas as gpd, fiona

def cargar_capa_gpkg(ruta_archivo):
    """
    Carga todas las capas de un GPKG y las devuelve en diccionario con prefijo 'gdf_'.
    """
    print("\nScript | Función-1: Cargar archivos desde GPKG\n")
    capas = fiona.listlayers(ruta_archivo) # Obtener las capas
    diccionario_gdfs = {} # Crear diccionario de capas

    for nombre in capas:
        nombre_variable = f"gdf_{nombre}"
        diccionario_gdfs[nombre_variable] = gpd.read_file(ruta_archivo, layer=nombre) # Cargar y guardar en diccionario
        print(f"Capa cargada: {nombre} | Variable: {nombre_variable} | Entidades: {len(diccionario_gdfs[nombre_variable])} | CRS: {diccionario_gdfs[nombre_variable].crs}")
    return diccionario_gdfs

def crear_buffer(diccionario_capa, capa_rio, buffer_distancia):
    """
    Crear buffer a partir de capa de entrada.
    """
    print("\nScript | Función-2: Crear buffer para capa de río\n")
    capa_entrada = diccionario_capa['gdf_' + capa_rio]
    gdf_buffer = capa_entrada.buffer(buffer_distancia)
    print(f"Buffer (m): {buffer_distancia} | Área capa entrada: {round(capa_entrada.area.sum(),3)} | Área capa salida: {round(gdf_buffer.area.sum(),3)}")
    return gdf_buffer

def edificio_afectado(diccionario_capa, capa_edificio, gdf_buffer):
    """
    Selección espacial de edificios que toquen el buffer.
    """
    print(f"\nScript | Función-3: Selección espacial de edificios afectados\n")
    gdf_edificios = diccionario_capa['gdf_' + capa_edificio] # Acceder a cada a través de edificio
    union_buffer = gdf_buffer.unary_union # Unir geometría múltiple de buffer
    mask = gdf_edificios.intersects(union_buffer) # Definir máscara para intersectar
    edificio_afectado = gdf_edificios.loc[mask].copy() # Seleccionar edificios afectados y copiar gdf
    print(f"Número de edificios afectados: {len(edificio_afectado)} | Área afectada: {round(edificio_afectado.area.sum(),3)}")
    return edificio_afectado

def exportar_resultado(gdf, nombre_salida):
    """
    Exporta un GeoDataFrame a formato GeoJSON en la raíz del script.
    """
    print(f"\nScript | Función-4: Exportando resultado a .geojson\n")
    ruta_salida = rf".\{nombre_salida}.geojson" # Definir ruta y nombre de salida
    gdf.to_file(ruta_salida, driver='GeoJSON') # Exportar a GeoJSON
    print(f"Archivo exportado: {ruta_salida}")
    return ruta_salida

def comprobar_archivo(gdf_salida):
    """
    Lee y verifica la integridad del archivo GeoJSON exportado.
    """
    print(f"\nScript | Función-5: Verificar archivo exportado\n")
    ruta = f'.\{gdf_salida}' # Cargar archivo
    gdf_cargado = gpd.read_file(ruta) # Leer archivo
    columnas = ", ".join(gdf_cargado.columns)
    n_filas, n_cols = gdf_cargado.shape
    print(f"Columnas: {columnas}")
    print(f"Dimensiones: {n_filas} filas & {n_cols} columnas\nCRS: {gdf_cargado.crs} | Área total: {round(gdf_cargado.area.sum(), 3)}")    
    return gdf_cargado
