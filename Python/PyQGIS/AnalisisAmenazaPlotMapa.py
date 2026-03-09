# coding=utf-8
# Título: Scripting con SIG desktop
# Requerimientos: QGIS, Python 3x
# Librerías: qgis.core, qgis.gui, qtwidgets, datetime, time
# Autor: Mauricio Tabares Mosquera
# Fecha: 2026-03-05

from qgis.core import *
from qgis.gui import *
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtCore import QCoreApplication
import sys, datetime
from time import strftime

# Inicio de script
print("\nScript iniciado: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# SECCIÓN 1: PARÁMETROS DE USUARIO

print("\nSección 1: Establecer parámetros de usuario\n".upper())

titulo_mapa, ok1 = QInputDialog.getText(None, "Configuración", "Título del mapa:", 0, "Mapa de incidente: Municipios y población afectada en Catalunya")
buffer_input, ok2 = QInputDialog.getInt(None, "Configuración", "Radio del buffer (metros):", 5000)
coords_input, ok3 = QInputDialog.getText(None, "Configuración", "Coordenadas (X,Y) EPSG:25831:", 0, "404000,4620000")

# Validación de parámetros
if not (ok1 and ok2 and ok3):
    raise Exception("Operación cancelada por el usuario; revisa los parámetros")

# Procesar variables de entrada
x, y = map(float, coords_input.split(','))
distancia_buffer = float(buffer_input)
# Imprimir en consola
print(f"Título mapa: {titulo_mapa}\nBuffer (m): {distancia_buffer} | Longitud (X): {x} | Latitud (Y): {y}")

# SECCIÓN 2: CARGA DE CAPA BASE (MUNICIPIOS)

print("\nSección 2: Cargar capa de municipios\n".upper())

# Limpiar composición existente y evitar duplicados
nombres_capas = ["municipios", "Area de Afectacion"]
for nombre in nombres_capas:
    for capa in QgsProject.instance().mapLayersByName(nombre):
        QgsProject.instance().removeMapLayer(capa.id())

# Agregar nueva capa
ruta_capa = r"D:\msc\8_analisis_espacial_python\practica_5\datos_p5.gpkg|layername=municipios"
capa_municipios = QgsVectorLayer(ruta_capa, "municipios", "ogr")

if not capa_municipios.isValid():
    raise Exception("No se pudo cargar la capa de municipios, revisa la ruta.")

# Añadir al proyecto para que sea visible
QgsProject.instance().addMapLayer(capa_municipios)

print(f"Nombre capa: {capa_municipios.name()} | Número de entidades: {capa_municipios.featureCount()} | CRS: {capa_municipios.crs().authid()}")

# SECCIÓN 3: ANÁLISIS GEOGRÁFICO Y POBLACIÓN

print("\nSección 3: Análisis geográfico y cálculo de población\n".upper())

# Crear geometrías
punto_incidente = QgsGeometry.fromPointXY(QgsPointXY(x, y)) # Punto
buffer_geom = punto_incidente.buffer(distancia_buffer, 25) # Buffer

# Contador de población
total_personas_afectadas = 0
# Contador de municipios
num_municipios_afectados = 0
# Iterar por entidades y sumar por intersección
for municipio in capa_municipios.getFeatures():
    if municipio.geometry().intersects(buffer_geom):
        total_personas_afectadas += municipio['POBLACION'] # Sumar a variable
        num_municipios_afectados += 1

print(f"Municipios afectados: {num_municipios_afectados} | Población: {total_personas_afectadas}")

# SECCIÓN 4: CREACIÓN DE CAPA DE AFECTACIÓN (VISUAL)

print("\nSección 4: Crear capa visual del buffer\n".upper())

crs_id = capa_municipios.crs().authid()
area_afectacion = QgsVectorLayer(f"Polygon?crs={crs_id}", "Area de Afectacion", "memory")
dp = area_afectacion.dataProvider()

# Añadir la geometría resultante
f = QgsFeature()
f.setGeometry(buffer_geom)
dp.addFeatures([f])
area_afectacion.updateExtents() # Ajusta ficha técnica de capa

print(f"Área afectada calculada. Distancia: {distancia_buffer}")

# SECCIÓN 5: CONFIGURAR SIMBOLOGÍA

print("\nSección 5: Configurar simbología\n".upper())

# Capa municipios
props_municipios = {
    'color': '#7d8b8f',
    'outline_color': 'black',
    'size': '1.5'
}
simbolo_puntos = QgsMarkerSymbol.createSimple(props_municipios)
capa_municipios.renderer().setSymbol(simbolo_puntos)

# Label: formato de texto
settings = QgsPalLayerSettings()
format = QgsTextFormat()
format.setFont(QFont("Segoe UI", 10))
format.setSize(10)
format.setColor(QColor("black"))
settings.setFormat(format)
settings.fieldName = "NOMCAP" # Variable del label
settings.enabled = True
# Label: posición
settings.placement = QgsPalLayerSettings.AroundPoint
settings.dist = 1.0 # Separación
# Label: aplicar a la capa
labels = QgsVectorLayerSimpleLabeling(settings)
capa_municipios.setLabeling(labels)
capa_municipios.setLabelsEnabled(True)

# Capa buffer
props_buffer = {
    'color': '255,0,0,66',
    'outline_color': 'red',
    'outline_width': '0.3'
}
simbolo_buffer = QgsFillSymbol.createSimple(props_buffer)
area_afectacion.renderer().setSymbol(simbolo_buffer)

# Refrescar ambas capas
capa_municipios.triggerRepaint()
area_afectacion.triggerRepaint()

print("Simbología aplicada a capas")

# SECCIÓN 6: GESTIÓN DEL ÁRBOL DE CAPAS

print("\nSección 6: Ordenar capas del proyecto\n".upper())

# Capa afectación, parámetro false evita añadir al final
QgsProject.instance().addMapLayer(area_afectacion, False)
# Parámetro 1 la inserta después de los municipios
QgsProject.instance().layerTreeRoot().insertChildNode(1, QgsLayerTreeLayer(area_afectacion))

print(f"Capas ordenadas y agregadas a proyecto")

# SECCIÓN 7: COMPOSICIÓN DE MAPA Y EXPORTACIÓN PDF

print("\nSección 7: Crear composición de mapa\n".upper())

# Limpiar layout previo
nombre_layout = "mapa_script"
proyecto = QgsProject.instance()
manager = proyecto.layoutManager()
layout_existente = manager.layoutByName(nombre_layout) # Verificar layout
if layout_existente:
    manager.removeLayout(layout_existente)
    print(f"Layout manager ajustado")

# Crear el layout
proyecto = QgsProject.instance()
layout = QgsPrintLayout(proyecto)
layout.initializeDefaults() # Configura A4 landscape por defecto
layout.setName("mapa_script")

# Ajustar a vertical (portrait)
pc = layout.pageCollection()
pagina = pc.pages()[0]
pagina.setPageSize(QgsLayoutSize(210, 297, QgsUnitTypes.LayoutMillimeters)) # Medidas A4
proyecto.layoutManager().addLayout(layout) # Agregar a layout manager

# Finalizar procesos pendientes
QCoreApplication.processEvents()

# Añadir mapa a Layout
mapa = QgsLayoutItemMap(layout)
mapa.attemptMove(QgsLayoutPoint(20, 30, QgsUnitTypes.LayoutMillimeters))
mapa.attemptResize(QgsLayoutSize(170, 180, QgsUnitTypes.LayoutMillimeters)) # Más alto para portrait
mapa.setFrameEnabled(True) # Añade un borde al mapa
mapa.setLayers([area_afectacion, capa_municipios]) # Asignación explícita de capas

# Ajustar extensión del mapa
layout.addLayoutItem(mapa)
mapa.setExtent(buffer_geom.boundingBox().scaled(1.5))

# Añadir texto formateado de título
titulo = QgsLayoutItemLabel(layout)
titulo.setText(titulo_mapa)
titulo.setFont(QFont("Segoe UI", 15, QFont.Bold))
titulo.adjustSizeToText()
titulo.attemptMove(QgsLayoutPoint(20, 10, QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(titulo)

# Añadir texto formateado de varables
info_pob = QgsLayoutItemLabel(layout)
fecha_hoy = datetime.date.today().strftime('%Y-%m-%d') # Definir la fecha actual
texto_pob = f"Municipio afectado: {num_municipios_afectados}\nPoblación asociada: {total_personas_afectadas:,}\nFecha: {fecha_hoy}"
info_pob.setText(texto_pob)
info_pob.setFont(QFont("Segoe UI", 8, QFont.Normal, True))
info_pob.adjustSizeToText()
info_pob.attemptMove(QgsLayoutPoint(22, 202, QgsUnitTypes.LayoutMillimeters)) # Colocar el texto
layout.addLayoutItem(info_pob)

# Añadir flecha norte
flecha = QgsLayoutItemPicture(layout)
# Ajustar ruta de SVG
ruta_svg = r"C:\Program Files\QGIS 3.34.14\apps\qgis-ltr\svg\arrows\NorthArrow_02.svg"
flecha.setPicturePath(ruta_svg)
flecha.attemptResize(QgsLayoutSize(13, 13, QgsUnitTypes.LayoutMillimeters))
flecha.attemptMove(QgsLayoutPoint(179, 30, QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(flecha)

# Refrescar y esperar finalización renderizado
layout.refresh()
mapa.refresh()
QCoreApplication.processEvents() # Esperar renderizado

# Exportar mapa a PDF
ruta_pdf = r"D:\msc\8_analisis_espacial_python\practica_5\p5_mapa_script.pdf"
exporter = QgsLayoutExporter(layout)
resultado = exporter.exportToPdf(ruta_pdf, QgsLayoutExporter.PdfExportSettings())

if resultado == QgsLayoutExporter.Success:
    print(f"Mapa exportado en: {ruta_pdf}")
else:
    print("Error al generar el mapa")

# Fin script
print("\nScript terminado: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))