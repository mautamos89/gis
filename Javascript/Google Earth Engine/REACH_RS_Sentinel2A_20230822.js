print('TÍTULO: COMPOSICIÓN SENTINEL CON FILTRO DE FECHA, ÁREA Y NUBES \
\nAUTOR: MAURICIO TABARES MOSQUERA\nPROFESIÓN: GEÓGRAFO, ESPECIALISTA SIG\nFECHA:2023-08-22');

print('SCRIPT INICIADO: '+new Date().toLocaleString());

// Variables
var sat = 'COPERNICUS/S2_SR_HARMONIZED';
var dpto = 'Valle Del Cauca'; // Nivel: Departamental
var cntry = 'Colombia'; // Nivel: Nación
var fec = ['2000-01-01', '2022-12-31']; // Fechas de corte
var nub_per = 10; // Porcentaje máximo de nubes

print('VARIABLES DEFINIDAS');

// Área de estudio político administrativa - Nivel: Departamental
var st_area = ee.FeatureCollection('FAO/GAUL_SIMPLIFIED_500m/2015/level1');
var shp = st_area.filter(ee.Filter.eq('ADM1_NAME',dpto));

// Área de estudio político administrativa - Nivel: Nacional
// var st_area = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017');
// var shp = st_area.filter(ee.Filter.eq('country_na',cntry));

// Área de estudio por coordenadas de interés
// var coor = [-76.07153, 4.39539];

print('ÁREA DE ESTUDIO ESTABLECIDA');

var sentinel = ee.ImageCollection(sat)
  .filterDate(fec[0],fec[1])
  //.select(['B4','B3','B2'])
  .filterBounds(shp) // Filtro por unidad político-administrativa
  // .filterBounds(ee.Geometry.Point(coor[0], coor[1])) // Filtrar por coordenada de interés
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', nub_per));
var img = sentinel.mosaic().clip(shp);

print('FILTROS APLICADOS EN CUADRANTES Y MOSAICO GENERADO');
print(sentinel);

Map.addLayer(shp, {'color':'#ed4ed3','opacity':0.7},'Área de estudio');
Map.addLayer(img,{bands: 'B6,B4,B2',min:0, max:3000}, 'Comp: 6-4-2');
Map.addLayer(img,{bands:'B4,B3,B2',min:0, max:3000}, 'Comp: 4-3-2');
//Map.setCenter(-76.07153, 4.39539,8.3);
Map.centerObject(shp);

print('SCRIPT FINALIZADO: '+new Date().toLocaleString());