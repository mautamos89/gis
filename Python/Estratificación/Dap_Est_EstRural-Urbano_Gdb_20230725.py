# coding=utf-8
print('title: processing of "es_rural" and "es_urbano" tables and export to gdb or folder python script'.upper())
print('requirements: arcgis advanced license tools'.upper())
print('autor: mauricio tabares mosquera'.upper())
print('career: geographer, gis specialist'.upper())
print('fecha: 2023-07-25'.upper())
import arcpy,os,datetime
from encodings import utf_8
arcpy.env.overwriteOutput = True
tstart = datetime.datetime.now()
print('started at: {a}'.format(a=tstart).upper())
#gdb = r'F:\dap_estrato\shp\gdb_estratificacion.gdb'
gdb = r'd:\gdb_estratificacion.gdb'
fmem = r'in_memory'
fout = r'D:' + '\\' # Almacenar aquí los archivos .DBF
tab = 'est_es_rural_202402' #Change filename of local DBF file
tabu = 'est_es_urbano_202402' #Change filename of local DBF file
tmp = os.path.join(fmem,tab + '_tmp')
tmpu = os.path.join(fmem,tabu + '_tmp')
tmp1 = os.path.join(fmem,tab + '_tmp1')
tgdb = os.path.join(gdb,tab + '_tmp')
tgdbu = os.path.join(gdb,tabu + '_tmp')
tfol = os.path.join(fout, tab + '_tmp.dbf')
#1
print('#####################'.upper())
print('#  table: es_rural  #'.upper())
print('#####################'.upper())
print('copying table to gdb and memory -----> started'.upper())
arcpy.CopyRows_management(os.path.join(fout,tab + '.dbf'),os.path.join(gdb,tab))
arcpy.CopyRows_management(os.path.join(gdb,tab),tmp)
print('table copied to memory -----> finished'.upper())
print('TABLE: {a}, NUMBER OF RECORDS: {b}'.format(a=tmp,b=arcpy.GetCount_management(tmp)))
print('updating fields attributes -----> started'.upper())
fl = arcpy.ListFields(tmp)
for a in fl:
    if a.type == 'String':
        print('UPDATING VALUES: Field: {a} | Type: {b} | Length: {c}'.format(a=a.name,b=a.type,c=a.length))
        with arcpy.da.UpdateCursor(tmp,a.name) as cursor: # type: ignore
            for row in cursor:
                if row[0] == 0 or row[0] == '0' or row[0] == '' or row[0] == ' ' or row[0] == '-' or row[0] == 'N/A':
                    row[0] = None
                else:
                    row[0] = row[0].strip()
                    #continue
                cursor.updateRow(row)
    elif a.type == 'Integer' or a.type == 'SmallInteger' or a.type == 'Double':
        print('UPDATING VALUES: Field: {a} | Type: {b} | Length: {c}'.format(a=a.name,b=a.type,c=a.length))
        with arcpy.da.UpdateCursor(tmp,a.name) as cursor: # type: ignore
            for row in cursor:
                if row[0] == 0 or row[0] == '0' or row[0] == '' or row[0] == ' ' or row[0] == '-' or row[0] == 'N/A':
                    row[0] = None
                else:
                    row[0]
                    #continue
                cursor.updateRow(row)
print('updating fields attributes -----> finished'.upper())
#Create and calculate id_predio field as long
print('creating id_predio field as integer -----> started'.upper())
arcpy.AlterField_management(tmp,'id_predio','id_predio1')
arcpy.AddField_management(tmp,'ID_PREDIO','LONG')
arcpy.CalculateField_management(tmp,'ID_PREDIO','!id_predio1!','PYTHON_9.3')
arcpy.DeleteField_management(tmp,'id_predio1')
print('field created -----> finished'.upper())
#Sort table by keys [id_predio asc & estrato desc] and delete duplicates
print('sorting table by keys and delete duplicates -----> started'.upper())
arcpy.Sort_management(tmp,tmp1,[['id_predio','ASCENDING'],['estrato','DESCENDING']])
arcpy.MakeTableView_management(tmp1,'t1','id_predio is not null')
arcpy.DeleteIdentical_management('t1','id_predio')
print('table sorted without duplicates -----> finished'.upper())
#Export processed table to local disk
print('exporting new table -----> started'.upper())
arcpy.CopyRows_management(tmp1,tgdb) # Change second argument for saving location [tfol=folder,tgdb=gdb]
print('EXPORTING NEW TABLE -----> FINISHED. LOCATION: {a}, NUMBER OF RECORDS: {b}'.format(a=tgdb,b=arcpy.GetCount_management(tgdb))) # Change second argument for saving location [tfol=folder,tgdb=gdb]
#Cleaning memory
arcpy.Delete_management('in_memory')
print('memory cleaned'.upper())
#2
print('######################'.upper())
print('#  table: es_urbano  #'.upper())
print('######################'.upper())
print('copying table to gdb and memory -----> started'.upper())
arcpy.CopyRows_management(os.path.join(fout,tabu + '.dbf'),os.path.join(gdb,tabu))
arcpy.CopyRows_management(os.path.join(gdb,tabu),tmpu)
print('table copied to memory -----> finished'.upper())
print('TABLE: {a}, NUMBER OF RECORDS: {b}'.format(a=tmpu,b=arcpy.GetCount_management(tmpu)))
print('updating fields attributes -----> started'.upper())
#Deleting rows strata = 0
print('deleting rows strata = 0 -----> started'.upper())
arcpy.MakeTableView_management(tmpu,'tu1','estrato = 0')
arcpy.DeleteRows_management('tu1')
print('rows deleted -----> finished'.upper())
#Create and calculate strata field as text
print('creating strata field as text -----> started'.upper())
arcpy.AlterField_management(tmpu,'estrato','estrato1')
arcpy.AddField_management(tmpu,'ESTRATO','TEXT','','',1)
arcpy.CalculateField_management(tmpu,'ESTRATO','!estrato1!','python_9.3')
arcpy.DeleteField_management(tmpu,'estrato1')
print('field created -----> finished'.upper())
#Create cadastrial block attributes
print('creating cadastrial block and side field -----> started'.upper())
arcpy.AddField_management(tmpu,'SESEMANLAD','TEXT','','',9)
arcpy.CalculateField_management(tmpu,'SESEMANLAD','str(!sect!).zfill(2)+str(!secc!).zfill(2)+str(!manz!).zfill(4)+!lado!','python_9.3')
print('field created -----> finished'.upper())
#Export processed table to local disk
print('exporting new table -----> started'.upper())
arcpy.CopyRows_management(tmpu,tgdbu) # Change second argument for saving location [tfol=folder,tgdb=gdb]
print('EXPORTING NEW TABLE -----> FINISHED. LOCATION: {a}, NUMBER OF RECORDS: {b}'.format(a=tgdbu,b=arcpy.GetCount_management(tgdbu))) # Change second argument for saving location [tfol=folder,tgdb=gdb]
#Cleaning memory
arcpy.Delete_management('in_memory')
print('memory cleaned'.upper())
#Summary of process
tend = datetime.datetime.now()
a,b,c = str(tend-tstart).split(':')[0].zfill(2), str(tend-tstart).split(':')[1].zfill(2), str(round(float(str(tend-tstart).split(':')[2]),0)).split('.')[0].zfill(2)
print('completed at: {a}'.format(a=tend).upper())
print('running time: {a} hours : {b} minutes : {c} seconds'.format(a=a,b=b,c=c).upper())