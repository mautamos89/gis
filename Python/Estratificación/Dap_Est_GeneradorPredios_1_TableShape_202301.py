# coding=utf-8
# Title: generador de predios catastrales a partir de alfa-carto #1: generación de conjunto de datos
# Requirements:
#   License: N/A
#   Files: Cadastrial table and shapefile
# Author: Mauricio Tabares Mosquera, Geographer, GIS Specialist
# Date: 20230201

print ("START OF PROGRAM [0/7]")

#***********************#
# Import system modules #
#***********************#

import arcpy,os,datetime
from arcpy import env
from time import strftime
print("script started: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
tstart = datetime.datetime.now() # Start timer
print("SET SCRIPT MODULES DONE!")

#**********************#
# Environment settings #
#**********************#

arcpy.env.overwriteOutput = True
arcpy.env.parallelProcessingFactor = "0"
GdbPath = r'D:\catastro20230804.gdb\\' #Path to cadastrial information GDB
InTable = GdbPath + 'dat_cat_bas_catastral_tmp' # Tabla alfanumérica de predios catastrales
InShp = GdbPath + r'SIC_IDESC\GEO_TERRENOS' # Capa geográfica de terrenos catastrales
Fol_InFiles = r'd:\\' #Root folder for output creation
Fol_InMem = r'in_memory' #In memory workspace path
Fol_OutFiles = arcpy.CreateFileGDB_management(Fol_InFiles, 'EstQT_FileGDB_2023.gdb').getOutput(0) # Must change for new GDB

#***************************#
# Start of table processing #
#***************************#

print ("START OF [1/8] -------------> TABLE: COPY TABLE TO MEMORY AND DESCRIBE SCRIPT!")
arcpy.env.workspace = Fol_InMem #Must change for saving location
Out_TabNam = 'Table_Tmp'
Out_TabMem = os.path.join(Fol_InMem, Out_TabNam)
arcpy.CopyRows_management(InTable, Out_TabMem)
i = 0 #Start counter
TabLstMem = sorted(arcpy.ListTables(), reverse=False)
for Tab in TabLstMem:
    i +=1 #Add one registry to counter
    NumRows = arcpy.GetCount_management(Tab)
    print(str(i) + ' | ' + Tab.split('.')[0] + ' | Number of records: ' + str(NumRows))
print ("END OF -------> COPY TABLE TO MEMORY AND DESCRIBE SCRIPT!")

print ("START OF [2/8] -------------> FIELDS MANAGEMENT SCRIPT #1!")
FieLst = sorted(arcpy.ListFields(Out_TabMem),reverse=False) #Filter fields to delete
FieLstOk =['OBJECTID','ID_PREDIO','DEPAPRED','MUNIPRED','COMUNA','BARRIO','MANZANA','TERRENO','CONDICION','NPN','IDTERRENO','NUMEPRED','DIREPRED']

i = 0
for fl in FieLst: #Type the name of the field you want to keep
    if fl.name not in FieLstOk:
        i += 1
        arcpy.DeleteField_management(Out_TabMem,fl.name) #Delete field process
        print(str(i) + ' | Delete field: ' + fl.name)
    else:
        i += 0
        print(str(i) + ' | Keep field: ' + fl.name)
print ("FIELDS MANAGEMENT #1 -------------> DONE!")

print ("START OF [3/8] -------------> EXPORT ROWS TO TABLE SCRIPT!")
i = 0
ii = 0
#ComLst = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22'] #Fixed value list
ComLst = sorted(set(row[0] for row in arcpy.da.SearchCursor(Out_TabMem, "COMUNA")), reverse=False) #Dynamic unique value list
print('Unique values found: ' + str(ComLst) + ' | Total values: ' + str(len(ComLst)))
for Com in ComLst:
    if Com == None or Com == '00':
     ii += 1
     print('Terrenos sin comuna: ' + str(ii))
    else:
        SqlQue = "COMUNA = '" + Com + "'" # Must change for table and shapefile processing
        Out_Name = 'Tab_PreCom_' + str(Com)# + '.dbf' # Must delete file extension for saving in memory location
        Out_Table = os.path.join(Fol_OutFiles, Out_Name) #Change for saving folder location
        arcpy.MakeTableView_management(Out_TabMem, Out_Name, SqlQue) #Make a table with SQL selection
        arcpy.CopyRows_management(Out_Name,Out_Table) #Copy table to specific location
        i +=1
        print(str(i) + ' | Exporting table: ' + str(Out_Name))

print ("START OF [4/8] -------------> DESCRIBE TABLE IN MEMORY SCRIPT!")
arcpy.env.workspace = Fol_OutFiles
i = 0 #Start counter
TabLst = sorted(arcpy.ListTables('Tab_PreCom_*'), reverse=False)
for Tab in TabLst:
    i +=1 #Add one registry to counter
    NumRows = arcpy.GetCount_management(Tab)
    print(str(i) + ' | ' + Tab.split('.')[0] + ' | Number of records: ' + str(NumRows))
print ("END OF -------> DESCRIBE TABLE IN MEMORY SCRIPT!")

#*******************************#
# Start of shapefile processing #
#*******************************#

print ("START OF [5/8] -------------> SHAPEFILE: COPY SHAPEFILE TO MEMORY AND DESCRIBE SCRIPT!")
arcpy.env.workspace = Fol_InMem
Out_ShpNam = 'Shape_Tmp'
Out_ShpMem = os.path.join(Fol_InMem, Out_ShpNam)
arcpy.CopyFeatures_management(InShp, Out_ShpMem)
i = 0 #Start counter
ShpLstMem = sorted(arcpy.ListFeatureClasses(), reverse=False)
for Shp in ShpLstMem:
    i +=1 #Add one registry to counter
    NumRows = arcpy.GetCount_management(Shp)
    print(str(i) + ' | ' + Shp.split('.')[0] + ' | Number of records: ' + str(NumRows))
print ("END OF -------> COPY SHAPEFILE TO MEMORY AND DESCRIBE SCRIPT!")

print ("START OF [6/8] -------------> FIELDS MANAGEMENT SCRIPT #1!")
FieLst = sorted(arcpy.ListFields(Out_ShpMem),reverse=False) #List the fields from shapefile
FieLstOk =['OBJECTID','COMUNA','BARRIO','MANZANA','CONEXION','SHAPE','SHAPE_Length','SHAPE_Area']
i = 0
for fl in FieLst: #Type the name of the field you want to keep
    if fl.name not in FieLstOk:
        i += 1
        arcpy.DeleteField_management(Out_ShpMem,fl.name) #Delete field process
        print(str(i) + ' | Delete field: ' + fl.name)
    else:
        i += 0
        print(str(i) + ' | Keep field: ' + fl.name)
# Crear campo identificador único: geo_id
arcpy.AddField_management(Out_ShpMem,'geo_id','LONG')
counter = 1
with arcpy.da.UpdateCursor(Out_ShpMem, ['geo_id']) as cursor:
    for row in cursor:
        # Actualizar el valor del campo con el contador
        row[0] = counter
        # Actualizar la fila en la tabla
        cursor.updateRow(row)
        # Incrementar el contador
        counter += 1
print ("FIELDS MANAGEMENT #1 -------------> DONE!")

print ("START OF [7/8] -------------> EXPORT ROWS TO TABLE SCRIPT!")
i = 0
ii = 0
#ComLst = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22'] #Fixed value list
ComLst = sorted(set(row[0] for row in arcpy.da.SearchCursor(Out_ShpMem, "COMUNA")), reverse=False) #Dynamic unique value list
print('Unique values found: ' + str(ComLst) + ' | Total values: ' + str(len(ComLst)))
for Com in ComLst:
    if Com == None or Com == '00' or Com == '':
     ii += 1
     print('Terrenos sin comuna: ' + str(ii))
    else:
        SqlQue = "COMUNA = '" + Com + "'" # Must change for table and shapefile processing
        Out_Name = 'Shp_PreCom_' + str(Com)# + '.shp' # Must delete file extension for saving in memory location
        Out_Shp1 = os.path.join(Fol_OutFiles, Out_Name) #Change for saving folder location
        arcpy.MakeFeatureLayer_management(Out_ShpMem, Out_Name, SqlQue) #Make a table with SQL selection
        arcpy.CopyFeatures_management(Out_Name,Out_Shp1) #Copy table to specific location
        i +=1
        print(str(i) + ' | Exporting shapefile: ' + str(Out_Name))

print ("START OF [8/8] -------------> DESCRIBE SHAPEFILE IN MEMORY SCRIPT!")
arcpy.env.workspace = Fol_OutFiles
i = 0 #Start counter
ShpLst = sorted(arcpy.ListFeatureClasses('Shp_PreCom_*'), reverse=False)
for Shp in ShpLst:
    i +=1 #Add one registry to counter
    NumRows = arcpy.GetCount_management(Shp)
    print(str(i) + ' | ' + Shp.split('.')[0] + ' | Number of records: ' + str(NumRows))
print ("END OF -------> DESCRIBE SHAPEFILE IN MEMORY SCRIPT!")

#**************************#
# Start of clean workspace #
#**************************#

print ("START OF [*] -------------> CLEANING FOLDER PROGRAM!")
arcpy.env.workspace = Fol_InMem
DelFiles = TabLstMem + ShpLstMem #List files to delete
i = 0
for z in DelFiles:
    if 'Shp_Pre' not in z and 'Tab_Pre' not in z: #Create a filtered list of files to delete
        i += 1
        arcpy.Delete_management(z) #Process to delete files
        print(str(i) + ' | Delete file: ' + z)
    else:
        i += 0
        print(str(i) + ' | Keep file: ' + z)
print ("CLEANING FOLDER -------------> DONE!")
arcpy.Delete_management("in_memory")

print ("END OF PROGRAM")
tend = datetime.datetime.now() # Stop timer
a,b,c = str(tend-tstart).split(':')[0].zfill(2), str(tend-tstart).split(':')[1].zfill(2), str(round(float(str(tend-tstart).split(':')[2]),0)).split('.')[0].zfill(2)
print('script running time: {a} hours : {b} minutes : {c} seconds'.format(a=a,b=b,c=c).upper())
print("script finished: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

""" print('Opening Script #2: GeneradorPredios_2_TableShape_202301')
import GeneradorPredios_2_TableShape_202301
print('Executing Script #2: GeneradorPredios_2_TableShape_202301') """