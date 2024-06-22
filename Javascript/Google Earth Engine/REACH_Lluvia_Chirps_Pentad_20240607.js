/*
Título: Estimar el total de lluvia de un área de interés empleando CHIRPS PENTAD DATA (5 días).
Fuente: https://spatialthoughts.com/2020/10/28/rainfall-data-gee/
Fecha: 2024-06-06
Autor: GIS / DATA REACH
*/

// Variables de usuario

var muni = 'Puerto Asís' // En fuente tipo título
var st_area_field = 'shapeName'
var year = 2012
var escala_dat = 5000 // Tamaño de píxel de los datos orígen
var pre_min = 3000 
var pre_max = 6000

// Definir área de interés político-administrativa

var st_area = ee.FeatureCollection("WM/geoLab/geoBoundaries/600/ADM2")
var shp = st_area.filter(ee.Filter.eq(st_area_field,muni));

// Definir conjunto de datos de interés

var chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/PENTAD')

// Filtrar y cortar resultado con variables temporales y de área

var startDate = ee.Date.fromYMD(year, 1, 1)
var endDate = startDate.advance(1, 'year')
var filtered = chirps
  .filter(ee.Filter.date(startDate, endDate))
var total = filtered.reduce(ee.Reducer.sum()).clip(shp)

// Calcular estadísticas descriptivas del raster

var st_min = total.reduceRegion({
  reducer: ee.Reducer.min(),
  geometry: shp,
  scale: escala_dat,
  })
var min = st_min.get('precipitation_sum');

var st_max = total.reduceRegion({
  reducer: ee.Reducer.max(),
  geometry: shp,
  scale: escala_dat,
  })
var max = st_max.get('precipitation_sum');

var st_mean = total.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: shp,
  scale: escala_dat,
  })
var mean = st_mean.get('precipitation_sum');

print('Mínima: '+ year, min) // 3360.41 mm
print('Máxima: '+ year, max) // 5093.27 mm
print('Promedio: '+ year, mean) // 4372.39 mm

// Paleta de colores y clasificación de los datos

var palette = ['#ffffcc','#a1dab4','#41b6c4','#2c7fb8','#253494']
var visParams = {
  min: pre_min,
  max: pre_max,
  palette: palette
}

// Agregar capas a la vista actual

var nombre_capa = 'Precipitación total ' + year

Map.addLayer(shp, null, muni, null, 0.3)
Map.addLayer(total, visParams, nombre_capa,null,0.7)
Map.centerObject(shp,10)

// Generar enlace de descarga como archivo comprimido zip

print('Enlace de descarga: ' + nombre_capa,
  total.getDownloadURL({
    name: nombre_capa,
    scale: escala_dat,
    crs: 'EPSG:4326',
    fileFormat: 'ZIPPED_GEO_TIFF',
    //bands: ['B3', 'B8', 'B11'],
    region: shp.geometry()
  }));
