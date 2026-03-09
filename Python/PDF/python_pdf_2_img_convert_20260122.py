# coding=utf-8
# Título: Convertir archivos PDF de una página en archivos de imagen individuales
# Requerimientos: Sistema operativo Windows
# Librerías: os, pymupdf, time
# Autor: Mauricio Tabares
# Fecha: 2026-01-22
# Versión: 1.0

import os, pymupdf
from time import strftime

# Script start
print("script start: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Parameters
input_fol = r'C:\Users\TabaresM\OneDrive - AECOM\Digital EC Colombia - GIS\Projects\6. GEPET\1_Input\graphs_pdf_2025'
ouput_fol = r'C:\Users\TabaresM\OneDrive - AECOM\Digital EC Colombia - GIS\Projects\6. GEPET\2_Workspace\PNG'
img_format = 'png'
img_dpi = 300

# Function
def convert_folder_pdfs_to_images(input_folder, output_folder, final_format, dpi):
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Process all PDF files
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        # Get filename without extension
        pdf_name = os.path.splitext(pdf_file)[0]
        
        try:
            # Open the PDF document
            doc = pymupdf.open(pdf_path)
            
            if doc.page_count > 0:
                # Load only the first page (0-indexed)
                page = doc.load_page(0)
                
                # Render page to a pixmap (image)
                # dpi parameter handles the resolution directly
                pix = page.get_pixmap(dpi=dpi)
                
                # Save the image
                output_path = os.path.join(output_folder, f"{pdf_name}.{final_format.lower()}")
                pix.save(output_path)
                
                print(f"Success: {pdf_name}.{final_format}")
            
            doc.close()
                
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")

# Run function
convert_folder_pdfs_to_images(input_fol, ouput_fol, img_format, img_dpi)

# Script end
print("script end: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))