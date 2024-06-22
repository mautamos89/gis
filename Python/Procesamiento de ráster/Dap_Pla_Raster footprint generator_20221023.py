# Title: Raster processing script #1: Raster files to polygon footprint automatic generator
# Requirements:
#   License:
#       Spatial Analyst; Raster Calculator
#       3D Analyst; Raster Domain
#   Files: raster projected to local reference system
# Author: Mauricio Tabares Mosquera, Geographer, GIS Specialist
# Date: 20221023

print ("START OF PROGRAM [0/12]")
# Import system modules
import arcpy,os,time
from arcpy import env
from arcpy.sa import *
arcpy.env.overwriteOutput = True
arcpy.env.compression = "JPEG 75"
arcpy.env.pyramid = "NONE 0 CUBIC JPEG 75 NO_SKIP"
arcpy.env.tileSize = "128 128"
arcpy.env.resamplingMethod = "CUBIC"
arcpy.CheckOutExtension("3D") # Obtain a license for the ArcGIS 3D Analyst extension
arcpy.CheckOutExtension("Spatial") # Check out the ArcGIS Spatial Analyst extension license
START = time.clock() #Timer start
arcpy.env.parallelProcessingFactor = "0"
arcpy.AddMessage ("SET SCRIPT MODULES DONE!")

# Environment settings. MUST CHANGE FOR PROCESSING
#***************************
arcpy.env.workspace = r"F:\planoteca\georreferenciacion\geor\magna\\" #Folder where raster files are saved
out_folder_a = r"D:\pub\\" #Folder where new files will be saved
RasterDate = '20221230' #Date of processing
GdbPath = r'F:\planoteca\georreferenciacion\Geodatabase\planoteca_idesc_cat_obj_geo_202106\planoteca.gdb\PLANOTECA\\' #Path to GDB with DivPol and GriRef data
#***************************
# Start of processing
i = 0 #Start counter
R1List = sorted(arcpy.ListRasters(),reverse=True)
#R1List.sort(reverse=False)
print ("START OF [1/12] -------------> DESCRIBE RASTER SCRIPT!")
for r in R1List: #Describe feature file then get its property
    comp_type = arcpy.Describe(r).compressionType
    spa_ref = arcpy.Describe(r).spatialReference
    pix_type = arcpy.Raster(r).pixelType
    no_data = arcpy.Raster(r).noDataValue
    no_data_int = int(no_data)
    i += 1 #Sum one registry to counter
    print (str(i)+ "|"+ r.split(".")[0] + "|" + comp_type + "|" + spa_ref.name + "|" + pix_type + "|" + str(no_data_int))
print ("END OF -------> DESCRIBE RASTER SCRIPT!")

print ("START OF [2/12] -------------> RASTER SET NULL SCRIPT!")
in_false_raster = 1
clause = 'VALUE >= 255'
i = 0
for r1 in arcpy.ListRasters():
    out_raster = out_folder_a + r1[:-4] + 'ST' + '.tif'
    outSetNull = SetNull(r1, in_false_raster, clause) # Execute Set Null process
    outSetNull.save(out_raster) # Save the output
    i += 1
    print (str(i) + ' | Set Null done [1=Data; 0=No data] for: ' + r1[:-4]) # print arcpy.GetMessages()
print ("RASTER SET NULL ------------->  DONE!")

print ("START OF [3/12] -------------> BUILDING FOOTPRINTS FOR RASTER FILES SCRIPT!")
env.workspace = out_folder_a
raster_list = sorted(list(set(arcpy.ListFiles('*ST*')) & set(arcpy.ListFiles('*.tif'))),reverse=False) #Filtered list
print(str(len(raster_list)))
i = 0
for r1 in raster_list:
    out_geom = 'POLYGON' # output geometry type
    out_poly = out_folder_a + r1[:-6] + 'DI.shp'
    arcpy.RasterDomain_3d(r1, out_poly, out_geom)
    i += 1
    print(str(i) + ' | Creating footprint polygon done for: ' + r1[:-6])
print ("BUILDING FOOTPRINTS FOR RASTER FILES ------------->  DONE!")

""" for r1 in raster_list:
    out_poly = out_folder_a + r1[:-6] + "RD.shp"
    arcpy.RasterToPolygon_conversion(r1,out_poly,'NO_SIMPLIFY','VALUE') #Convert raster to polygon
feat_list1 = list(set(arcpy.ListFiles('*RD*')) & set(arcpy.ListFiles('*.shp'))) #Filtered list
feat_list1.sort(reverse=False)
for fc1 in feat_list1:
    out_feat = out_folder_a + fc1[:-6] + 'DI.shp'
    out_copy = out_folder_a + fc1[:-6] + 'CP.shp'
    out_temp = fc1[:-6] + 'LY.shp'
    LyrSql = '"gridcode" IN( 2 )' #SQL query for new shapefile
    arcpy.MakeFeatureLayer_management(fc1,out_temp,LyrSql) #Make temporary shapefile with selection
    arcpy.CopyFeatures_management(out_temp,out_copy) #Copy temporary layer to disk
    arcpy.Dissolve_management(out_copy,out_feat) #Dissolve converted files
    i += 1
    print(str(i) + ' | Creating footprint polygon done for: ' + fc1[:-6])
print ("BUILDING FOOTPRINTS FOR RASTER FILES ------------->  DONE!") """

print ("START OF [4/12] -------------> MINIMUM BOUNDING GEOMETRY FOR FEATURE CLASS SCRIPT!")
feat_list = sorted(list(set(arcpy.ListFiles('*DI*')) & set(arcpy.ListFiles('*.shp'))),reverse=False) #Filtered list
i = 0
for fc1 in feat_list:
    out_feat = out_folder_a + fc1[:-6] + 'MG.shp'
    MinGeoMethod = 'RECTANGLE_BY_AREA'#'CONVEX_HULL'#'RECTANGLE_BY_WIDTH' #Change MBG method (https://desktop.arcgis.com/en/arcmap/latest/tools/data-management-toolbox/minimum-bounding-geometry.htm)
    arcpy.MinimumBoundingGeometry_management(fc1, out_feat, MinGeoMethod, 'NONE') 
    i += 1
    print (str(i) +' | Minimum bounding rectangle done for: ' + fc1[:-6])
print ("MINIMUM BOUNDING AREA FOR FEATURE CLASS ------------->  DONE!")

print ("START OF [5/12] -------------> RASTER FILENAME TO ATTRIBUTE SCRIPT!")
i = 0
fc_list = sorted(arcpy.ListFeatureClasses('*MG*'),reverse=False)
filename = "SrcTif" #Field name to create
for fc2 in fc_list:
    name = fc2[:-4] # Get the shapefile's name without the extension
    arcpy.AddField_management(fc2, filename, 'TEXT','','', 50) # Add the field name to the shapefile
    with arcpy.da.UpdateCursor(fc2, filename) as cur: # Iterate over the rows, populating the source field with the shapefile name
        for row in cur:
            row[0] = name[:-2]
            cur.updateRow(row)
            i += 1
            print (str(i) +' | Raster filename to attribute done for: ' + fc2[:-6])
print ("RASTER FILENAME TO ATTRIBUTE ------------->  DONE!")

print ("START OF [6/12] -------------> MERGE OF FEATURE CLASSES SCRIPT!")
out_merge = out_folder_a + 'planoteca_' + RasterDate + '_poly' + 'ME.shp' #Merged file created name
arcpy.Merge_management(fc_list, out_merge) # Merge the shapefiles
print ("MERGE OF FEATURE CLASSES -------------> DONE!")

print ("START OF [7/12] -------------> CALCULATE GEOMETRY ATTRIBUTES (AREA M2) SCRIPT!")
arcpy.AddField_management(out_merge, "AreMt2", "DOUBLE") #Add field
arcpy.CalculateField_management(out_merge,"AreMt2","!shape.area@squaremeters!","PYTHON") #Calculate field
print ("CALCULATE GEOMETRY ATTRIBUTES (AREA M2) -------------> DONE!")

print ("START OF [8/12] -------------> CALCULATE CENTROID OF FEATURE CLASS SCRIPT!")
out_point_fc = out_folder_a + 'planoteca_' + RasterDate + '_point' + 'ME.shp'
arcpy.FeatureToPoint_management(out_merge, out_point_fc, "INSIDE") #Create centroid shapefile
print('1 | ' + str(out_point_fc[:-4]) + ' | Number of records: ' + str(arcpy.GetCount_management(out_point_fc)))
print ("CALCULATE CENTROID OF FEATURE CLASS -------------> DONE!")

print ("START OF [9/12] -------------> INTERSECTING SHAPEFILES SCRIPT!")
DivPol = GdbPath + 'pdt_pla_div_poli_admin'
GriRef = GdbPath + 'pdt_pla_grilla_rerefencia'
OutInter1 = out_folder_a + 'PntInter1' + 'int.shp'
OutInter2 = out_folder_a + 'PntInter2' + 'int.shp'
arcpy.Intersect_analysis([out_point_fc,DivPol],OutInter1) #Run the process for DivPol
arcpy.Intersect_analysis([OutInter1,GriRef],OutInter2) #Run the process for Divpol+GriRef
print('1 | ' + str(OutInter1[:-4]) + ' | Number of records: ' + str(arcpy.GetCount_management(OutInter1)))
print('2 | ' + str(OutInter2[:-4]) + ' | Number of records: ' + str(arcpy.GetCount_management(OutInter2)))
print ("INTERSECTING SHAPEFILES -------------> DONE!")

print ("START OF [10/12] -------------> FIELDS MANAGEMENT SCRIPT!")
arcpy.JoinField_management(out_merge,'SrcTif',OutInter2,'SrcTif') #Join all fields between shapefiles
FieldList = sorted(arcpy.ListFields(out_merge),reverse = False) #Filter fields to delete
FieLstOk = ['FID','Shape','SrcTif','AreMt2','IdComCorre','ComCorre','IdBarVer','BarVer','GrRef']
for fl in FieldList: #Type the name of the field you want to keep
    if fl.name not in FieLstOk:
        arcpy.DeleteField_management(out_merge,fl.name) #Delete field process
        print('Done deleting field: ' + fl.name)
    else:
        print('Field to keep: ' + fl.name)
print ("FIELDS MANAGEMENT -------------> DONE!")

print ("START OF [11/12] -------------> DISSOLVE GEOMETRY FOR FEATURE CLASS SCRIPT!")
out_dis = out_folder_a + 'planoteca_' + RasterDate + '_poly' + 'MEDI.shp' #Merged file created name
DisFields = ['SrcTif','IdComCorre','ComCorre','IdBarVer','BarVer','GrRef']
StaField = [['AreMt2','MAX']]
arcpy.Dissolve_management(out_merge, out_dis, DisFields, StaField) #Dissolve by fields with largest area part
print('1 | ' + str(out_dis[:-4]) + ' | Number of records: ' + str(arcpy.GetCount_management(out_dis)))
print("DISSOLVE GEOMETRY FOR FEATURE CLASS ------------->  DONE!")

print ("START OF [12/12] -------------> CLEANING FOLDER PROGRAM!")
DelFiles = arcpy.ListFiles('*') #List al files in workspace folder
DelFiles.sort(reverse=False)
for z in DelFiles:
    if 'polyMEDI' not in z and '.lock' not in z: #Create a filtered list of files to delete
        arcpy.Delete_management(z) #Process to delete files
        #print('Done deleting file: ' + z)
    else:
        print('File to keep: ' + z)
print ("CLEANING FOLDER -------------> DONE!")

print ("END OF PROGRAM [12/12]")
print('TOTAL PROCESSED RASTER FILES: ' + str(len(R1List)))
NumRows = arcpy.GetCount_management(out_dis)
print('1 | ' + out_dis.split('.')[0] + ' | Number of records: ' + str(NumRows))
END = int((time.clock()-START)/60) #Process timer set to minutes
print("SCRIPT RUNNING TIME -------> {} MINUTES".format(END))