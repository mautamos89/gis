# Batch processing of tools needed for satellite imagery spectral index calculation and area discrimination by defined ranges.
# Requirements: License: Spatial Analyst; Raster: SENTINEL2 imagery with atmospheric correction and cloudless; Shapefile: Study area
# Author: Mauricio Tabares Mosquera, Geographer, GIS Specialist
# Date: 20220405

# Import necessary system modules
import arcpy,os,time
from arcpy import env
from arcpy.sa import *
from collections import defaultdict as dd

# Set ArcPy script environmental settings
START = time.clock()
arcpy.env.overwriteOutput = True
arcpy.env.parallelProcessingFactor = "0"

arcpy.AddMessage ("SET SCRIPT MODULES DONE!")

# Folder where raster files are located.  
RasFolder = arcpy.GetParameterAsText(0) #Folder where satellite imagery is located. # PARAMETER!!
ShpFolder = arcpy.GetParameterAsText(5) #Folder where study area is located. # PARAMETER!!
OutputFolder = arcpy.CreateFolder_management(RasFolder, 'Spectral_Index_Geoprocessing [Output]').getOutput(0) # arcpy.GetParameterAsText(6) #Folder where files will be saved. # PARAMETER!!
arcpy.env.workspace = OutputFolder
arcpy.CheckOutExtension('Spatial')

arcpy.AddMessage ('RASTER FOLDER: ' + str(RasFolder))
arcpy.AddMessage ('SHAPEFILE FOLDER: ' + str(ShpFolder))
arcpy.AddMessage ('OUTPUT FOLDER: ' + str(OutputFolder))

# Location where output files will be saved.
FolderScript1 = OutputFolder
FolderOutClipStudyArea = arcpy.CreateFolder_management(FolderScript1, 'C_Sentinel_Imagery [Raster]').getOutput(0)
FolderOutSpecIndex = arcpy.CreateFolder_management(FolderScript1, 'B_Spectral_Index_Calculation [Raster]').getOutput(0)
FolderOutReclass = arcpy.CreateFolder_management(FolderScript1, 'Temp_Files [For Script2]').getOutput(0)
FolderOutDis = arcpy.CreateFolder_management(FolderScript1, 'A_Spectral_Index_Calculation [Shapefile]').getOutput(0)

arcpy.AddMessage ("SET SCRIPT FOLDERS DONE!")

OldRaster = arcpy.GetParameterAsText(3)
RecentRaster = arcpy.GetParameterAsText(4)

# Set reclassification custom mapping for spectral index.
RemapNdvi = arcpy.GetParameterAsText(8)
RemapSavi = arcpy.GetParameterAsText(9)
RemapMndwi = arcpy.GetParameterAsText(10)
RemapNdti = arcpy.GetParameterAsText(11)

# Set the cell size for raster resampling
CellSize = arcpy.GetParameterAsText(1) #'10' # PARAMETER!!

# Set the resampling technique to be used
ResType = arcpy.GetParameterAsText(2)

# Set the buffer distance for image clipping
BufDistance = arcpy.GetParameterAsText(6) #'100 Meters' # PARAMETER!!

# Set the Minimum Mapping Unit (MMU) for vector data production
MMU = arcpy.GetParameterAsText(7) #'5000 Meters Sentinel-2 10Mt pixel = 1:15k; 10000 Meters Sentinel-2 20Mt pixel = 1:25k' # PARAMETER!!

# Set bands order for spectral index estimation - SENTINEL 2
B1 = '1' #  Aerosol
B2 = '2' #  Blue
B3 = '3' #  Green
B4 = '4' #  Red
B5 = '5' #  Red edge 1
B6 = '6' #  Red edge 2
B7 = '7' #  Red edge 3
B8 = '8' #  Near infrared (NIR) 1
B9 = '9' #  Near infrared (NIR) 2
B10 = '10' #  Water vapour
B11 = '11' #  Cirrus
B12 = '12' #  Short wave infrared (SWIR) 1
B13 = '13' #  Short wave infrared (SWIR) 2

# Set bands filename for spectral index estimation - SENTINEL 2
FileB1 = r'\Band_' + str(B1) + '.tif' #  Aerosol
FileB2 = r'\Band_' + str(B2) + '.tif' #  Blue
FileB3 = r'\Band_' + str(B3) + '.tif' #  Green
FileB4 = r'\Band_' + str(B4) + '.tif' #  Red
FileB5 = r'\Band_' + str(B5) + '.tif' #  Red edge 1
FileB6 = r'\Band_' + str(B6) + '.tif' #  Red edge 2
FileB7 = r'\Band_' + str(B7) + '.tif' #  Red edge 3
FileB8 = r'\Band_' + str(B8) + '.tif' #  Near infrared (NIR) 1
FileB9 = r'\Band_' + str(B9) + '.tif' #  Near infrared (NIR) 2
FileB10 = r'\Band_' + str(B10) + '.tif' #  Water vapour
FileB11 = r'\Band_' + str(B11) + '.tif' #  Cirrus
FileB12 = r'\Band_' + str(B12) + '.tif' #  Short wave infrared (SWIR) 1
FileB13 = r'\Band_' + str(B13) + '.tif' #  Short wave infrared (SWIR) 2

arcpy.AddMessage ('CHANGE DETECTION PARAMETERS: [OLDEST RASTER DATE: ' + str(OldRaster) + '|' + 'MOST RECENT RASTER DATE: ' + str(RecentRaster) + ']')
arcpy.AddMessage ('PARAMETERS [RESAMPLING CELL & TYPE: ' + str(CellSize) + 'MT--' + str(ResType) + '|' + 'BUFFER: ' + str(BufDistance) + 'MT' + '|' + 'MMU: ' + str(MMU) + 'MT2]')
arcpy.AddMessage ('REMAP VALUES NDVI: [' + str(RemapNdvi) + ']' + '--' + 'REMAP VALUES SAVI: [' + str(RemapSavi) + ']' + '--' + 'REMAP VALUES MNDWI: [' + str(RemapMndwi) + ']' + '--' + 'REMAP VALUES NDTI: [' + str(RemapNdti) + ']')
arcpy.AddMessage ("SET SCRIPT PARAMETERS DONE!")
arcpy.AddMessage ("START OF -------> SRIPT [1/2]: SPECTRAL INDEX GEOPROCESSING SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: DESCRIBE RASTER FILES SCRIPT!")
 
arcpy.env.workspace = RasFolder
RasterList = arcpy.ListDatasets('*.tif','Raster') # Filter raster files with .tif extension
RasterList.sort(reverse=False)
for a1 in RasterList:
    BandNumber = arcpy.Describe(a1).bandCount
    comp_type = arcpy.Describe(a1).compressionType
    spa_ref = arcpy.Describe(a1).spatialReference
    pix_type = arcpy.Raster(a1).pixelType
    no_data = arcpy.Raster(a1).noDataValue
    no_data_int = int(no_data)
    arcpy.AddMessage ('FILE: ' + (a1)[:-4] + '|' + 'BAND COUNT: ' + str(BandNumber) + '|' + 'COMPRESSION: ' + comp_type + '|' + 'SPATIALREF: ' + spa_ref.name + "|" + 'PIXEL TYPE: ' + pix_type + '|' + 'NO DATA VALUE: ' + str(no_data_int))

arcpy.AddMessage ("END OF -------> DESCRIBE RASTER FILES SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: DESCRIBE VECTOR FILES SCRIPT!")

arcpy.env.workspace = ShpFolder
VectorList = arcpy.ListFiles('*.shp') # Filter files with .shp extension
for a2 in VectorList:
    ShapeType = arcpy.Describe(a2).shapeType
    FeatureType = arcpy.Describe(a2).featureType
    SpatialIndex = arcpy.Describe(a2).hasSpatialIndex
    arcpy.AddMessage ('FILE: ' + (a2)[:-4] + '|' + 'GEOMETRY: ' + ShapeType + '|' + 'TYPE: ' + FeatureType + '|' + 'INDEX: ' +  str(SpatialIndex))

arcpy.AddMessage ("END OF -------> DESCRIBE VECTOR FILES SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: BUFFER AREA FOR BOUNDARY SCRIPT!")

VectorList = arcpy.ListFiles('*.shp') # Study area shapefile.
for a3 in VectorList:
    FileBuf = 'Buf' + a3[:-4] + '.shp'
    OutBuf = os.path.join(OutputFolder, FileBuf)
    arcpy.Buffer_analysis(a3, OutBuf, BufDistance, 'FULL', 'ROUND', 'NONE', '')
    arcpy.AddMessage (("BUFFER AREA DONE FOR: ") + a3)

arcpy.AddMessage ("END OF -------> BUFFER AREA FOR BOUNDARY SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: CLIP RASTER TO BOUNDARY AREA SCRIPT!")

arcpy.env.workspace = OutputFolder # Make temporary vector layer with FID
VectorListClip = list(set(arcpy.ListFiles('Buf*')) & set(arcpy.ListFiles('*.shp')))
for ShpClip in VectorListClip:
    arcpy.MakeFeatureLayer_management(ShpClip, 'BufLyr') # Make a Feature Layer for the original shapefile
    FIDNumbers = [] # Create an empty list to hold the FID numbers
    with arcpy.da.SearchCursor('BufLyr', ["FID"]) as cursor: # First, loop through the original layer and get all the FID numbers.
        for row in cursor:
            FIDNumbers.append(row[0])
    for FID in FIDNumbers: # Then create a layer for each FID and export it out
        arcpy.MakeFeatureLayer_management('BufLyr', "TempLyr{0}".format(FID), "\"FID\" = {0}".format(FID))
        FileFID = 'Clip_' + ShpClip[3:-4] + '_FID{0}.shp'.format(FID)
        OutFID = os.path.join(OutputFolder, FileFID)
        arcpy.CopyFeatures_management("TempLyr{0}".format(FID), OutFID)
        arcpy.AddMessage (("TEMP VECTOR LAYER CREATED FOR: ") + ShpClip[:-4] + ' FID: ' + ('{0}.shp'.format(FID)[:-4]))

# Clip rasters with temporary vector layer
VectorListClip1 = list(set(arcpy.ListFiles('Clip*')) & set(arcpy.ListFiles('*.shp')))
VectorListClip1.sort(reverse=False)
for RClip in RasterList:
    for Vec in VectorListClip1:
        FileVec = Vec.split('_')[1] + '_' + Vec.split('_')[2]
        FileClip = "RT" + RClip[7:-11] + '_' + str(FileVec)[0:-4] + '.tif'
        OutClip = os.path.join(FolderOutClipStudyArea, FileClip)
        arcpy.Clip_management(os.path.join(str(RasFolder), RClip), '', OutClip, Vec, '0', 'ClippingGeometry') #clip based on layer, clipping geometry will use the polygon extent only
        arcpy.AddMessage (("CLIP STUDY AREA DONE FOR: ") + str(RClip) +  " FEATURE: " + str(Vec))

arcpy.AddMessage ("END OF -------> CLIP RASTER SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: RESAMPLING RASTER PIXEL SIZE: " + str(CellSize) + "MT!")

arcpy.env.workspace = FolderOutClipStudyArea
RasterListRes = arcpy.ListDatasets("*.tif","Raster")
for b1 in RasterListRes:
    FileRes = 'Res' + str(b1)[2:-4] + '.tif'
    OutRes = os.path.join(OutputFolder, FileRes)
    ResRaster = arcpy.Resample_management(b1, OutRes, CellSize, ResType)
    arcpy.AddMessage (("RESAMPLING RASTER DONE FOR: ") + b1)

arcpy.AddMessage ("END OF -------> RESAMPLING RASTER PIXEL SIZE: " + str(CellSize) + "MT SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: MAP ALGEBRA: INDEX - VEGETATION SCRIPT!") # INDEX CLASS
arcpy.AddMessage ("START OF -------> STAGE: MAP ALGEBRA: NDVI SCRIPT!") # NORMALIZED DIFFERENCE VEGETATION INDEX (NDVI)

arcpy.env.workspace = OutputFolder
RasterListSpecIndex = arcpy.ListDatasets('Res*',"Raster")
for c1a in RasterListSpecIndex:
    Red = arcpy.MakeRasterLayer_management(c1a, os.path.join(str(FolderScript1), str(FileB4)), '', '', B4) # Number of the band needed for index calculation
    Nir = arcpy.MakeRasterLayer_management(c1a, os.path.join(str(FolderScript1), str(FileB8)), '', '', B8) # Number of the band needed for index calculation
    RasterRed = arcpy.Raster(os.path.join(str(FolderScript1), str(FileB4))) # Filename of the temporal file to save the band as raster
    RasterNir = arcpy.Raster(os.path.join(str(FolderScript1), str(FileB8))) # Filename of the temporal file to save the band as raster
    FileNdvi = 'Ndvi' + str(c1a)[3:-4] + '.tif'
    OutNdvi = os.path.join(str(FolderOutSpecIndex), str(FileNdvi))
    Ndvi = (Float(RasterNir) - Float(RasterRed)) / (Float(RasterNir) + Float(RasterRed))
    Ndvi.save(OutNdvi)
    arcpy.AddMessage (("NDVI MAP ALGEBRA DONE FOR: ") + c1a)

arcpy.AddMessage ("END OF -------> MAP ALGEBRA: NDVI SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: MAP ALGEBRA: SAVI SCRIPT!") # SOIL ADJUSTED VEGETATION INDEX (SAVI)

for c1e in RasterListSpecIndex:
    Red = arcpy.MakeRasterLayer_management(c1e, os.path.join(str(FolderScript1), str(FileB4)), '', '', B4) # Number of the band needed for index calculation
    Nir = arcpy.MakeRasterLayer_management(c1e, os.path.join(str(FolderScript1), str(FileB8)), '', '', B8) # Number of the band needed for index calculation
    RasterRed = arcpy.Raster(os.path.join(str(FolderScript1), str(FileB4))) # Filename of the temporal file to save the band as raster
    RasterNir = arcpy.Raster(os.path.join(str(FolderScript1), str(FileB8))) # Filename of the temporal file to save the band as raster
    FileSavi = 'Savi' + str(c1e)[3:-4] + '.tif'
    OutSavi = os.path.join(str(FolderOutSpecIndex), str(FileSavi))
    Savi = (Float(RasterNir) - Float(RasterRed)) / ((Float(RasterNir) + Float(RasterRed) + 0.5) * 1.5)
    Savi.save(OutSavi)
    arcpy.AddMessage (("SAVI MAP ALGEBRA DONE FOR: ") + c1e)

arcpy.AddMessage ("END OF -------> MAP ALGEBRA: SAVI SCRIPT!")
arcpy.AddMessage ("END OF -------> STAGE: MAP ALGEBRA: INDEX - VEGETATION SCRIPT!")

arcpy.AddMessage ("START OF -------> STAGE: MAP ALGEBRA: INDEX - WATER SCRIPT!") # INDEX CLASS
arcpy.AddMessage ("START OF -------> STAGE: MAP ALGEBRA: MNDWI SCRIPT!") # MODIFIED NORMALIZED DIFFERENCE WATER INDEX (MNDWI)

for c2b in RasterListSpecIndex:
    Green = arcpy.MakeRasterLayer_management(c2b, os.path.join(str(FolderScript1), str(FileB3)), '', '', B3) # Number of the band needed for index calculation
    Swir1 = arcpy.MakeRasterLayer_management(c2b, os.path.join(str(FolderScript1), str(FileB12)), '', '', B12) # Number of the band needed for index calculation
    RasterGreen = arcpy.Raster(os.path.join(str(FolderScript1), str(FileB3))) # Filename of the temporal file to save the band as raster
    RasterSwir1 = arcpy.Raster(os.path.join(str(FolderScript1), str(FileB12))) # Filename of the temporal file to save the band as raster
    FileMndwi = 'Mndwi' + str(c2b)[3:-4] + '.tif'
    OutMndwi = os.path.join(str(FolderOutSpecIndex), str(FileMndwi))
    Mndwi = (Float(RasterGreen) - Float(RasterSwir1)) / (Float(RasterGreen) + Float(RasterSwir1))
    Mndwi.save(OutMndwi)
    arcpy.AddMessage (("MNDWI MAP ALGEBRA DONE FOR: ") + c2b)

arcpy.AddMessage ("END OF -------> MAP ALGEBRA: MNDWI SCRIPT!")
arcpy.AddMessage ("END OF -------> MAP ALGEBRA: INDEX - WATER SCRIPT!")

arcpy.AddMessage ("START OF -------> STAGE: MAP ALGEBRA: INDEX - LANDSCAPE SCRIPT!") # INDEX CLASS
arcpy.AddMessage ("START OF -------> STAGE: MAP ALGEBRA: NDTI SCRIPT!") # NORMALIZED DIFFERENCE TILLAGE INDEX (NDTI)

for c3d in RasterListSpecIndex:
    Swir1 = arcpy.MakeRasterLayer_management(c3d, os.path.join(str(FolderScript1), str(FileB12)), '', '', B12) # Number of the band needed for index calculation
    Swir2 = arcpy.MakeRasterLayer_management(c3d, os.path.join(str(FolderScript1), str(FileB13)), '', '', B13) # Number of the band needed for index calculation
    RasterSwir1 = arcpy.Raster(os.path.join(str(FolderScript1), str(FileB12))) # Filename of the temporal file to save the band as raster
    RasterSwir2 = arcpy.Raster(os.path.join(str(FolderScript1), str(FileB13))) # Filename of the temporal file to save the band as raster
    FileNdti = 'Ndti' + str(c3d)[3:-4] + '.tif'
    OutNdti = os.path.join(str(FolderOutSpecIndex), str(FileNdti))
    Ndti = (Float(RasterSwir1) - Float(RasterSwir2)) / (Float(RasterSwir1) + Float(RasterSwir2))
    Ndti.save(OutNdti)
    arcpy.AddMessage (("NDTI MAP ALGEBRA DONE FOR: ") + c3d)

arcpy.AddMessage ("END OF -------> MAP ALGEBRA: NDTI SCRIPT!")
arcpy.AddMessage ("END OF -------> MAP ALGEBRA: INDEX - LANDSCAPE SCRIPT!")

arcpy.AddMessage ("START OF -------> STAGE: RECLASSIFY SCRIPT!")
# Execute Reclassify
arcpy.env.workspace = FolderOutSpecIndex
RasterListRecNdvi = arcpy.ListRasters('Ndvi*')
for e1a in RasterListRecNdvi:
    RecRaster = Reclassify(e1a, 'VALUE', RemapNdvi, "NODATA")
    FileRec = 'Rec' + str(e1a)[:-4] + '.tif'
    OutRec = os.path.join(FolderOutReclass, FileRec)
    RecRaster.save(OutRec)
    arcpy.AddMessage (("RECLASSIFY DONE FOR: ") + e1a)
# Execute Reclassify
RasterListRecSavi = arcpy.ListRasters('Savi*')
for e1e in RasterListRecSavi:
    RecRaster = Reclassify(e1e, 'VALUE', RemapSavi, "NODATA")
    FileRec = 'Rec' + str(e1e)[:-4] + '.tif'
    OutRec = os.path.join(FolderOutReclass, FileRec)
    RecRaster.save(OutRec)
    arcpy.AddMessage (("RECLASSIFY DONE FOR: ") + e1e)
# Execute Reclassify
RasterListRecMndwi = arcpy.ListRasters('Mndwi*')
for e1g in RasterListRecMndwi:
    RecRaster = Reclassify(e1g, 'VALUE', RemapMndwi, "NODATA")
    FileRec = 'Rec' + str(e1g)[:-4] + '.tif'
    OutRec = os.path.join(FolderOutReclass, FileRec)
    RecRaster.save(OutRec)
    arcpy.AddMessage (("RECLASSIFY DONE FOR: ") + e1g)
# Execute Reclassify
RasterListRecNdti = arcpy.ListRasters('Ndti*')
for e1j in RasterListRecNdti:
    RecRaster = Reclassify(e1j, 'VALUE', RemapNdti, "NODATA")
    FileRec = 'Rec' + str(e1j)[:-4] + '.tif'
    OutRec = os.path.join(FolderOutReclass, FileRec)
    RecRaster.save(OutRec)
    arcpy.AddMessage (("RECLASSIFY DONE FOR: ") + e1j)

arcpy.AddMessage ("END OF -------> RECLASSIFY SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: RASTER TO POLYGON CONVERSION SCRIPT!")
# Convert raster to polygon
arcpy.env.workspace = FolderOutReclass
RasterListArea = arcpy.ListRasters()
for e2 in RasterListArea:
    FileRasPol = 'Vec' + str(e2)[3:-4] + '.shp'
    OutRasPol = os.path.join(FolderOutReclass, FileRasPol)
    RasPolField = 'Value'
    arcpy.RasterToPolygon_conversion(e2, OutRasPol, "NO_SIMPLIFY", RasPolField)
    arcpy.AddMessage (("RASTER TO POLYGON DONE FOR: ") + e2)
# Calculate area field
VectorListArea1 = arcpy.ListFiles("*.shp")
for e7 in VectorListArea1:
    arcpy.AddField_management(e7, 'AreaMt2', 'FLOAT')
    with arcpy.da.UpdateCursor(e7, ('AreaMt2', 'SHAPE@')) as ShpCur00:
        for row in ShpCur00:
            row[0] = row[1].getArea('GEODESIC', 'SQUAREMETERS')
            ShpCur00.updateRow(row)

arcpy.AddMessage ("END OF -------> RASTER TO POLYGON CONVERSION SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: SET AND ELIMINATE POLYGONS BY MINIMAL MAPPING UNIT: " + str(MMU) + 'MT2 SCRIPT!')
# Set and eliminate polygons by MMU
Mmu1List = arcpy.ListFeatureClasses('*.shp')
for e5 in Mmu1List:
    FileMmu1 = 'Mmu1' + str(e5)[3:-4] + '.shp'
    OutMmu1 = os.path.join(OutputFolder, FileMmu1)
    FileMmu1Temp = str(e5) + 'Temp'
    arcpy.MakeFeatureLayer_management(e5, FileMmu1Temp)
    arcpy.SelectLayerByAttribute_management(FileMmu1Temp, 'NEW_SELECTION', '"AreaMt2" < ' + MMU)
    arcpy.Eliminate_management(FileMmu1Temp, OutMmu1, "LENGTH", '')
# MMU2
arcpy.env.workspace = OutputFolder
Mmu2List = arcpy.ListFeatureClasses('Mmu1*')
for e6 in Mmu2List:
    FileMmu2 = 'Mmu2' + str(e6)[4:-4] + '.shp'
    OutMmu2 = os.path.join(OutputFolder, FileMmu2)
    FileMmu2Temp = str(e6) + 'Temp'
    arcpy.MakeFeatureLayer_management(e6, FileMmu2Temp)
    arcpy.SelectLayerByAttribute_management(FileMmu2Temp, 'NEW_SELECTION', '"AreaMt2" < ' + MMU)
    arcpy.Eliminate_management(FileMmu2Temp, OutMmu2, "LENGTH", '')
    arcpy.AddMessage ("POLYGON ELIMINATE BY MMU DONE FOR: " + e6)
# Dissolve polygon by class
VectorListDis = arcpy.ListFeatureClasses('Mmu2*')
for e3 in VectorListDis:
    FileDis = str(e3)[4:-4] + '.shp'
    OutDis = os.path.join(FolderOutDis, FileDis)
    arcpy.Dissolve_management(e3, OutDis, 'gridcode', '', 'MULTI_PART', 'DISSOLVE_LINES')

arcpy.AddMessage ("END OF -------> SET AND ELIMINATE POLYGONS BY MINIMAL MAPPING UNIT: " + str(MMU) + "MT2 SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: CREATE FIELDS AND CALCULATE ATTRIBUTES SCRIPT!")
# Calculate fields
arcpy.env.workspace = FolderOutDis
VectorListArea = list(set(arcpy.ListFeatureClasses()) - set(arcpy.ListFeatureClasses('Merge*')))
VectorListArea.sort(reverse=False)
for e4 in VectorListArea:
    arcpy.AddField_management(e4, 'SpecInd', 'TEXT', '', '', 10)
    arcpy.AddField_management(e4, 'ImgDate', 'TEXT', '', '', 10)
    arcpy.AddField_management(e4, 'RemVal', 'SHORT')
    arcpy.AddField_management(e4, 'Legend', 'TEXT', '', '', 60)
    arcpy.AddField_management(e4, 'AreaMt2', 'DOUBLE')
    arcpy.AddField_management(e4, 'AreaHa', 'FLOAT')
    arcpy.AddField_management(e4, 'AreaKm2', 'FLOAT')
    arcpy.AddField_management(e4, 'AreaPercen', 'FLOAT')
    arcpy.AddField_management(e4, 'SrcShpFID', 'LONG')
    arcpy.CalculateField_management(e4,'RemVal','!gridcode!','PYTHON')
    arcpy.DeleteField_management(e4, 'gridcode')
    with arcpy.da.UpdateCursor(e4, ('AreaMt2', 'AreaHa', 'AreaKm2', 'SHAPE@')) as ShpCur0:
        for row in ShpCur0:
            row[0], row[1], row[2] = [row[3].getArea('GEODESIC', 'SQUAREMETERS'), row[3].getArea('GEODESIC', 'HECTARES'), row[3].getArea('GEODESIC', 'SQUAREKILOMETERS')]
            ShpCur0.updateRow(row)
    SumTotal = float(sum(row[0] for row in arcpy.da.SearchCursor(e4, 'SHAPE@AREA')))
    with arcpy.da.UpdateCursor(e4, ('SHAPE@AREA', 'AreaPercen')) as uCursor:
        for Area, Percent in uCursor:
            uCursor.updateRow([Area, (Area / SumTotal) * 100])
    ShpFID = (e4.split('_')[2])[3:-4]
    SpecInd = (e4.split('_')[0])[:-8]
    ImgDate = (e4.split('_')[0])[-8:]
    with arcpy.da.UpdateCursor(e4, ('SrcShpFID', 'SpecInd', 'ImgDate')) as ShpCur1:
        for row in ShpCur1:
            row[0], row[1], row[2] = [ShpFID, SpecInd, ImgDate]
            ShpCur1.updateRow(row)
    arcpy.AddMessage (("CALCULATE AREA & SOURCE ATTRIBUTES DONE FOR: ") + e4)
# Calculate legend field vegetation
LegListVege = list(set(arcpy.ListFeatureClasses('Ndvi*')) | set(arcpy.ListFeatureClasses('Savi*')))
LegListVege.sort(reverse=False)
for e8 in LegListVege:
    with arcpy.da.UpdateCursor(e8, ('RemVal', 'Legend')) as tCursor:
        for value in tCursor:
            if value[0] == 0:
               value[1] = 'Non-vegetation'
            if value[0] == 1:
               value[1] = 'Shrub and grassland / Crop earliest season'
            if value[0] == 2:
               value[1] = 'Temperate and tropical rainforest / Crop mid-late season'
            tCursor.updateRow(value)
        arcpy.AddMessage (("CALCULATE LEGEND ATTRIBUTES DONE FOR: ") + e8)
# Calculate legend field water
LegListWater = arcpy.ListFeatureClasses('Mndwi*')
LegListWater.sort(reverse=False)
for e9 in LegListWater:
    with arcpy.da.UpdateCursor(e9, ('RemVal', 'Legend')) as xCursor:
        for value1 in xCursor:
            if value1[0] == 0:
               value1[1] = 'Non-water'
            if value1[0] == 1:
               value1[1] = 'Water bodies'
            xCursor.updateRow(value1)
        arcpy.AddMessage (("CALCULATE LEGEND ATTRIBUTES DONE FOR: ") + e9)
# Calculate legend field built-up
LegListBuilt = arcpy.ListFeatureClasses('Ndti*')
LegListBuilt.sort(reverse=False)
for e10 in LegListBuilt:
    with arcpy.da.UpdateCursor(e10, ('RemVal', 'Legend')) as yCursor:
        for value2 in yCursor:
            if value2[0] == 0:
               value2[1] = 'Non-built'
            if value2[0] == 1:
               value2[1] = 'Built-up'
            yCursor.updateRow(value2)
        arcpy.AddMessage (("CALCULATE LEGEND ATTRIBUTES DONE FOR: ") + e10)

arcpy.AddMessage ("END OF -------> CREATE FIELDS AND CALCULATE ATTRIBUTES SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: GROUP AND MERGE SHAPEFILE BY NAME SCRIPT!")
# Group and merge by shapefile name
Dic = dd(list)
for Item in os.listdir(FolderOutDis):
    FileItem = Item.split('_')[1]
    if os.path.isfile(os.path.join(FolderOutDis,Item)) and Item.endswith('.shp') and not Item.startswith('Merge'):
        Dic[FileItem].append(os.path.join(FolderOutDis, Item))
for group, mergelist in Dic.items():
    arcpy.AddMessage ('GROUP SET FOR: '+ str(group))
    arcpy.Merge_management(inputs=mergelist, output=os.path.join(FolderOutDis, 'MergeCal_{}.shp'.format(group)))

arcpy.AddMessage ("END OF -------> GROUP AND MERGE SHAPEFILE BY NAME SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: JOIN FIELD WITH SOURCE SHAPEFILE SCRIPT!")
# Join fields with source shapefile
FolderA = ShpFolder
FolderB = FolderOutDis
env.workspace = FolderA
FolderAList = arcpy.ListFeatureClasses() # LIST INPUT SHAPEFILES
env.workspace = FolderB
FolderBList = arcpy.ListFeatureClasses('Merge*') # LIST MERGED SHAPEFILES
for FileA, FileB in zip(FolderAList, FolderBList):
    arcpy.JoinField_management((os.path.join(str(FolderB), str(FileB))), 'SrcShpFID', (os.path.join(str(FolderA), str(FileA))), 'FID')
    arcpy.DeleteField_management(FileB, 'SrcShpFID')
    arcpy.AddMessage ('FIELDS JOINED FOR: ' + '[' + str(FileA)[:-4] + ' & ' + str(FileB)[:-4] + ']')

arcpy.AddMessage ("END OF -------> JOIN FIELD WITH SOURCE SHAPEFILE SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: WORKSPACE FOLDER CLEANUP SCRIPT!")
# Workspace folder cleanup
arcpy.env.workspace = OutputFolder
DataDel = list(set(arcpy.ListFeatureClasses()) | set(arcpy.ListDatasets('*.tif','Raster')))
DataDel.sort(reverse=False)
for del0 in DataDel:
    arcpy.Delete_management(del0)
    arcpy.AddMessage (('DELETING TEMP FILE: ') + str(del0))
arcpy.env.workspace = FolderOutReclass
DataDel1 = arcpy.ListFeatureClasses()
DataDel1.sort(reverse=False)
for del1 in DataDel1:
    arcpy.Delete_management(del1)
    arcpy.AddMessage (('DELETING TEMP FILE: ') + str(del1))
arcpy.env.workspace = FolderOutDis
MergeDelList = list(set(arcpy.ListFeatureClasses()) - set(arcpy.ListFeatureClasses('Merge*')))
MergeDelList.sort(reverse=False)
for del2 in MergeDelList:
    arcpy.Delete_management(del2)
    arcpy.AddMessage (('DELETING TEMP FILE: ') + str(del2))

arcpy.AddMessage ("END OF -------> WORKSPACE FOLDER CLEANUP SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: GENERATE EXCEL REPORT SCRIPT!")
# Generate Excel report with merged shapefiles
arcpy.env.workspace = FolderOutDis
ExcelList = arcpy.ListFeatureClasses()
for ExFile in ExcelList:
    ExFilename = 'A_Spectral_Index_Calculation [' + (ExFile.split('_')[1])[:-4] + ']' + '.xls'
    arcpy.TableToExcel_conversion(ExFile, os.path.join(OutputFolder, ExFilename))
    arcpy.AddMessage(('EXCEL REPORT DONE FOR: ') + str(ExFilename))

arcpy.AddMessage ("END OF -------> GENERATE EXCEL REPORT SCRIPT!")
arcpy.AddMessage ("END OF -------> SRIPT [1/2]: SPECTRAL INDEX GEOPROCESSING SCRIPT!")
END = (time.clock()-START)
arcpy.AddMessage ("SCRIPT RUNNING TIME -------> {} SECONDS".format(END))

#===================================================================================================================================#
#                                               SPECTRAL INDEX CHANGE DETECTION SCRIPT!                                             #
#===================================================================================================================================#

arcpy.AddMessage ("START OF -------> SRIPT [2/2]: SPECTRAL INDEX CHANGE DETECTION SCRIPT!")
START1 = time.clock()
FolderOutSc1 = arcpy.CreateFolder_management(RasFolder, 'Spectral_Index_Geoprocessing [Output]').getOutput(0)
arcpy.env.workspace = RasFolder

arcpy.AddMessage ('WORKSPACE FOLDER: ' + str(RasFolder))
# Location where output files will be saved
FolderScript1a = FolderOutSc1
FolderOutConDis = arcpy.CreateFolder_management(FolderScript1a, 'D_Spectral_Index_Change_Detection [Shapefile]').getOutput(0)
arcpy.AddMessage ("SET SCRIPT FOLDERS DONE!")
arcpy.AddMessage ("START OF -------> STAGE: MAP ALGEBRA CHANGE DETECTION SCRIPT!")

Folder1 = FolderOutReclass
Folder2 = FolderOutReclass
# Creating raster lists with oldest and most recent files
env.workspace = Folder1
Folder1List = arcpy.ListRasters('*' + OldRaster + '*') # OLDEST RASTER FOR SPECTRAL INDEX COMPARISON # PARAMETER!!
env.workspace = Folder2
Folder2List = arcpy.ListRasters('*' + RecentRaster + '*') # MOST RECENT RASTER FOR SPECTRAL INDEX COMPARISON # PARAMETER!!
arcpy.AddMessage ('CHANGE DETECTION PARAMETERS: [OLDEST RASTER DATE: ' + str(OldRaster) + '|' + 'MOST RECENT RASTER DATE: ' + str(RecentRaster) + ']')
# Map algebra loop with tuplets with oldest and most recent files
for File1, File2 in zip(Folder1List, Folder2List):
    FileRasterCon = 'RCon' + str(File1)[:-4] + '.tif'
    OutRasterCon = os.path.join(FolderOutSc1, FileRasterCon)
    RasterCon = Con(Raster(os.path.join(str(Folder2), str(File2))) > Raster(os.path.join(str(Folder1), str(File1))), 2, Con(Raster(os.path.join(str(Folder2), str(File2))) == Raster(os.path.join(str(Folder1), str(File1))), 1, 0)) # LEYEND RECENT TO EARLIEST: 0, PERDIÓ; 1, IGUAL; 2, GANÓ -- InRasNew > InRasOld, 3, Con(InRasNew == InRasOld, 2, 1))
    RasterCon.save(OutRasterCon)
    arcpy.AddMessage ('MAP ALGEBRA CHANGE DETECTION DONE FOR: ' + '[' + str(File2)[3:-4] + ' - ' + str(File1)[3:-4] + ']')

arcpy.AddMessage ("END OF -------> MAP ALGEBRA CHANGE DETECTION SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: RASTER TO POLYGON CONVERSION SCRIPT!")
# Convert raster to polygon
arcpy.env.workspace = FolderOutSc1
RasterListArea1 = arcpy.ListRasters('RCon*') # MUST CHANGE AS TEXT PARAMETER
for e2a in RasterListArea1:
    FileRasPol1 = 'Vec' + str(e2a)[4:-4] + '.shp'
    OutRasPol1 = os.path.join(FolderOutSc1, FileRasPol1)
    RasPolField1 = 'Value'
    arcpy.RasterToPolygon_conversion(e2a, OutRasPol1, "NO_SIMPLIFY", RasPolField1)
    arcpy.AddMessage ("RASTER TO POLYGON DONE FOR: " + e2a)
# Calculate area field
VectorListArea1a = list(set(arcpy.ListFiles('Vec*')) & set(arcpy.ListFiles('*.shp')))
for e7a in VectorListArea1a:
    arcpy.AddField_management(e7a, 'AreaMt2', 'FLOAT')
    with arcpy.da.UpdateCursor(e7a, ('AreaMt2', 'SHAPE@')) as ShpCur00a:
        for row in ShpCur00a:
            row[0] = row[1].getArea('GEODESIC', 'SQUAREMETERS')
            ShpCur00a.updateRow(row)

arcpy.AddMessage ("END OF -------> RASTER TO POLYGON CONVERSION SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: SET AND ELIMINATE POLYGONS BY MINIMAL MAPPING UNIT: " + str(MMU) + 'MT2 SCRIPT!')
# Set and eliminate polygons by MMU
Mmu1Lista = arcpy.ListFeatureClasses('*.shp')
for e5a in Mmu1Lista:
    FileMmu1a = 'Mmu1' + str(e5a)[3:-4] + '.shp'
    OutMmu1a = os.path.join(FolderOutSc1, FileMmu1a)
    FileMmu1Tempa = str(e5a) + 'Temp'
    arcpy.MakeFeatureLayer_management(e5a, FileMmu1Tempa)
    arcpy.SelectLayerByAttribute_management(FileMmu1Tempa, 'NEW_SELECTION', '"AreaMt2" < ' + MMU)
    arcpy.Eliminate_management(FileMmu1Tempa, OutMmu1a, "LENGTH", '')
# MMU2
Mmu2Lista = arcpy.ListFeatureClasses('Mmu1*')
for e6a in Mmu2Lista:
    FileMmu2a = 'Mmu2' + str(e6a)[4:-4] + '.shp'
    OutMmu2a = os.path.join(FolderOutSc1, FileMmu2a)
    FileMmu2Tempa = str(e6a) + 'Temp'
    arcpy.MakeFeatureLayer_management(e6a, FileMmu2Tempa)
    arcpy.SelectLayerByAttribute_management(FileMmu2Tempa, 'NEW_SELECTION', '"AreaMt2" < ' + MMU)
    arcpy.Eliminate_management(FileMmu2Tempa, OutMmu2a, "LENGTH", '')
    arcpy.AddMessage ("POLYGON ELIMINATE BY MMU DONE FOR: " + e6a)
# Dissolve polygon by class
VectorListDisa = arcpy.ListFeatureClasses('Mmu2*')
for e3a in VectorListDisa:
    FileDisa = 'Chg' + str(e3a)[7:-4] + '.shp'
    OutDisa = os.path.join(FolderOutConDis, FileDisa)
    arcpy.Dissolve_management(e3a, OutDisa, 'gridcode', '', 'MULTI_PART', 'DISSOLVE_LINES')

arcpy.AddMessage ("END OF -------> SET AND ELIMINATE POLYGONS BY MINIMAL MAPPING UNIT: " + str(MMU) + "MT2 SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: CREATE FIELDS AND CALCULATE ATTRIBUTES SCRIPT!")
# Calculate fields
arcpy.env.workspace = FolderOutConDis
VectorListAreaC = list(set(arcpy.ListFeatureClasses('Chg*')) - set(arcpy.ListFeatureClasses('Merge*')))
VectorListAreaC.sort(reverse=False)
for e4a in VectorListAreaC:
    arcpy.AddField_management(e4a, 'SpecInd', 'TEXT', '', '', 10)
    arcpy.AddField_management(e4a, 'ReceDate', 'TEXT', '', '', 10)
    arcpy.AddField_management(e4a, 'OldDate', 'TEXT', '', '', 10)
    arcpy.AddField_management(e4a, 'RemVal', 'SHORT')
    arcpy.AddField_management(e4a, 'Legend', 'TEXT', '', '', 80)
    arcpy.AddField_management(e4a, 'AreaMt2', 'FLOAT')
    arcpy.AddField_management(e4a, 'AreaHa', 'FLOAT')
    arcpy.AddField_management(e4a, 'AreaKm2', 'FLOAT')
    arcpy.AddField_management(e4a, 'AreaPercen', 'FLOAT')
    arcpy.AddField_management(e4a, 'SrcShpFID', 'LONG')
    arcpy.CalculateField_management(e4a,'RemVal','!gridcode!','PYTHON')
    arcpy.DeleteField_management(e4a, 'gridcode')
    with arcpy.da.UpdateCursor(e4a, ('AreaMt2', 'AreaHa', 'AreaKm2', 'SHAPE@')) as ShpCur0a:
        for row in ShpCur0a:
            row[0], row[1], row[2] = [row[3].getArea('GEODESIC', 'SQUAREMETERS'), row[3].getArea('GEODESIC', 'HECTARES'), row[3].getArea('GEODESIC', 'SQUAREKILOMETERS')]
            ShpCur0a.updateRow(row)
    SumTotala = float(sum(row[0] for row in arcpy.da.SearchCursor(e4a, 'SHAPE@AREA')))
    with arcpy.da.UpdateCursor(e4a, ('SHAPE@AREA', 'AreaPercen')) as uCursora:
        for AreaC, Percenta in uCursora:
            uCursora.updateRow([AreaC, (AreaC / SumTotala) * 100])
    ShpFIDa = (e4a.split('_')[2])[3:-4]
    SpecInda = (e4a.split('_')[0])[3:-8]
    ReceDatea = RecentRaster
    OldDatea = OldRaster
    with arcpy.da.UpdateCursor(e4a, ('SrcShpFID', 'SpecInd', 'ReceDate', 'OldDate')) as ShpCur1a:
        for row in ShpCur1a:
            row[0], row[1], row[2], row[3] = [ShpFIDa, SpecInda, ReceDatea, OldDatea]
            ShpCur1a.updateRow(row)
    arcpy.AddMessage ("CALCULATE AREA & SOURCE ATTRIBUTES DONE FOR: " + e4a)
VectorListLeg = list(set(arcpy.ListFeatureClasses()) - set(arcpy.ListFeatureClasses('Merge*')))
VectorListLeg.sort(reverse=False)
for e4aa in VectorListLeg:
    with arcpy.da.UpdateCursor(e4aa, ('RemVal', 'Legend')) as tCursora:
        for valuez in tCursora:
            if valuez[0] == 0:
               valuez[1] = 'Recent period decreased coverage. Land cover loss from initial to final date'
            if valuez[0] == 1:
               valuez[1] = 'No change between periods. Land cover unchanged'
            if valuez[0] == 2:
               valuez[1] = 'Recent period increased coverage. Land cover recovery from initial to final date'
            tCursora.updateRow(valuez)
        arcpy.AddMessage ("CALCULATE LEGEND ATTRIBUTES DONE FOR: " + e4aa)

arcpy.AddMessage ("END OF -------> CREATE FIELDS AND CALCULATE ATTRIBUTES SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: GROUP AND MERGE SHAPEFILE BY NAME SCRIPT!")
# Group and merge by shapefile name
Dic1 = dd(list)
for Item1 in os.listdir(FolderOutConDis):
    FileItem1 = Item1.split('_')[1]
    if os.path.isfile(os.path.join(FolderOutConDis,Item1)) and Item1.endswith('.shp') and not Item1.startswith('Merge'):
        Dic1[FileItem1].append(os.path.join(FolderOutConDis, Item1))
for group1, mergelist1 in Dic1.items():
    arcpy.AddMessage ('GROUP SET FOR: ' + str(group1))
    arcpy.Merge_management(inputs=mergelist1, output=os.path.join(FolderOutConDis, 'MergeChg_{}.shp'.format(group1)))

arcpy.AddMessage ("END OF -------> GROUP AND MERGE SHAPEFILE BY NAME SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: JOIN FIELD WITH SOURCE SHAPEFILE SCRIPT!")
# Join fields with source shapefile
FolderA1 = ShpFolder
FolderB1 = FolderOutConDis
env.workspace = FolderA1
FolderAList1 = arcpy.ListFeatureClasses() # LIST INPUT SHAPEFILES
env.workspace = FolderB1
FolderBList1 = arcpy.ListFeatureClasses('Merge*') # LIST MERGED SHAPEFILES
for FileA1, FileB1 in zip(FolderAList1, FolderBList1):
    arcpy.JoinField_management((os.path.join(str(FolderB1), str(FileB1))), 'SrcShpFID', (os.path.join(str(FolderA1), str(FileA1))), 'FID')
    arcpy.DeleteField_management(FileB1, 'SrcShpFID')
    arcpy.AddMessage ('FIELDS JOINED FOR: ' + '[' + str(FileA1)[:-4] + ' & ' + str(FileB1)[:-4] + ']')

arcpy.AddMessage ("END OF -------> JOIN FIELD WITH SOURCE SHAPEFILE SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: WORKSPACE FOLDER CLEANUP SCRIPT!")
# Workspace folder cleanup
arcpy.env.workspace = FolderOutSc1
DataDela = list(set(arcpy.ListFeatureClasses()) | set(arcpy.ListDatasets('*.tif','Raster')))
DataDela.sort(reverse=False)
for del0a in DataDela:
    arcpy.Delete_management(del0a)
    arcpy.AddMessage ('DELETING TEMP FILE: ' + str(del0a))
arcpy.env.workspace = FolderOutConDis
MergeDelList1 = list(set(arcpy.ListFeatureClasses()) - set(arcpy.ListFeatureClasses('Merge*')))
MergeDelList1.sort(reverse=False)
for del2a in MergeDelList1:
    arcpy.Delete_management(del2a)
    arcpy.AddMessage ('DELETING TEMP FILE: ' + str(del2a))
arcpy.env.workspace = FolderOutReclass
DataDelz = arcpy.ListDatasets('*.tif', 'Raster')
DataDelz.sort(reverse=False)
for delz in DataDelz:
    arcpy.Delete_management(delz)
    arcpy.AddMessage ('DELETING TEMP FILE: ' + str(delz))
arcpy.env.workspace = OutputFolder
FolDela = arcpy.ListWorkspaces('Temp_Files [For Script2]', 'Folder')
for del1a in FolDela:
    arcpy.Delete_management(del1a)
    arcpy.AddMessage ('DELETING TEMP FOLDER: ' + str(del1a))

arcpy.AddMessage ("END OF -------> WORKSPACE FOLDER CLEANUP SCRIPT!")
arcpy.AddMessage ("START OF -------> STAGE: GENERATE EXCEL REPORT SCRIPT!")
# Generate Excel report with merged shapefiles
arcpy.env.workspace = FolderOutConDis
ExcelList1 = arcpy.ListFeatureClasses()
for ExFile1 in ExcelList1:
    ExFilename1 = 'D_Spectral_Index_Change_Detection [' + (ExFile1.split('_')[1])[:-4] +  ']' + '[' + RecentRaster + '-' + OldRaster + ']' +  '.xls'
    arcpy.TableToExcel_conversion(ExFile1, os.path.join(FolderOutSc1, ExFilename1))
    arcpy.AddMessage(('EXCEL REPORT DONE FOR: ') + str(ExFilename1))

arcpy.AddMessage ("END OF -------> GENERATE EXCEL REPORT SCRIPT!")
arcpy.AddMessage ("END OF -------> SRIPT [2/2]: SPECTRAL INDEX CHANGE DETECTION SCRIPT")
END1 = (time.clock()-START1)
arcpy.AddMessage ("SCRIPT RUNNING TIME -------> {} SECONDS".format(END1))