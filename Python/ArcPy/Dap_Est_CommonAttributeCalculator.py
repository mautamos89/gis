# coding=utf-8
#CÁLCULO AUTOMATIZADO DE CAMPOS EN COMÚN ENTRE FEATURES
from time import strftime
import arcpy
print("Start script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
print('title: transfer of multiple field values between feature classes with common field sets python script'.upper())
print('requirements: arcgis basic license tools'.upper())
print('autor: mauricio tabares mosquera'.upper())
print('career: geographer, gis specialist'.upper())
print('fecha: 2023-07-29'.upper())
#Info source: https://community.esri.com/t5/python-blog/turbo-charging-data-manipulation-with-python/ba-p/884079
kf = ['ID_PREDIO','OBJECTID','Shape','Shape_Length','Shape_Area','FECHA_EDIT','NUMEPRED','NPN']
InTab = 'pdt_est_estrato_predios' # Capa actualizada y orígen de los datos
OutTab = 'est_bd_maestra_20231229' # Capa para actualizar y destino de los datos
lf1,lf2 = arcpy.ListFields(InTab), arcpy.ListFields(OutTab)
lf = list(sorted(set((list(set(x.name for x in lf1))))&set((list(set(x.name for x in lf2)))),reverse=False))
for a in lf: a if a not in kf else lf.remove(a)
lf.insert(0,kf[0])
print('SOURCE TABLE: {a}, NUMBER OF RECORDS: {b}'.format(a=InTab,b=arcpy.GetCount_management(InTab)))
print('DESTINATION TABLE: {a}, NUMBER OF RECORDS: {b}'.format(a=OutTab,b=arcpy.GetCount_management(OutTab)))
print('COUNT OF COMMON FIELDS: {a}'.format(a=len(lf)))
print('creating dictionary with data'.upper())
# Build a dictionary from a da SearchCursor
valueDict = {r[0]:(r[1:]) for r in arcpy.da.SearchCursor(InTab, lf)}
print('updating field values with data'.upper())
with arcpy.da.UpdateCursor(OutTab, lf) as updateRows:
    for updateRow in updateRows: # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
        if keyValue in valueDict: # verify that the keyValue is in the Dictionary
            for n in range (1,len(lf)): # transfer the values stored under the keyValue from the dictionary to the updated fields.
                updateRow[n] = valueDict[keyValue][n-1]
            updateRows.updateRow(updateRow)
del valueDict
print("Finished script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))