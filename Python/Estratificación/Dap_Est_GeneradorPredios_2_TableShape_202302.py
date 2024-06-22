# coding=utf-8
# Title: generador de predios catastrales a partir de alfa-carto #2: creación de entidad geográfica "predio" y cálculo de atributos
# Requirements:
#   License: N/A
#   Files: Cadastrial table and shapefile from script #1
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
Fol_OutFiles = r'd:\EstQT_FileGDB_2023.gdb'
Fol_InMem = r'in_memory'
Range = 37 # Cambiar según el conjunto de datos a procesar: Urbano = 22; Rural = 15
arcpy.env.workspace = Fol_OutFiles

#*********************************#
# Start of table query processing #
#*********************************#

print ('START OF [1/7] -------------> TABLE QUERY SCRIPT!')
print('Number of iterations: ' + str(Range))
LstA_Shp, LstB_Tab = sorted(arcpy.ListFeatureClasses('Shp_PreCom_*'),reverse=False), sorted(arcpy.ListTables('Tab_PreCom_*'),reverse=False)
LstA_Shp1,LstB_Tab1 = LstA_Shp[: + Range], LstB_Tab[: + Range]
#print('Shape list: ' + str(LstA_Shp1) + ' | Table list: ' + str(LstB_Tab1)) # Files needed for query table tool
i = 0
shp = ['OBJECTID','COMUNA','BARRIO','MANZANA','CONEXION','SHAPE','SHAPE_Length','SHAPE_Area','geo_id'] # Campos para la generación
tab = ['OBJECTID','ID_PREDIO','DEPAPRED','MUNIPRED','COMUNA','BARRIO','MANZANA','TERRENO','CONDICION','NPN','IDTERRENO','NUMEPRED','DIREPRED']
for Shp, Tab in zip(LstA_Shp1, LstB_Tab1):
    InTabLst = [Shp, Tab]
    QT_Fields = [[Shp + '.Shape', 'Shape'],[Shp + '.CONEXION', 'CONEXION'],[Shp + '.geo_id', 'geo_id'],\
    [Tab + '.ID_PREDIO', 'ID_PREDIO'],[Tab + '.NPN', 'NPN'],[Tab + '.COMUNA', 'COMUNA'],[Tab + '.BARRIO', 'BARRIO'],[Tab + '.MANZANA', 'MANZANA'],[Tab + '.IDTERRENO', 'IDTERRENO'],[Tab + '.DIREPRED', 'DIRECCION'],[Tab + '.CONDICION', 'CONDICION'],[Tab + '.NUMEPRED', 'NUMEPRED']]
    SqlQue = Shp + '.CONEXION = ' + Tab + '.IDTERRENO'
    Out_Name = 'QTab_' + str(Shp) # + '.shp' # Must delete file extension for saving in memory location
    QLyr = "QTLayer"
    arcpy.MakeQueryTable_management(InTabLst, QLyr , "ADD_VIRTUAL_KEY_FIELD", "", QT_Fields, SqlQue) #Make the query table
    arcpy.CopyFeatures_management(QLyr, os.path.join(Fol_OutFiles,Out_Name)) #Copy table to specific location
    i +=1
    print(str(i) + ' | Exporting QT Tuple: [Shape: ' + Shp + ' & Table: ' + Tab + ']' + ' | Shapefile records: ' + str(arcpy.GetCount_management(Shp)) + ' | Table records: ' + str(arcpy.GetCount_management(Tab)))
print('END OF -------> TABLE QUERY SCRIPT!')

# Ajustar nombre de campos para producto final
print ("START OF [2/7] -------------> FIELDS MANAGEMENT SCRIPT #1!")
ShpLst = sorted(arcpy.ListFeatureClasses('QTab_*'))
for Shp in ShpLst:
    FieLst = sorted(arcpy.ListFields(Shp),reverse=False) #Filter fields to delete
    i = 0
    ii = 0
    for fl in FieLst: #Type the name of the field you want to keep
        if len(fl.name) >= 15 and ('CONEXION' not in fl.name or 'OBJECTID' not in fl.name):
            i += 1
            NewFieNam = fl.aliasName
            print(str(i) + ' | Shapefile: ' + Shp + ' | Field name to modify: ' + fl.name + ' | New field name: ' + NewFieNam)
            arcpy.AlterField_management(Shp,fl.name, NewFieNam,NewFieNam)
        elif fl.aliasName == 'CONEXION':
            ii += 1
            NewFieNam = str(fl.aliasName) + str(ii)
            print(str(ii) + ' | Shapefile: ' + Shp + ' | Field name to modify: ' + fl.name + ' | New field name: ' + NewFieNam)
            arcpy.AlterField_management(Shp,fl.name, NewFieNam,NewFieNam)
        else:
            i += 0
    print ("FIELDS MANAGEMENT #1 -------------> DONE!")

print ("START OF [3/7] -------------> MERGE OF FEATURE CLASSES # 1 SCRIPT!")
Out_ShpMer1 = os.path.join(Fol_InMem,'Shp_Mer_Tmp') #Merged file created name
arcpy.Merge_management(LstA_Shp, Out_ShpMer1) # Merge the shapefiles
# Generar índice de terrenos catastrales
fields = arcpy.ListFields(Out_ShpMer1)
for a in fields:
    if a.name == 'geo_id':
        values = [row[0] for row in arcpy.da.SearchCursor(Out_ShpMer1, a.name)]
        ter_todos = sorted(set(values),reverse=False)
        print(u'Capa: {0} | Campo: {1} | Valores únicos: {2}'.format(Out_ShpMer1,a.name,len(ter_todos)))
print ("MERGE OF FEATURE CLASSES #1 -------------> DONE!")

print ("START OF [4/7] -------------> MERGE OF FEATURE CLASSES #2 SCRIPT!")
Out_ShpMer2 = os.path.join(Fol_OutFiles,'QTab_Mer_Com') #Merged file created name
arcpy.Merge_management(ShpLst, Out_ShpMer2) # Merge the shapefiles
# Generar índice de terrenos conectados
fields = arcpy.ListFields(Out_ShpMer2)
for a in fields:
    if a.name == 'geo_id':
        values = [row[0] for row in arcpy.da.SearchCursor(Out_ShpMer2, a.name)]
        ter_conectados = sorted(set(values),reverse=False)
        print(u'Capa: {0} | Campo: {1} | Valores únicos: {2}'.format(Out_ShpMer2,a.name,len(ter_conectados)))
print ("MERGE OF FEATURE CLASSES #2 -------------> DONE!")

print ("START OF [5/7] -------------> GENERAR LISTA DE TERRENOS NO CONECTADOS SCRIPT!")
ter_no_conectados = []
for a in ter_todos:
    if a in ter_conectados:
        continue
    elif a not in ter_conectados:
        ter_no_conectados.append(a)
print('Terrenos no conectados: {0}'.format(len(ter_no_conectados)))
#print(ter_no_conectados)
clausula = "{} IN ({})".format(arcpy.AddFieldDelimiters(Out_ShpMer1, 'geo_id'), ','.join(map(str, ter_no_conectados)))
arcpy.AddField_management(Out_ShpMer1,"CONTROL",'TEXT',field_length='15')
arcpy.MakeFeatureLayer_management(Out_ShpMer1,'Geo_Tmp',clausula)
arcpy.CalculateField_management('Geo_Tmp',"CONTROL",'"""No conectado"""','PYTHON_9.3')
print ("LISTA DE TERRENOS NO CONECTADOS -------------> DONE!")

print ("START OF [6/7] -------------> MERGE OF FEATURE CLASSES #3 SCRIPT!")
Out_ShpMer3 = os.path.join(Fol_OutFiles,'QTab_Mer_Vf') #Merged file created name
arcpy.Merge_management([Out_ShpMer2,'Geo_Tmp',], Out_ShpMer3) # Merge the shapefiles
del Out_ShpMer1
print ("MERGE OF FEATURE CLASSES #3 -------------> DONE!")

print ("START OF [7/7] -------------> CALCULATE ATTRIBUTES SCRIPT!")
arcpy.MakeFeatureLayer_management(Out_ShpMer3,'Lyr1','CONEXION IS NULL')
arcpy.CalculateField_management('Lyr1',"CONEXION","!IDTERRENO!","PYTHON_9.3")
arcpy.MakeFeatureLayer_management(Out_ShpMer3,'Lyr1','CONTROL IS NULL')
arcpy.CalculateField_management('Lyr1',"CONTROL",'"""Conectado"""',"PYTHON_9.3")
arcpy.DeleteField_management(Out_ShpMer3,["IDTERRENO",'geo_id'])
print ("CALCULATE ATTRIBUTES -------------> DONE!")

#**************************#
# Start of clean workspace #
#**************************#

print ("START OF [*] -------------> CLEANING FOLDER PROGRAM!")
arcpy.Delete_management("in_memory")
arcpy.env.workspace = Fol_OutFiles
LstA = sorted(arcpy.ListFeatureClasses(),reverse=False)
LstB = sorted(arcpy.ListTables(),reverse=False)
DelFiles = LstA + LstB
i = 0
for z in DelFiles:
    if 'QTab_Mer_Vf' not in z: #Create a filtered list of files to delete
        i += 1
        arcpy.Delete_management(z) #Process to delete files
        print(str(i) + ' | Delete file: ' + z)
    else:
        i += 0
        print(str(i) + ' | Keep file: ' + z)
print ("CLEANING FOLDER -------------> DONE!")

print ("END OF PROGRAM")
tend = datetime.datetime.now()
a,b,c = str(tend-tstart).split(':')[0].zfill(2), str(tend-tstart).split(':')[1].zfill(2), str(round(float(str(tend-tstart).split(':')[2]),0)).split('.')[0].zfill(2)
print('script running time: {a} hours : {b} minutes : {c} seconds'.format(a=a,b=b,c=c).upper())
print("script finished: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))