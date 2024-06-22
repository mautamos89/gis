# coding=utf-8
print(u'título: exportar gdb de estratificación con estructura de datos idesc y saul en archivo zip'.upper())
print(u'requisitos: Licencia básica de ArcGIS y sus herramientas'.upper())
print('autor: mauricio tabares mosquera'.upper())
print(u'carrera: geógrafo, especialista sig'.upper())
print('fecha: 2023-08-01'.upper())
import arcpy,os,datetime,time,zipfile
from arcpy import env # type: ignore
from time import strftime
from encodings import utf_8
tstart = datetime.datetime.now()
print('started at: {a}'.format(a=tstart).upper())
arcpy.env.overwriteOutput = True

# Definir rutas de archivos y variables
gdb = r'd:\gdb_estratificacion.gdb' # Base de datos copiada
#gdb_org = r'F:\dap_estrato\shp\gdb_estratificacion.gdb' # Base de datos original

# Definir rutas de los dataset
gdbf = r'\estratificacion'
gdbf1 = r'\suelo_expansion'
gdbf2 = r'\zonificacion'

# Definir rutas de procesamiento
fmem = r'in_memory'
fout = r'd:' + '\\'

# Definir variables principales del script
base_maestra = 'est_bd_maestra_20231229' # Cambiar para el corte de interés
es_urbano = 'est_es_urbano_202402' # Cambiar para el corte de interés
es_rural = 'est_es_rural_202402' # Cambiar para el corte de interés

# Definir listas de archivos y campos
lfk = ['OBJECTID','Shape','EmComuna','EmBarrio','EmManzana','EmObservac','EmSeseman','EmHistoric','EmLado','EmEstrato','EmFecPub','EmProyecto','EmDireccio',
'EmExpNumer','EmExpFecha','EmExpUrl','Shape_Length','Shape_Area'] # Campos Manzanas 500
flk = ['dat_est_estrato_urbano_expansion','pdt_est_estrato_manzanas_500','pdt_est_estrato_rural'] #Lista de features a conservar GDB : IDESC
flk1 = ['dat_est_estrato_urbano_expansion','pdt_est_estrato_manzanas_500','pdt_est_estrato_rural','areas_conurbanadas','dat_est_estrato_atipicos'] #Lista de features a conservar GDB : Gdrive

# Insertar las variables en la listas
flk.insert(0,base_maestra)
flk1.insert(0,base_maestra)
flk1.insert(len(flk1),es_urbano)
flk1.insert(len(flk1),es_rural)

# Definir direcciones absolutas y relativas de archivos
tmp = os.path.join(fmem,flk[0] + '_tmp')
tgdb = os.path.join(gdb,flk[1])
tfol = os.path.join(fout,flk[0] + '.dbf')
zidesc = "D:\gdb_est_idesc_" + strftime("%Y%m%d") + ".zip"
zdrive = "D:\gdb_est_gdrive_" + strftime("%Y%m%d") + ".zip"
zdbf = fout + flk[0] + '.zip'

# Dictionary with field name: Base Maestra IDESC
print('custom dictionary loaded'.upper())
dicf = {'ID_PREDIO':'EstIdPredi',
        'SESEMANLAD':'EstSesemal',
        'ESTRATO':'EstEstrato',
        'TIPO_EST':'EstTipEstr',
        'USO_PRINCI':'EstUsoPrin',
        'DESTINO_EC':'EstDestEco',
        'FECHA_PUB':'EstFecPub',
        'HISTORICO':'EstHistori'}

# Function to modify field name using dictionary
print('custom functions loaded'.upper())
def x(a): 
    if a in dicf.keys():
      return dicf[a]
    else:
      return ''

print('start processing gdb for gdrive repository'.upper())
# Copy original GDB to local drive
#print('COPYING DATABASE TO LOCAL DRIVE: {a}'.format(a=gdb_org))
#arcpy.Copy_management(gdb_org,gdb)
# GBD file for Gdrive
print('COPYING TABLE TO LOCAL DRIVE: {a}'.format(a=tfol))
arcpy.CopyRows_management(os.path.join(gdb,flk[0]),tfol.encode('UTF-8'))
print('table copied to memory'.upper())
print('TABLE: {a}, NUMBER OF RECORDS: {b}'.format(a=tfol,b=arcpy.GetCount_management(tfol)))

# Start zipping .Dbf file for Gdrive
print('start zipping'.upper())
zdbf1 = zipfile.ZipFile(zdbf, mode='w', compression=zipfile.ZIP_DEFLATED)
zdbf1.write(tfol, os.path.basename(tfol))
zdbf1.close()
arcpy.Delete_management(tfol)
print('FINISH ZIPPING FILE: {a}'.format(a=zdbf))

# Delete features
arcpy.env.workspace = gdb
print('deleting features'.upper())
ltf = sorted(arcpy.ListFeatureClasses(),reverse=False)
for count,value in enumerate(ltf,start=1):
    if value not in flk1:
        print('Feature deleted: {a}-{b}'.format(a=count,b=value))
        arcpy.Delete_management(value)
        time.sleep(1)
    else:
        print('Feature keep: {a}-{b}'.format(a=count,b=value))

# Delete tables
print('deleting tables'.upper())
ltt = sorted(arcpy.ListTables(),reverse=False)
for count,value in enumerate(ltt,start=1):
    if value not in flk1:
        print('Table deleted: {a}-{b}'.format(a=count,b=value))
        arcpy.Delete_management(value)
        time.sleep(1)
    else:
        print('Table keep: {a}-{b}'.format(a=count,b=value))

# Delete rasters
print('deleting rasters'.upper())
ltr = sorted(arcpy.ListRasters(),reverse=False)
for count,value in enumerate(ltr,start=1):
    if value not in flk1:
        print('Raster deleted: {a}-{b}'.format(a=count,b=value))
        arcpy.Delete_management(value)
        time.sleep(1)
    else:
        print('Raster keep: {a}-{b}'.format(a=count,b=value))

# Start zipping Gdb for Gdrive
print('start zipping'.upper())
zfile = zipfile.ZipFile(zdrive, mode='w', compression=zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk(fout):
 if root == gdb:
    for f in files:
        zfile.write(os.path.join(root, f))
zfile.close()
print('FINISH ZIPPING FILE: {a}'.format(a=zdrive))
print('finish processing gdb for gdrive repository'.upper())

# Gdb file for IDESC
print('start processing gdb for IDESC'.upper())
# Strata master list database
print('copying table to memory'.upper())
arcpy.CopyRows_management(os.path.join(gdb,flk[0]),tmp)
print('table copied to memory'.upper())
print('TABLE: {a}, NUMBER OF RECORDS: {b}'.format(a=tmp,b=arcpy.GetCount_management(tmp)))
print('updating data structure started'.upper())
fl = arcpy.ListFields(tmp)
for y in fl:
    fn = x(y.name)
    if y.name != 'OBJECTID' and fn != '':#and y.name not in dic.keys() :
        print(u'Modifying field: [{k}]. New field name: [{v}]. New field alias: [{a}]'.format(k=y.name,v=fn,a=y.aliasName))
        arcpy.AlterField_management(tmp,'{k}'.format(k=y.name),'{v}'.format(v=fn))
    elif y.name != 'OBJECTID':
        print('Deleting field: [{y}]'.format(y=y.name))
        arcpy.DeleteField_management(tmp,'{y}'.format(y=y.name))
        continue
print('updating data structure finished\nexporting new table started'.upper())
arcpy.CopyRows_management(tmp,tgdb) # Change second argument for saving location [tfol=folder,tgdb=gdb]
print('exporting table to gdb finished. location: {a}'.format(a=tgdb).upper()) # Change second argument for saving location [tfol=folder,tgdb=gdb]
#arcpy.CopyRows_management(tmp,tfol) # Change second argument for saving location [tfol=folder,tgdb=gdb]
#print('exporting table table to folder finished. location: {a}'.format(a=tfol).upper()) # Change second argument for saving location [tfol=folder,tgdb=gdb]
arcpy.Delete_management('in_memory')
print('memory cleaned'.upper())

# Manzanas 500 database
arcpy.env.workspace = gdb + gdbf
lf = arcpy.ListFields(flk[2])
for a in lf:
 if a.name not in lfk:
  print('Field deleted: {x}'.format(x=a.name))
  arcpy.DeleteField_management(flk[2],a.name)
  time.sleep(1)
 else:
  print('Field keep: {x}'.format(x=a.name))

# Delete features
print('deleting features'.upper())
ltf = sorted(arcpy.ListFeatureClasses(),reverse=False)
for count,value in enumerate(ltf,start=1):
    if value not in flk:
        print('Feature deleted: {a}-{b}'.format(a=count,b=value))
        arcpy.Delete_management(value)
        time.sleep(1)
    else:
        print('Feature keep: {a}-{b}'.format(a=count,b=value))

# Delete tables
print('deleting tables'.upper())
arcpy.env.workspace = gdb
ltt = sorted(arcpy.ListTables(),reverse=False)
for count,value in enumerate(ltt,start=1):
    if value not in flk or value == flk[0]:
        print('Table deleted: {a}-{b}'.format(a=count,b=value))
        arcpy.Delete_management(value)
        time.sleep(1)
    else:
        print('Table keep: {a}-{b}'.format(a=count,b=value))

# Delete features
ltf = sorted(arcpy.ListFeatureClasses(),reverse=False)
for count,value in enumerate(ltf,start=1):
    if value not in flk:
        print('Feature deleted: {a}-{b}'.format(a=count,b=value))
        arcpy.Delete_management(value)
        time.sleep(1)
    else:
        print('Feature keep: {a}-{b}'.format(a=count,b=value))

# Delete rasters
print('deleting rasters'.upper())
ltr = sorted(arcpy.ListRasters(),reverse=False)
for count,value in enumerate(ltr,start=1):
    if value not in flk:
        print('Raster deleted: {a}-{b}'.format(a=count,b=value))
        arcpy.Delete_management(value)
        time.sleep(1)
    else:
        print('Raster keep: {a}-{b}'.format(a=count,b=value))

# Deleting datasets
print('deleting feature dataset'.upper())
arcpy.Delete_management(gdb + gdbf1)
arcpy.Delete_management(gdb + gdbf2)
time.sleep(1)

# Start zipping Gdb for IDESC
print('start zipping'.upper())
zfile = zipfile.ZipFile(zidesc, mode='w', compression=zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk(fout):
 if root == gdb:
    for f in files:
        zfile.write(os.path.join(root, f))
zfile.close()
print('FINISH ZIPPING FILE: {a}'.format(a=zidesc))
print('finish processing gdb for IDESC'.upper())

# Deleting memory
arcpy.Delete_management('in_memory')
arcpy.Delete_management(gdb)
print('memory cleaned'.upper())

# Processing result
tend = datetime.datetime.now()
a,b,c = str(tend-tstart).split(':')[0].zfill(2), str(tend-tstart).split(':')[1].zfill(2), str(round(float(str(tend-tstart).split(':')[2]),0)).split('.')[0].zfill(2)
print('completed at: {a}'.format(a=tend).upper())
print('running time: {a} hours : {b} minutes : {c} seconds'.format(a=a,b=b,c=c).upper())