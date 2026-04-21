# Título: Práctica 1
# Módulo: Análisis de Datos Espaciales con R y R Studio
# Autor: Mauricio Tabares
# Fecha: 2026-01-03

# Desarrollo Práctica # 1 -------------------------------------------------

# Instalar y cargar librerías ---------------------------------------------
install.packages(c("pacman", "tidyverse", "sp", "sf", "terra",
                   "mapview", "viridis", "osmdata", "ggspatial"))
# remotes::install_github("r-spatial/mapview") # Forzar instalación desde repo Git
library(pacman)
p_load(tidyverse, janitor, ggplot2, sp, sf, mapview, terra, viridis, osmdata, ggspatial)
sessionInfo() # Validar paquetes cargados

# Importar los datos ------------------------------------------------------

# Geología
st_layers("datos/geologia.gpkg") # Verificar contenido
geologia <- st_read("datos/geologia.gpkg")
geologia_clean <- clean_names(geologia)
names(geologia_clean)
dim(geologia_clean) # Validar dimensiones
# Crear código permeabilidad
geologia_clean_permeabilidad <- geologia_clean %>%
  mutate(permeabilidad = case_when(
      descripcio %in% c(
        "Arcillas con cantos rodados",
        "Arcillas con cantos rodados dispersos",
        "Arcillas rojas y margas grises",
        "Arcillas y limos",
        "Gravas con matriz lutítica",
        "Lutitas con intercalaciones de areniscas") ~ 1,
      descripcio %in% c(
        "Calcáreas miocríticas",
        "Conglomerados que forman bancos lenticulares",
        "Depósitos de lechos de arroyos y torrentes actuales",
        "Gravas con matriz arenosa y arcillosa",
        "Gravas y limos",
        "Lecho actual, llanura inundable y terraza más baja",
        "Litosomas de microconglomerados y areniscas",
        "Lutitas con areniscas y microconglomerados",
        "Tramos conglomeráticos lenticulares") ~ 2,
      TRUE ~ 0 # Para los valores no listados
      )
    )
# Ver datos
dim(geologia_clean_permeabilidad) # Validar dimensiones
#View(geologia_clean_permeabilidad)
# Transfomar sistema de referencia a EPSG: 25831
geologia_clean_permeabilidad <- st_transform(geologia_clean_permeabilidad, 25831)
# Guardar en GeoJSON
st_write(geologia_clean_permeabilidad, "resultados/geologia_clean_permeabilidad.geojson", driver = "GeoJSON", delete_dsn = TRUE)
# Re-cargar con el mismo nombre
geologia_clean_permeabilidad <- st_read("resultados/geologia_clean_permeabilidad.geojson")
# Mapa estático
plot(geologia_clean_permeabilidad$geom, border = "white", col = "grey")

# Límite comarca
lim_comarca <- st_read("datos/lim_comarcal.shp")
lim_comarca_clean <- clean_names(lim_comarca)
names(lim_comarca_clean)
# Ver datos
#View(lim_comarca_clean)
# Transfomar sistema de referencia a EPSG: 25831
lim_comarca_clean <- st_transform(lim_comarca_clean, 25831)
# Guardar en GeoJSON
st_write(lim_comarca_clean, "resultados/lim_comarca_clean.geojson", driver = "GeoJSON", delete_dsn = TRUE)
# Re-cargar con el mismo nombre
lim_comarca_clean <- st_read("resultados/lim_comarca_clean.geojson")
# Mapa estático
plot(lim_comarca_clean$geom, border = "white", col = "grey")

# Zona protegida - Espacio natural
st_layers("datos/proteccion.gpkg") # Verificar contenido
espacio_natural <- st_read("datos/proteccion.gpkg", layer = "espacios_naturales")
espacio_natural_clean <- clean_names(espacio_natural)
names(espacio_natural_clean)
# Ver datos
#View(espacio_natural_clean)
# Transfomar sistema de referencia a EPSG: 25831
espacio_natural_clean <- st_transform(espacio_natural_clean, 25831)
# Guardar en GeoJSON
st_write(espacio_natural_clean, "resultados/espacio_natural_clean.geojson", driver = "GeoJSON", delete_dsn = TRUE)
# Re-cargar con el mismo nombre
espacio_natural_clean <- st_read("resultados/espacio_natural_clean.geojson")
# Mapa estático
plot(espacio_natural_clean$geom, border = "white", col = "grey")

# Zona protegida - Humedal
st_layers("datos/proteccion.gpkg") # Verificar contenido
humedal <- st_read("datos/proteccion.gpkg", layer = "humedales")
humedal_clean <- clean_names(humedal)
names(humedal_clean)
# Ver datos
#View(humedal_clean)
# Transfomar sistema de referencia a EPSG: 25831
humedal_clean <- st_transform(humedal_clean, 25831)
# Guardar en GeoJSON
st_write(humedal_clean, "resultados/humedal_clean.geojson", driver = "GeoJSON", delete_dsn = TRUE)
# Re-cargar con el mismo nombre
humedal_clean <- st_read("resultados/humedal_clean.geojson")
# Mapa estático
plot(humedal_clean$geom, border = "white", col = "grey")

# Zona protegida - Fauna y flora
st_layers("datos/proteccion.gpkg") # Verificar contenido
fauna_flora <- st_read("datos/proteccion.gpkg", layer = "interes_fauna_flora")
fauna_flora_clean <- clean_names(fauna_flora)
names(fauna_flora_clean)
# Ver datos
#View(fauna_flora_clean)
# Transfomar sistema de referencia a EPSG: 25831
fauna_flora_clean <- st_transform(fauna_flora_clean, 25831)
# Guardar en GeoJSON
st_write(fauna_flora_clean, "resultados/fauna_flora_clean.geojson", driver = "GeoJSON", delete_dsn = TRUE)
# Re-cargar con el mismo nombre
fauna_flora_clean <- st_read("resultados/fauna_flora_clean.geojson")
# Mapa estático
plot(fauna_flora_clean$geom, border = "white", col = "grey")

# Zona protegida - Agua subterránea
st_layers("datos/proteccion.gpkg") # Verificar contenido
agua_subterranea <- st_read("datos/proteccion.gpkg", layer = "masa_agua_subterranea")
agua_subterranea_clean <- clean_names(agua_subterranea)
names(agua_subterranea_clean)
# Ver datos
#View(agua_subterranea_clean)
# Transfomar sistema de referencia a EPSG: 25831
agua_subterranea_clean <- st_transform(agua_subterranea_clean, 25831)
# Guardar en GeoJSON
st_write(agua_subterranea_clean, "resultados/agua_subterranea_clean.geojson", driver = "GeoJSON", delete_dsn = TRUE)
# Re-cargar con el mismo nombre
agua_subterranea_clean <- st_read("resultados/agua_subterranea_clean.geojson")
# Mapa estático
plot(agua_subterranea_clean$geom, border = "white", col = "grey")

# Suelos - Cubierta suelo tabla
cubierta_suelo_tabla <- st_read("datos/suelos.gpkg", layer = "cubiertas_suelo_categorias")
cubierta_suelo_tabla_clean <- clean_names(cubierta_suelo_tabla)
names(cubierta_suelo_tabla_clean)
# Ver datos
#View(cubierta_suelo_tabla_clean)

# Suelos - Cubierta suelo
st_layers("datos/suelos.gpkg") # Verificar contenido
cubierta_suelo <- st_read("datos/suelos.gpkg", layer = "cubiertas_suelo")
cubierta_suelo_clean <- clean_names(cubierta_suelo)
names(cubierta_suelo_clean)
# Unir tabla y campo categoría
cubierta_suelo_clean_join <- cubierta_suelo_clean %>%
  left_join(
    cubierta_suelo_tabla_clean %>%
      select(nivell_2, categoria), by = "nivell_2")
# Ver datos
#View(cubierta_suelo_clean_join)
# Transfomar sistema de referencia a EPSG: 25831
cubierta_suelo_clean_join <- st_transform(cubierta_suelo_clean_join, 25831)
# Guardar en GeoJSON
st_write(cubierta_suelo_clean_join, "resultados/cubierta_suelo_clean_join.geojson", driver = "GeoJSON", delete_dsn = TRUE)
# Re-cargar con el mismo nombre
cubierta_suelo_clean_join <- st_read("resultados/cubierta_suelo_clean_join.geojson")
names(cubierta_suelo_clean_join)
# Mapa estático
plot(cubierta_suelo_clean_join$geom, border = "white", col = "grey")

# Urbanismo
st_layers("datos/urbanismo.gpkg") # Verificar contenido
urbanismo <- st_read("datos/urbanismo.gpkg", layer = "urbanismo")
urbanismo_clean <- clean_names(urbanismo)
names(urbanismo_clean)
# Ver datos
#View(urbanismo_clean)
# Transfomar sistema de referencia a EPSG: 25831
urbanismo_clean <- st_transform(urbanismo_clean, 25831)
# Guardar en GeoJSON
st_write(urbanismo_clean, "resultados/urbanismo_clean.geojson", driver = "GeoJSON", delete_dsn = TRUE)
# Re-cargar con el mismo nombre
urbanismo_clean <- st_read("resultados/urbanismo_clean.geojson")
# Mapa estático
plot(urbanismo_clean$geom, border = "white", col = "grey")

# Modelo digital de elevación
modelo_elevacion <- rast("datos/mde_5m_20241210_124521.tif")
# Verificar datos
modelo_elevacion
# Mapa estático
plot(modelo_elevacion, col = viridis::viridis(100))
# Calcular pendiente en grados
pendiente_grados <- terrain(modelo_elevacion, v = "slope", unit = "degrees")
# Convertir a porcentaje: tan(θ) * 100
pendiente_porcentaje <- tan(pendiente_grados * pi / 180) * 100
# Guardar raster de pendientes
writeRaster(pendiente_porcentaje, "resultados/mde_porcen.tif", overwrite = TRUE)
# Re-cargar archivo guardado
pendiente_porcentaje <- rast("resultados/mde_porcen.tif")
# Verificar
pendiente_porcentaje
# Visualizar
plot(pendiente_porcentaje, col = viridis::viridis(100))

# Descargar datos OSM -----------------------------------------------------
# Filtrar por la geometría de interés
comarca_interes <- lim_comarca_clean %>%
  filter(codicomar == 27)
#View(comarca_interes)
# Visualizar
mapview(comarca_interes, zcol = "nomcomar")
# Transfomar sistema de referencia a WGS84 - 4326
comarca_interes_wgs <- st_transform(comarca_interes, 4326)
# Calcular extensión para servicio OSM
bbox <- st_bbox(comarca_interes_wgs)

# Filtrar y descargar los datos - Ríos [Descarga falla al hacer una lista (c)]
consulta <- opq(bbox = bbox) %>%
  add_osm_feature(key = "waterway", value = "river")
# Descargar
rio_osm <- osmdata_sf(consulta)
# Seleccionar la geometría
rio_linea <- rio_osm$osm_lines
# Limpiar campos
rio_linea_clean <- clean_names(rio_linea)
names(rio_linea_clean)
# Ver tabla
#View(rio_linea_clean)
# Transfomar sistema de referencia a EPSG: 25831
rio_linea_clean <- st_transform(rio_linea_clean, 25831)
# Guardar en GeoJSON
st_write(rio_linea_clean, "resultados/rio_linea_clean.geojson", driver = "GeoJSON", delete_dsn = TRUE)
# Volver a cargar con el mismo nombre
rio_linea_clean <- st_read("resultados/rio_linea_clean.geojson")
# Visualizar mapa
mapview(comarca_interes_wgs, zcol = "nomcomar") +
  mapview(rio_linea_clean, color = "blue")

# Filtrar y descargar los datos - Arroyos
consulta <- opq(bbox = bbox) %>%
  add_osm_feature(key = "waterway", value = "stream")
# Descargar
arroyo_osm <- osmdata_sf(consulta)
# Seleccionar la geometría
arroyo_linea <- arroyo_osm$osm_lines
# Limpiar campos
arroyo_linea_clean <- clean_names(arroyo_linea)
names(arroyo_linea_clean)
# Ver tabla
#View(arroyo_linea_clean)
# Transfomar sistema de referencia a EPSG: 25831
arroyo_linea_clean <- st_transform(arroyo_linea_clean, 25831)
# Guardar en GeoJSON
st_write(arroyo_linea_clean, "resultados/arroyo_linea_clean.geojson", driver = "GeoJSON", delete_dsn = TRUE)
# Volver a cargar con el mismo nombre
arroyo_linea_clean <- st_read("resultados/arroyo_linea_clean.geojson")
# Visualizar mapa
mapview(comarca_interes_wgs, zcol = "nomcomar") +
  mapview(arroyo_linea_clean, color = "grey") +
  mapview(rio_linea_clean, color = "blue")

# Filtrar y descargar los datos - Canales
consulta <- opq(bbox = bbox) %>%
  add_osm_feature(key = "waterway", value = "canal")
# Descargar
canal_osm <- osmdata_sf(consulta)
# Seleccionar la geometría
canal_linea <- canal_osm$osm_lines
# Limpiar campos
canal_linea_clean <- clean_names(canal_linea)
names(canal_linea_clean)
# Ver tabla
#View(canal_linea_clean)
# Transfomar sistema de referencia a EPSG: 25831
canal_linea_clean <- st_transform(canal_linea_clean, 25831)
# Guardar en GeoJSON
st_write(canal_linea_clean, "resultados/canal_linea_clean.geojson", driver = "GeoJSON", delete_dsn = TRUE)
# Volver a cargar con el mismo nombre
canal_linea_clean <- st_read("resultados/canal_linea_clean.geojson")
# Visualizar mapa
mapview(comarca_interes_wgs, zcol = "nomcomar") +
  mapview(arroyo_linea, color = "grey") +
  mapview(rio_linea, color = "blue") +
  mapview(canal_linea_clean, color = "purple")

# Geoprocesamiento --------------------------------------------------------

# Variables
buffer_espacio_protegido <- st_buffer(espacio_natural_clean, dist = 1000)
buffer_humedal <- st_buffer(humedal_clean, dist = 500)
zona_subterranea <- agua_subterranea_clean
buffer_rio <- st_buffer(rio_linea_clean, dist = 350)
buffer_arroyo <- st_buffer(arroyo_linea_clean, dist = 150)
buffer_canal <- st_buffer(canal_linea_clean, dist = 50)
buffer_fauna_flora <- st_buffer(fauna_flora_clean, dist = 500)
filtro_permeabilidad <- geologia_clean_permeabilidad %>%
  filter(permeabilidad != 1) # Invertido para crear las restricciones
filtro_cubierta <- cubierta_suelo_clean_join %>% 
  filter(!nivell_2 %in% c(116,224,228,230,350,352)) # No zona quemada
filtro_suelo_urbano <- urbanismo_clean %>%
  filter(!d_clas_muc %in% c("Suelo urbano no consolidado",
                            "Suelo urbanizable no delimitado",
                            "Suelo urbanizable delimitado"))

# Unir geometrías y luego hacer unión (se pierde atributos)
restricciones <- st_union(
  do.call(c, list(
    st_geometry(buffer_espacio_protegido),
    st_geometry(buffer_humedal),
    st_geometry(zona_subterranea),
    st_geometry(buffer_rio),
    st_geometry(buffer_arroyo),
    st_geometry(buffer_canal),
    st_geometry(buffer_fauna_flora),
    st_geometry(filtro_permeabilidad),
    st_geometry(filtro_cubierta),
    st_geometry(filtro_suelo_urbano)
  ))
)

# Diferencia espacial: comarca menos restricciones
zona_apta <- st_difference(comarca_interes, restricciones)
zona_apta$aptitud <- "Sí" # Añadir campo de aptitud

# Disolver, explotar y seleccionar polígonos ------------------------------

# Disolver los polígonos
zona_apta_dis <- st_union(zona_apta)
# Convertir a uniparte
zona_apta_uni <- st_cast(zona_apta_dis, "POLYGON")
# Convertir a sf
zona_apta <- st_as_sf(zona_apta_uni)
# calcular área en hectáreas
zona_apta <- zona_apta %>%
  mutate(area_ha = round(as.numeric(st_area(.) / 10000), 3)) %>% 
  filter(area_ha >= 3) # Filtrar por área

# Calcular estadística zonal ----------------------------------------------
zona_apta_vect <- vect(zona_apta) # convertir a SpatVector
# Calcular estadística zonal por polígono
zonal_stats <- terra::extract(pendiente_porcentaje, zona_apta_vect, fun = mean, na.rm = TRUE)
# Unir resultado a capa
zona_apta_vect$pendiente_media <- round(zonal_stats[,2], 3)
zona_apta <- st_as_sf(zona_apta_vect) # Convertir a sf

# Filtrar por pendiente media
zona_apta <- zona_apta %>%
  filter(pendiente_media <= 5) # Filtrar por área
zona_apta$aptitud <- "Sí" # Añadir campo de aptitud

# Transfomar sistema de referencia a EPSG: 25831
zona_apta <- st_transform(zona_apta, 25831)
# Guardar en GeoJSON
st_write(zona_apta, "resultados/zona_apta.geojson", driver = "GeoJSON", delete_dsn = TRUE)
# Volver a cargar con el mismo nombre
zona_apta <- st_read("resultados/zona_apta.geojson")
# Verificar
# View(zona_apta)
print(zona_apta)

# Zonas no aptas: restricciones recortadas al límite de la comarca
zona_no_apta <- st_difference(comarca_interes, st_union(zona_apta))
zona_no_apta$aptitud <- "No"

# Transfomar sistema de referencia a EPSG: 25831
zona_no_apta <- st_transform(zona_no_apta, 25831)
# Guardar en GeoJSON
st_write(zona_no_apta, "resultados/zona_no_apta.geojson", driver = "GeoJSON", delete_dsn = TRUE)
# Volver a cargar con el mismo nombre
zona_no_apta <- st_read("resultados/zona_no_apta.geojson")
# Verificar
# View(zona_no_apta)
print(zona_no_apta)

# Visualizar
mapview(comarca_interes, zcol = "nomcomar") +
  mapview(zona_no_apta, col.regions = "red") +
  mapview(zona_apta, col.regions = "green")

# Mapa final --------------------------------------------------------------
mapa_final <- ggplot() +
  # Comarca de interés (límite)
  geom_sf(data = comarca_interes, aes(fill = "Comarca"), color = "black", size = 1, alpha = 0.1) +
  # Zonas no aptas
  geom_sf(data = zona_no_apta, aes(fill = "Zona no apta"), color = "darkred", alpha = 0.5) +
  # Zonas aptas
  geom_sf(data = zona_apta, aes(fill = "Zona apta"), color = "darkgreen", alpha = 0.6) +
  # Título, subtítulo y créditos
  labs(
    title = "Localización óptima de instalación",
    subtitle = "Planta de gestión de residuos en Pla d’Urgell, provincia de Lleida",
    caption = "Fuente: Datos abiertos Generalitat de Catalunya; OSM",
    fill = "Leyenda"
    ) +
  scale_fill_manual(values = c("Zona apta" = "green", "Zona no apta" = "red", "Comarca" = "grey80")) +
  # Grid de coordenadas UTM
  coord_sf(datum = st_crs(25831)) +
  # Barra de escala
  annotation_scale(location = "br", width_hint = 0.15) +
  # Flecha de norte
  annotation_north_arrow(
    location = "tr",
    which_north = "true",
    style = north_arrow_fancy_orienteering,
    height = unit(0.75, "cm"),
    width = unit(0.75, "cm")
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 13.5, face = "bold"),
    plot.subtitle = element_text(size = 11),
    plot.caption = element_text(size = 9, hjust = 0)
    )
mapa_final

# Guardar con tamaño específico en píxeles
ggsave("plots/mapa.png",
       plot = mapa_final,
       width = 2560,
       height = 1440,
       units = "px",
       dpi = 300,
       bg = "white")

# Guardar los objetos de la sesión R --------------------------------------
save.image(file=".RData")
