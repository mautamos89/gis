# -----------------------------------------------------------------------------------------------------------
# Created on: 2017-03-23
# By: Mauricio Tabares and "Territorios" Research Group
# Description: it runs SVM, Classify Raster, Updated Accuracy Assessment Points and Confusion Matrix
# -----------------------------------------------------------------------------------------------------------

# Import arcpy module
import arcpy, os, sys, string
from arcpy import env
from arcpy.sa import *
arcpy.gp.overwriteOutput = 1

os.system('cls')

# Set of arguments
dirbase = raw_input('Workspace directory: ') 
dirout = raw_input('Output directory: ')
inputSegmented = raw_input('Enter segmented file name: ')
inputDEM = raw_input('Enter DEM name: ')

print "-------------------------------------------------"
print "     Running script: SVM Image Classification    " 
print "-------------------------------------------------"

# Set the workspace for ListFeatureClasses
arcpy.env.workspace = dirbase #r"D:\Workspace\Procalculo\MeanShift\Tile807.gdb"

# Local variables:
Segmentation = dirbase + "\\" + inputSegmented # r"D:\Workspace\Procalculo\MeanShift\Tile807.gdb\MS_807_spe15_spa15_531"
DEM_30m = dirbase + "\\" + inputDEM
output = dirout # r"D:\Workspace\Procalculo\MeanShift"

# PROCESS: SVM Classifier
# List of segmements (60 percent of the total)
inputData = arcpy.ListFeatureClasses("MS_807_TMS_60p_all_merge_*")
for a in inputData:
	if a[-3:] <> "pts": # This is used in order to avoid listing point features classes
		outputFileECD = output + "\\" + a.split("_")[-7] + "_" + a.split("_")[-6] + "_" + a.split("_")[-1] + ".ecd"
		print a
		# Run: SVM Classifier
		arcpy.gp.TrainSupportVectorMachineClassifier_sa(Segmentation, a, outputFileECD, DEM_30m, "0", "COLOR;MEAN;STD;COUNT;COMPACTNESS;RECTANGULARITY")
		print "Done with " + a
	
	# PROCESS: Classify Raster
	# Output for Classify Raster
	outputFileCR = a.split("_")[-7] + "_" + a.split("_")[-6] + "_" + a.split("_")[-1] + "_cr"
	# Run: Classify Raster
	arcpy.gp.ClassifyRaster_sa(Segmentation, outputFileECD, outputFileCR, DEM_30m)
	print "Done with " + outputFileCR
	
	# PROCESS: Updated Accuracy Assessment Points
	# List of feature classes for Updated Accuracy Assessment Points
	updateAAP = arcpy.ListFeatureClasses("*_pts")
	for b in updateAAP:
		print b
		# Output for UAAP feature classes
		outputFileUAAP = a.split("_")[-7] + "_" + a.split("_")[-6] + "_" + a.split("_")[-1] + "_uaap"
		#Run: Update Accuracy Assessment Points
		arcpy.gp.UpdateAccuracyAssessmentPoints_sa(outputFileCR, b, outputFileUAAP, "CLASSIFIED")
		print "Done with " + outputFileUAAP
	
	# PROCESS: Compute Confusion Matrix	
	# Output for Compute Confusion Matrix		
	outputFileCMM = a.split("_")[-7] + "_" + a.split("_")[-6] + "_" + a.split("_")[-1] + "_cmm"
	# Run: Compute Confusion Matrix
	arcpy.gp.ComputeConfusionMatrix_sa(outputFileUAAP, outputFileCMM)
	print "Done with " + outputFileCMM
	
	print "Finished!"
