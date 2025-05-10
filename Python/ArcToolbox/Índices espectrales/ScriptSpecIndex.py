# Batch processing of satellite imagery including raster masking, bands splitting, map algebra, spectral index calculation, raster reclassification and segmentation of geographic objetcs.
# Requirements: Spatial Analyst
# Author: Mauricio Tabares Mosquera
# Date: 20220405

#Import necessary system modules
import arcpy,os
from arcpy import env
from arcpy.sa import *

#Overwrite files
arcpy.env.overwriteOutput = True

print "SET SCRIPT MODULES DONE!"

#Folder where raster files are located.  
arcpy.env.workspace = r"C:\Users\mauricio\Desktop\EvaluacionSistemaEPEcoparqueCinturonEco\Sig\gdb\Script\Raster" #Folder where satellite imagery is located and files will be saved.
arcpy.CheckOutExtension('Spatial')

#Location where output files will be saved.
arcpy.CreateFolder_management(arcpy.env.workspace, '0_ClipStudyArea')
arcpy.CreateFolder_management(arcpy.env.workspace, '1_SpecIndex')
arcpy.CreateFolder_management(arcpy.env.workspace, '2_Reclass')
arcpy.CreateFolder_management(arcpy.env.workspace, '3_Segments')
FolderOutClipStudyArea = arcpy.env.workspace + r'\0_ClipStudyArea'
FolderOutSpecIndex = arcpy.env.workspace + r'\1_SpecIndex'
FolderOutReclass = arcpy.env.workspace + r'\2_Reclass'
FolderOutSegMeanShift = arcpy.env.workspace + r'\3_Segments'

print "SET SCRIPT FOLDERS DONE!"

# Set local variables for clip with mask shapefile.
MaskShape = r"C:\Users\mauricio\Desktop\EvaluacionSistemaEPEcoparqueCinturonEco\Sig\gdb\StudyArea.shp" #Your shapefile used as mask.

# Set local variables for reclassify tool.
RecField = 'VALUE'
RemapNdvi = '-1,0 0 0;0 0,333333 1;0,333333 0,666666 2;0,666666 1 3'

# Set local variables for segmentation mean shift.
SpectralDetail = "15.5"
SpatialDetail = "15"
MinSegmentSize = "50"
BandIndex = "8 4 2"

print "SET SCRIPT PARAMETERS DONE!"

print "START OF -------> PROCESS TREE SCRIPT!"
print "START OF -------> STAGE 00: DESCRIBE RASTER SCRIPT!"

#Filter raster files with .tif extension.  
RasterList = arcpy.ListDatasets("*.tif","Raster")

#describe feature file then get its property
for a in RasterList:
    comp_type = arcpy.Describe(a).compressionType
    spa_ref = arcpy.Describe(a).spatialReference
    pix_type = arcpy.Raster(a).pixelType
    no_data = arcpy.Raster(a).noDataValue
    no_data_int = int(no_data)

    #print raster full description
    print a[:-4] + "|" + comp_type + "|" + spa_ref.name + "|" + pix_type + "|" + str(no_data_int)

print "END OF -------> DESCRIBE RASTER SCRIPT!"
print "START OF -------> STAGE 01: CLIP TO OBJECTS AND STUDY AREA SCRIPT!"

for RClip in RasterList:
    for b in range(6): #This number must the equal to the features in the shapefile
        arcpy.MakeFeatureLayer_management(MaskShape, "layer" + str(b), ' "FID" = ' + str(b)) #create a layer with only polygon i
        FileClip = RClip[:-4] + ".Mask." + str(b) + ".tif"
        OutClip = os.path.join(FolderOutClipStudyArea, FileClip)
        arcpy.Clip_management(RClip, "#", OutClip,"layer" + str(b), "0", "ClippingGeometry") #clip based on layer, clipping geometry will use the polygon extent only
        print "CLIP STUDY AREA DONE FOR: " + "FEATURE: " + str(b)

print "END OF -------> CLIP TO OBJECTS AND STUDY AREA SCRIPT!"
print "START OF -------> STAGE 02: MAP ALGEBRA: NDVI SCRIPT!"

arcpy.env.workspace = FolderOutClipStudyArea
RasterListSpecIndex = arcpy.ListDatasets("*.tif","Raster")

for c in RasterListSpecIndex:
    Red = arcpy.MakeRasterLayer_management(c, r"C:\Band_Red.tif", "", "", "4") # Number of the band needed for index calculation
    Nir = arcpy.MakeRasterLayer_management(c, r"C:\Band_Nir.tif", "", "", "8") # Number of the band needed for index calculation
    RasterRed = arcpy.Raster(r"C:\Band_Red.tif") # Filename of the temporal file to save the band as raster
    RasterNir = arcpy.Raster(r"C:\Band_Nir.tif") # Filename of the temporal file to save the band as raster
    OutNdvi = os.path.join(FolderOutSpecIndex,os.path.splitext(c)[0].split('_')[0] + '_Ndvi' + '.tif')
    Ndvi = (Float(RasterNir) - Float(RasterRed)) / (Float(RasterNir) + Float(RasterRed))
    Ndvi.save(OutNdvi)
    print "NDVI ALGEBRA DONE FOR: " + c

print "END OF -------> MAP ALGEBRA: NDVI SCRIPT!"
print "START OF -------> STAGE 03: MAP ALGEBRA: NDWI SCRIPT!"

for d in RasterListSpecIndex:
    Mir = arcpy.MakeRasterLayer_management(d, r"C:\Band_Mir.tif", "", "", "12") # Number of the band needed for index calculation
    Nir = arcpy.MakeRasterLayer_management(d, r"C:\Band_Nir.tif", "", "", "8") # Number of the band needed for index calculation
    RasterMir = arcpy.Raster(r"C:\Band_Mir.tif") # Filename of the temporal file to save the band as raster
    RasterNir = arcpy.Raster(r"C:\Band_Nir.tif") # Filename of the temporal file to save the band as raster
    OutNdwi = os.path.join(FolderOutSpecIndex,os.path.splitext(d)[0].split('_')[0] + '_Ndwi' + '.tif')
    Ndwi = (Float(RasterNir) - Float(RasterMir)) / (Float(RasterNir) + Float(RasterMir))
    Ndwi.save(OutNdwi)
    print "NDWI ALGEBRA DONE FOR: " + d

print "END OF -------> MAP ALGEBRA: NDWI SCRIPT!"
print "START OF -------> STAGE 04: RECLASSIFY SCRIPT!"

arcpy.env.workspace = FolderOutSpecIndex
RasterListReclass = arcpy.ListRasters()

# Execute Reclassify
for e in RasterListReclass:
    RecRaster = Reclassify(e, RecField, RemapNdvi, "NODATA")
    FileRec = 'Rec_' + str(e)[:-4] + '.tif'
    OutRec = os.path.join(FolderOutReclass, FileRec)
    RecRaster.save(OutRec)
    print "RECLASSIFY DONE FOR: " + e

print "END OF -------> RECLASSIFY SCRIPT!"
print "START OF -------> STAGE 05: SEGMENTATION MEAN SHIFT SCRIPT!"

arcpy.env.workspace = FolderOutClipStudyArea
RasterListSegMean = arcpy.ListDatasets("*.tif","Raster")

# Execute segment mean shift
for f in RasterListSegMean:
   SegRaster = SegmentMeanShift(f, SpectralDetail, SpatialDetail, MinSegmentSize, BandIndex)
   FileSeg = str(f)[:-4] + '-SegB' + str(BandIndex) + '.tif'
   OutSeg = os.path.join(FolderOutSegMeanShift, FileSeg)
   SegRaster.save(OutSeg)
   print "SEGMENTATION MEAN SHIFT DONE FOR: " + f

print "END OF -------> SEGMENTATION MEAN SHIFT SCRIPT!"
print "END OF -------> PROCESS TREE SCRIPT!"
