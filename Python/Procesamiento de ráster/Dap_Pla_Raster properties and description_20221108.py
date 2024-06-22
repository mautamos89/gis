# Open a folder and iterate with rasters from the disk to print their properties
# Requirements: N/A
# Author: Mauricio Tabares Mosquera
# Date: 20190910 | Update: 20221108

import arcpy,time

# MUST CHANGE: Set script parameters for folder #1
folder = r'f:\planoteca\georreferenciacion\geor\pcs' #path to folder that contains the raster files
folder1 = r'f:\planoteca\georreferenciacion\geor\magna' #path to folder that contains the raster files
arcpy.env.workspace = folder
raster_list = arcpy.ListRasters()
print("START OF -------> DESCRIBE RASTER SCRIPT!")
START = time.clock() #Timer start
# Define function for scale relation using raster cesll size property
def RScale(Num):
    if Num <= 0.0132293:
     return '1:50'
    elif Num > 0.0132293 and Num <= 0.0264584:
     return '1:100'
    elif Num > 0.0264584 and Num <= 0.0396876:
     return '1:150'
    elif Num > 0.0396876 and Num <= 0.0529168:
     return '1:200'
    elif Num > 0.0529168 and Num <= 0.0661459:
     return '1:250'
    elif Num > 0.0661459 and Num <= 0.0793751:
     return '1:300'
    elif Num > 0.0793751 and Num <= 0.0926043:
     return '1:350'
    elif Num > 0.0926043 and Num <= 0.1058334:
     return '1:400'
    elif Num > 0.1058334 and Num <= 0.1190626:
     return '1:450'
    elif Num > 0.1190626 and Num <= 0.1322918:
     return '1:500'
    elif Num > 0.1322918 and Num <= 0.1455209:
     return '1:550'
    elif Num > 0.1455209 and Num <= 0.1587501:
     return '1:600'
    elif Num > 0.1587501 and Num <= 0.1719793:
     return '1:650'
    elif Num > 0.1719793 and Num <= 0.1852084:
     return '1:700'
    elif Num > 0.1852084 and Num <= 0.1984376:
     return '1:750'
    elif Num > 0.1984376 and Num <= 0.2116668:
     return '1:800'
    elif Num > 0.2116668 and Num <= 0.2248959:
     return '1:850'
    elif Num > 0.2248959 and Num <= 0.2381251:
     return '1:900'
    elif Num > 0.2381251 and Num <= 0.2513543:
     return '1:950'
    else:
     return '1:1000'
print('Processing folder: '+ folder + ' | Files found: ' + str(len(raster_list))) #Describe feature file then get its property
print("#|File Name|Compression Type|Spatial Reference|Pixel Type|No Data Value|Cell Size|Raster Scale")
i = 0
for r in raster_list:
    comp_type = arcpy.Describe(r).compressionType
    spa_ref = arcpy.Describe(r).spatialReference
    pix_type = arcpy.Raster(r).pixelType
    no_data = arcpy.Raster(r).noDataValue
    no_data_int = int(no_data)
    CellSize = arcpy.Raster(r).meanCellWidth
    rScale = RScale(CellSize)
    CellSize1 = (str(round(arcpy.Raster(r).meanCellHeight,7))).replace('.',',')
    i += 1
    print(str(i) + "|" + r.split(".")[0] + "|" + comp_type + "|" + spa_ref.name + "|" + pix_type + "|" + str(no_data_int) + "|" + str(CellSize1) + '|' + str(rScale))
print("END OF -------> DESCRIBE RASTER SCRIPT!")

#Set script parameters for folder #2
arcpy.env.workspace = folder1
raster_list1 = arcpy.ListRasters()
print("START OF -------> DESCRIBE RASTER SCRIPT!")
print('Processing folder: '+ folder1 + ' | Files found: ' + str(len(raster_list1))) #Dscribe feature file then get its property
print("#|File Name|Compression Type|Spatial Reference|Pixel Type|No Data Value|Cell Size|Raster Scale")
i = 0
for r in raster_list1:
    comp_type = arcpy.Describe(r).compressionType
    spa_ref = arcpy.Describe(r).spatialReference
    pix_type = arcpy.Raster(r).pixelType
    no_data = arcpy.Raster(r).noDataValue
    no_data_int = int(no_data)
    CellSize = arcpy.Raster(r).meanCellWidth
    rScale = RScale(CellSize)
    CellSize1 = (str(round(arcpy.Raster(r).meanCellHeight,7))).replace('.',',')
    i += 1
    print(str(i) + "|" + r.split(".")[0] + "|" + comp_type + "|" + spa_ref.name + "|" + pix_type + "|" + str(no_data_int) + "|" + str(CellSize1) + '|' + str(rScale))
print('TOTAL PROCESSED FILES: ' + str(len(raster_list1 + raster_list)))
print("END OF -------> DESCRIBE RASTER SCRIPT!")
END = int((time.clock()-START)/60) #Process timer set to minutes
print("SCRIPT RUNNING TIME -------> {} MINUTES".format(END))
