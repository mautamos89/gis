# coding=utf-8
# OBTENER VALORES ÚNICOS DE CAMPOS EN TABLA (ÚTIL PARA DOMINIOS)
import arcpy, os, pandas as pd
from time import strftime

print('inicio script: {0}'.format(strftime("%Y-%m-%d %H:%M:%S")))
ruta_carpeta = r'D:\tulua\Nueva carpeta\Carto1000_76834000_CABECERA_MPAL.gdb'
gdb_proces = ruta_carpeta.split("""\\""")[-1]
arcpy.env.workspace = ruta_carpeta
datasets = arcpy.ListDatasets('*', 'Feature')

flk = ['objectid', 'shape', 'shape_length', 'shape_area']

data = {
    'GDB': [],
    'Dataset': [],
    'Entidad': [],
    'Campo': [],
    'Alias': [],
    'Conteo_unicos': [],
    'Valor': [],
    'Dominio': [],
    'ValorDominio': [],
}

domains = arcpy.da.ListDomains(ruta_carpeta)

print("Creando el data frame!")

for dataset in datasets:
    arcpy.env.workspace = os.path.join(ruta_carpeta, dataset)
    fcs = arcpy.ListFeatureClasses()

    for fc in fcs:
        fields = arcpy.ListFields(fc)
        for field in fields:
            if field.name.lower() not in flk and field.type != 'Geometry':
                values = [row[0] for row in arcpy.da.SearchCursor(fc, field.name)]
                uniqueValues = sorted(set(values), reverse=False)
                valor_concatenado = ",".join(str(x) for x in uniqueValues)
                #import six
                #valor_concatenado = u",".join(six.text_type(x) for x in uniqueValues)

                data['GDB'].append(gdb_proces)
                data['Dataset'].append(dataset)
                data['Entidad'].append(fc)
                data['Campo'].append(field.name)
                data['Alias'].append(field.aliasName)
                data['Conteo_unicos'].append(len(uniqueValues))
                data['Valor'].append(valor_concatenado)

                if field.domain:
                    gdb_domains = arcpy.da.ListDomains(ruta_carpeta)
                    for domain in gdb_domains:
                        if domain.name == field.domain:
                            if domain.domainType == 'CodedValue':
                                coded_values = domain.codedValues
                                valor_descripcion = []
                                for valor in uniqueValues:
                                    for code, desc in coded_values.iteritems():
                                        if code == valor:
                                            valor_descripcion.append(desc)
                                            break
                                    else:
                                        valor_descripcion.append("")  # or None, depending on your preference
                                valor_descripcion_concatenado = ",".join(str(x) for x in valor_descripcion)
                                #valor_descripcion_concatenado = u",".join(six.text_type(x) for x in valor_descripcion)
                                data['ValorDominio'].append(valor_descripcion_concatenado)
                                data['Dominio'].append(field.domain)
                            else:
                                data['ValorDominio'].append("")  # or None, depending on your preference
                                data['Dominio'].append(field.domain)
                else:
                    data['ValorDominio'].append("")  # or None, depending on your preference
                    data['Dominio'].append("")  # or None, depending on your preference

print("Data frame creado!")
df = pd.DataFrame(data)

# Exportar dataframe a archivo de texto separado por "|"
ruta_salida = os.path.join(os.path.dirname(__file__), "{0}_{1}.txt".format(gdb_proces,strftime('%Y%m%d_%H%M%S')))
df.to_csv(ruta_salida, sep="|", index=False)

print("Archivo exportado a:", ruta_salida)
print('final script: {0}'.format(strftime("%Y-%m-%d %H:%M:%S")))