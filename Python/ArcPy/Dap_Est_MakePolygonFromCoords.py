#CREACIÓN AUTOMATIZADA DE POLÍGONOS A PARTIR DE TABLA DE COORDENADAS

#################################
# DATUM ESRI
# MAGNA CALI VALLE DEL CAUCA 2009
#"PROJCS['MAGNA_Cali_Valle_del_Cauca_2009',GEOGCS['GCS_MAGNA',DATUM['D_MAGNA',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['IGAC_Plano_Cartesiano'],PARAMETER['False_Easting',1061900.18],PARAMETER['False_Northing',872364.63],PARAMETER['Longitude_Of_Center',-76.5205625],PARAMETER['Latitude_Of_Center',3.441883333333334],PARAMETER['Height',1000.0],UNIT['Meter',1.0]]"
# MAGNA COLOMBIA OESTE
#"PROJCS['MAGNA_Colombia_Oeste',GEOGCS['GCS_MAGNA',DATUM['D_MAGNA',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',1000000.0],PARAMETER['False_Northing',1000000.0],PARAMETER['Central_Meridian',-77.07750791666666],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',4.596200416666666],UNIT['Meter',1.0]]")
#################################
import arcpy
from time import strftime
print("Start script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
print('title: automated generation of polygon-type geographic entity and attributes from a list of georeferenced points python script'.upper())
print('requirements: arcgis basic license tools'.upper())
print('autor: mauricio tabares mosquera'.upper())
print('career: geographer, gis specialist'.upper())
print('fecha: 2023-07-29'.upper())
arcpy.MakeXYEventLayer_management('pry_coord','X','Y','xy_pnt',"PROJCS['MAGNA_Cali_Valle_del_Cauca_2009',GEOGCS['GCS_MAGNA',DATUM['D_MAGNA',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['IGAC_Plano_Cartesiano'],PARAMETER['False_Easting',1061900.18],PARAMETER['False_Northing',872364.63],PARAMETER['Longitude_Of_Center',-76.5205625],PARAMETER['Latitude_Of_Center',3.441883333333334],PARAMETER['Height',1000.0],UNIT['Meter',1.0]]")
arcpy.PointsToLine_management('xy_pnt',r'in_memory\xy_line','NOMBRE','PUNTO','CLOSE')
ml = []
with arcpy.da.SearchCursor('xy_line','NOMBRE') as cursor:
    for row in cursor:
        if row[0] != None:
            n = r'in_memory\xy_poly_' + row[0]
            n1 = r'in_memory\xy_poly_spa_' + row[0]
            ml.append(n1)
            arcpy.SelectLayerByAttribute_management('xy_line','NEW_SELECTION',"NOMBRE = '{a}'".format(a=row[0]))
            arcpy.FeatureToPolygon_management('xy_line',n,'','ATTRIBUTES')
            arcpy.SpatialJoin_analysis(n,'xy_line',n1,'JOIN_ONE_TO_ONE','KEEP_ALL','','CLOSEST')
            arcpy.SelectLayerByAttribute_management('xy_line','CLEAR_SELECTION',"NOMBRE = '{a}'".format(a=row[0]))
arcpy.Merge_management(ml,r'in_memory\merge')
arcpy.AddField_management('merge','AreMt2','DOUBLE')
arcpy.CalculateField_management('merge','AreMt2','!shape.area@squaremeter!','PYTHON_9.3')
df=['Join_Count','TARGET_FID']
for a in arcpy.ListFields('merge'): arcpy.DeleteField_management('merge',a.name) if a.name in df else a
arcpy.CopyFeatures_management('merge','Polygons')
arcpy.Delete_management('in_memory')
print("Finished script: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))