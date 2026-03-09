
# coding=utf-8
# Título: Imprimir las plantillas de un proyecto de ArcGIS Pro
# Requerimientos: Sistema operativo Windows, Arcpy
# Librerías: os, arcpy, time
# Autor: Mauricio Tabares
# Fecha: 2026-01-30
# Versión: 1.0

# NO CORRE STANDALONE!!

import arcpy, os
from time import strftime

# Script start
print("script start: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# User inputs
dpi = 225
# Path to .aprx file
aprx_path = r"C:\Users\TabaresM\OneDrive - AECOM\Digital EC Colombia - GIS\Projects\6. GEPET\20260210\Workspace\GEPET_1_DR_S01\GEPET_1_DR_S01.aprx"
# Folder where PDFs will be saved
output_folder = r"C:\Users\TabaresM\Downloads\export_test1"

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Reference the ArcGIS Pro Project
aprx = arcpy.mp.ArcGISProject(aprx_path)

# Loop through all layouts with a counter
for i, lyt in enumerate(aprx.listLayouts(), start=1):
    pdf_path = os.path.join(output_folder, f"{lyt.name}.pdf")
    print(f"{i}-Exporting: {lyt.name}...")
    # Export the layout
    lyt.exportToPDF(pdf_path, resolution=dpi, image_quality="BEST")#, image_compression='JPEG')

print("All layouts exported successfully.")

# Script end
print("script end: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))