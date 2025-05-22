# --------------------------------------------------------------------------- 
# Stratified Random Selection, Merge and Centroids 
# By: Mauricio Tabares and "Territorios" Research Group
# Created on: 2017-03-28 
# ---------------------------------------------------------------------------  

# Import arcpy module
import arcpy, os
from arcpy import env
from arcpy.sa import * 
arcpy.gp.overwriteOutput = 1 
 
os.system('cls') 
 
# Set of arguments
dirbase = raw_input('Workspace directory: ')
dirout = raw_input('Output directory: ')
inputShapefile = raw_input('Input data: ') 
 
 
print("--------------------------------------------------------------------------")
print("-----Running script: Stratified Random Selection, Merge and Centroids-----")
print("--------------------------------------------------------------------------")  

# Workspace 
#outputDirectory = r"H:\X\Prueba\tile_607\escript\Tile607.gdb" 
arcpy.env.workspace = dirbase
outputDirectory = arcpy.env.workspace 
 
# Set of variables
inputData = inputShapefile 
#inputData = "MS_607_TMS_a" 
 
# PROCESS 1: SELECT CLASSES 
for a in range (1, 16): # Number of classes 
	print("We're on time %d" % (a))
	outputClass = "MS_607_TMS_class_" + str(a)
	where_clause = "Classvalue = " + str(a) 
 	# Execute Select
	arcpy.Select_analysis(inputData, outputClass, where_clause)
	print("Done with " + outputClass)
 	 
# PROCESS 2: SUBSET FEATURES # Data sets (40% and 60%) 
inputClasses = arcpy.ListFeatureClasses("MS_607_TMS_class*")
for b in inputClasses:
	for c in range (1, 21): # Number of groups of 40% and 60% to be created
		output60p = b.split("_")[-2] + "_" + b.split("_")[-1] + "_" + "MS_607_TMS_60p" + "_" + "iteration" + "_" + str(c)
		output40p = b.split("_")[-2] + "_" + b.split("_")[-1] + "_" + "MS_607_TMS_40p" + "_" + "iteration" + "_" + str(c) 
 	 	# Execute SubsetFeatures
		arcpy.SubsetFeatures_ga(b, output60p, output40p, "60", "PERCENTAGE_OF_INPUT")
		print("class " + str(b))
		print("Done with SubsetFeatures class " + "iteration " + str(c))
 	 	 	 
# PROCESS 3: MERGE 
# Merge feature classes representing 40% of the records
for d in range (1, 21): # Number of groups of 40% to be merged
	inputFile40 = "*MS_607_TMS_40p_iteration_" + str(d)
	listElements40 = arcpy.ListFeatureClasses(inputFile40)
	print("New group", listElements40)
	outputFile40 = "MS_607_TMS_40p_all_merge" + "_" + str(d)
	arcpy.Merge_management(listElements40, outputFile40)
	print("Done with merge class " + outputFile40)
 	 
# Number of groups of 60% to be merged
	inputFile60 = "*MS_607_TMS_60p_iteration_" + str(d)
	listElements60 = arcpy.ListFeatureClasses(inputFile60)
	print("New group", listElements60)
	outputFile60 = "MS_607_TMS_60p_all_merge" + "_" + str(d)
	arcpy.Merge_management(listElements60, outputFile60)
	print("Done with merge class " + outputFile60)
 
 	# PROCESS 4: FEATURE TO POINTS (CENTROIDS)
	outFeatureClassPts = outputFile40 + "_pts" 
 	# Use FeatureToPoint function to find a point inside polygon
	arcpy.FeatureToPoint_management(outputFile40, outFeatureClassPts, "INSIDE")
	print("Done finding centroids " + outFeatureClassPts)
	
	print("Finished!")
 
