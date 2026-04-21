# Título: Práctica 2
# Módulo: Análisis de Datos Espaciales con R y R Studio
# Autor: Mauricio Tabares
# Fecha: 2026-01-17

# Desarrollo Práctica # 2 -------------------------------------------------

# Instalar y cargar librerías ---------------------------------------------
install.packages(c("pacman", "tidyverse", "janitor", "sp", "sf", "purr", "mapview",
                   "terra", "viridis", "CatastRo"))
# remotes::install_github("r-spatial/mapview") # Forzar instalación desde repo Git
library(pacman)
p_load(tidyverse, janitor, sp, sf, purrr, mapview, terra, viridis, CatastRo)
sessionInfo() # Validar paquetes cargados

# Importar los datos ------------------------------------------------------

# Municipios
municipios <- st_read("datos/municipios.geojson")
# Limipiar nombres de campo
municipios_clean <- clean_names(municipios)
names(municipios_clean)
# Transfomar sistema de referencia a EPSG: 25831
municipios_clean <- st_transform(municipios_clean, 25831)
# Guardar en GeoJSON
st_write(municipios_clean, "resultados/municipios_clean.geojson", driver = "GeoJSON", delete_dsn = TRUE)
# Re-cargar con el mismo nombre
municipios_clean <- st_read("resultados/municipios_clean.geojson")
# Mapa estático
plot(municipios_clean$geom, border = "white", col = "grey")

# Suelos - Cubierta suelo tabla
df_cubierta_tabla <- read.csv("datos/tabla_cubiertas.csv", sep = ",", encoding = "utf8")
# View(df_cubierta_tabla) # Ver el df
df_cubierta_tabla_clean <- clean_names(df_cubierta_tabla)
names(df_cubierta_tabla_clean)
# View(df_cubierta_tabla_clean) # Ver datos

# Suelos - Cubierta suelo
st_layers("datos/cubiertas_suelo.gpkg") # Verificar contenido
cubierta_suelo <- st_read("datos/cubiertas_suelo.gpkg", layer = "cubiertas")
cubierta_suelo_clean <- clean_names(cubierta_suelo)
names(cubierta_suelo_clean)
# plot(cubierta_suelo_clean$geom, border = "black", col = "grey") # Mapa estático

# Unir tabla y campo categoría
cubierta_suelo_clean_join <- cubierta_suelo_clean %>%
  left_join(
    df_cubierta_tabla_clean %>%
      select(nivel_2, categoria), by = "nivel_2")
# Ver datos
# View(cubierta_suelo_clean_join)
# Transfomar sistema de referencia a EPSG: 25831
cubierta_suelo_clean_join <- st_transform(cubierta_suelo_clean_join, 25831)
# Guardar en GeoJSON
# st_write(cubierta_suelo_clean_join, "resultados/cubierta_suelo_clean_join.geojson", driver = "GeoJSON", delete_dsn = TRUE)
# Re-cargar con el mismo nombre
# cubierta_suelo_clean_join <- st_read("resultados/cubierta_suelo_clean_join.geojson")
# Mapa estático
plot(cubierta_suelo_clean_join$geom, border = "black", col = "grey")

# Modelo digital de elevación
modelo_elevacion <- rast("datos/mde_5m.tif")
# Verificar datos
modelo_elevacion
# Transformar sistema a EPSG: 28531 y usar definición de otra capa
crs(modelo_elevacion) <- st_crs(cubierta_suelo_clean_join)$wkt
# Mapa estático
plot(modelo_elevacion, col = viridis::viridis(100))

# Geoprocesamiento --------------------------------------------------------

# Máscara límite comarcal y recorte DEM -----------------------------------

# Unir límite de municipios
limite_comarcal <- st_union(municipios_clean)
limite_vectorial <- vect(limite_comarcal) # Necesario para enmascarar
# plot(limite_vectorial, border = "black", col = "white") # Validar
# Recortar y enmascarar
mde_recorte <- crop(modelo_elevacion, limite_vectorial, mask = TRUE)
# Guardar resultado
#writeRaster(mde_recorte, "resultados/mde_recorte.tif", overwrite = TRUE)
# Visualizar para verificar
plot(mde_recorte, col = viridis::viridis(100))

# Valores mín-máx ---------------------------------------------------------

# Obtener valores mínimo y máximo
valores_extremos <- minmax(mde_recorte) # minxmax los guardó como tupla
print(paste("Valor mínimo:", valores_extremos[1]))
print(paste("Valor máximo:", valores_extremos[2]))

# Aislar zonas con cota superior a 750m -----------------------------------

mde_750 <- mde_recorte
mde_750[mde_750 <= 750] <- NA
plot(mde_750, col = viridis::viridis(100))

# Guardar el resultado
writeRaster(mde_750, "resultados/mde_750.tif", overwrite = TRUE)

# Plot relieve sombreado --------------------------------------------------

# Las zonas >750m reciben el valor 1 y el resto 0
mde_binario <- mde_recorte > 750
# Labels para la leyenda
levels(mde_binario) <- data.frame(id = c(0, 1), 
                                  label = c("< 750m", "> 750m"))
# Definir colores para el mapa
colores_binarios <- c("blue", "green")

# Generar el relieve sombreado
pend <- terrain(mde_recorte, v = "slope", unit = "radians")
aspect <- terrain(mde_recorte, v = "aspect", unit = "radians")
sombreado <- shade(pend, aspect, angle = 45, direction = 315)

# Crear y abrir archivo de imagen
png("plots/1_mapa_zona_750m.png", 
    width = 2560, 
    height = 1440, 
    units = "px", 
    res = 300)

# Plot: sombreado
plot(sombreado, col = grey(0:100 / 100), legend = FALSE, 
     main = "Zonas > 750m", axes = TRUE)

# Plot: mapa binario
plot(mde_binario, 
     col = colores_binarios, 
     alpha = 0.5, 
     add = TRUE, 
     plg = list(title = "Elevación", x = "topright"),
     labels = c("< 750m", "> 750m"))

# Guardar el archivo
dev.off()

# 4 puntos situados en la zona >750m --------------------------------------

puntos_750 <- spatSample(mde_750, 
                         size = 4, 
                         method = "random", 
                         na.rm = TRUE, # Elegir únicamente píxeles con datos
                         xy = TRUE, # Regresa las coordenadas
                         values = TRUE) # Extraer valores del raster

# Verificar la ubicación
plot(mde_750, col = "green", main = "Localización de los 4 puntos (>750m)")
points(puntos_750[, c("x", "y")], pch = 21, bg = "red", col = "white", cex = 1.5)

# Convertir a sf
puntos_750 <- st_as_sf(puntos_750,
                       coords = c("x", "y"),
                       crs = 25831)

# Renombrar columnas
puntos_750$id <- 1:nrow(puntos_750)
names(puntos_750)[names(puntos_750) == "mde_5m"] <- "z"
names(puntos_750)

# Ver resultado
print(puntos_750)

# Transfomar sistema de referencia a EPSG: 25831
puntos_750 <- st_transform(puntos_750, 25831)

# Guardar en GeoJSON
st_write(puntos_750, "resultados/puntos_750.geojson", driver = "GeoJSON", delete_dsn = TRUE)

# Re-cargar con el mismo nombre
puntos_750 <- st_read("resultados/puntos_750.geojson")

# Ver resultado
print(puntos_750)


# Cuenca visual -----------------------------------------------------------

# Crear objeto por punto
aerogenerador_1 <- st_coordinates(puntos_750 %>%
  filter(id == 1))
aerogenerador_2 <- st_coordinates(puntos_750 %>%
  filter(id == 2))
aerogenerador_3 <- st_coordinates(puntos_750 %>%
  filter(id == 3))
aerogenerador_4 <- st_coordinates(puntos_750 %>%
  filter(id == 4))
# Validar
# print(aerogenerador_1)

# calcular la cuenca visual # 1
visual1 <- viewshed(mde_recorte, loc = c(aerogenerador_1[1], aerogenerador_1[2]), observer = 60, target = 0, output = "yes/no")
visual1 <- ifel(visual1, 1, 0) # convertir los valores a 1/0
terra::plot(visual1)

# calcular la cuenca visual # 2
visual2 <- viewshed(mde_recorte, loc = c(aerogenerador_2[1], aerogenerador_2[2]), observer = 60, target = 0, output = "yes/no")
visual2 <- ifel(visual2, 1, 0) # convertir los valores a 1/0
terra::plot(visual2)

# calcular la cuenca visual # 3
visual3 <- viewshed(mde_recorte, loc = c(aerogenerador_3[1], aerogenerador_3[2]), observer = 60, target = 0, output = "yes/no")
visual3 <- ifel(visual3, 1, 0) # convertir los valores a 1/0
terra::plot(visual3)

# calcular la cuenca visual # 4
visual4 <- viewshed(mde_recorte, loc = c(aerogenerador_4[1], aerogenerador_4[2]), observer = 60, target = 0, output = "yes/no")
visual4 <- ifel(visual4, 1, 0) # convertir los valores a 1/0
terra::plot(visual4)

# Sumar los cuatro rasters
visual_acumulada <- visual1 + visual2 + visual3 + visual4

# Guardar el raster
crs(visual_acumulada) <- st_crs(cubierta_suelo_clean_join)$wkt # Tomar referencia de otro file
writeRaster(visual_acumulada, "resultados/visual_acumulada.tif", overwrite = TRUE)

# Visualizar

# Crear y abrir archivo de imagen
png("plots/2_acumulado_cuenca_visual.png", 
    width = 2560, 
    height = 1440, 
    units = "px", 
    res = 300)

# Raster acumulado
plot(visual_acumulada, main = "Acumulado de cuencas visuales")

# Municipios: solo borde, sin relleno
plot(municipios_clean, border = "white", col = NA, add = TRUE)

# Puntos: rellenos en rojo
plot(puntos_750, col = "red", bg = "red", pch = 21, add = TRUE)

# Guardar el archivo
dev.off()

# Análisis espacial y estadístico comarcal-----------------------------------------

# Calcular el valor medio de impacto por municipio
municipios_clean$impacto_medio <- terra::extract(visual_acumulada, 
                                                 municipios_clean, 
                                                 fun = mean, 
                                                 na.rm = TRUE)[,2] # Extraer columna con valores del df

# Crear el objeto final con ID secuencial y ordenado
impacto_municipios <- municipios_clean %>%
  mutate(id = row_number()) %>% # Crear ID
  select(nommuni, id, geometry, impacto_medio) %>% # Seleccionar columna
  arrange(desc(impacto_medio)) # Ordenar

# Visualizar resultado
View(impacto_municipios)

# Exportar a CSV
impacto_municipios %>%
  st_drop_geometry() %>%
  write_excel_csv("resultados/impacto_municipios.csv")

# Análisis espacial y estadístico municipal -------------------------------

# Crear objeto de municipio
municipio_estudio <- impacto_municipios %>%
  slice(1)

# Verificar el resultado
print(municipio_estudio)
plot(municipio_estudio$geom, border = "black", col = "grey")

# Recortar y enmascarar MDE
mde_recorte_municipio <- crop(mde_recorte, municipio_estudio, mask = TRUE)

# Crear y abrir archivo de imagen
png("plots/4_mde_recortado_municipio.png", 
    width = 2560, 
    height = 1440, 
    units = "px", 
    res = 300)
# Visualizar el resultado
plot(mde_recorte_municipio, main = paste("MDE de", municipio_estudio$nommuni))
# Guardar el archivo
dev.off()
# Guardar resultado
writeRaster(mde_recorte_municipio, "resultados/mde_recorte_municipio.tif", overwrite = TRUE)

# Rasterizar y procesar cubiertas -----------------------------------------

# Intersectar cubiertas con municipio
cubiertas_municipio <- st_intersection(cubierta_suelo_clean_join, municipio_estudio)
View(cubiertas_municipio)

# Se usa otro raster como plantilla (extensión y resolución)
cubiertas_raster <- rasterize(cubiertas_municipio, 
                              mde_recorte_municipio, 
                              field = "nivel_2") # Código de cubierta

# Visualizar
plot(cubiertas_raster, main = paste("Cubiertas de suelo:", municipio_estudio$nommuni))

# Exportar raser
writeRaster(cubiertas_raster, "resultados/cubiertas_raster_municipio.tif", overwrite = TRUE)

# Tabla de frecuencias de cubiertas ---------------------------------------

# Recortar y enmascarar raster
impacto_maximo_visual <- crop(visual_acumulada, municipio_estudio, mask = TRUE)
plot(impacto_maximo_visual)

# Filtrar por valor de impacto
impacto_maximo_visual_muni <- impacto_maximo_visual == 4
plot(impacto_maximo_visual_muni)

# Obtener código de cubierta: multiplicar código_cubierta * 1
cubiertas_impacto_maximo <- cubiertas_raster * impacto_maximo_visual_muni

# Calcular la frecuencia de píxeles y área
frecuencia_pixeles <- freq(cubiertas_impacto_maximo) %>%
  rename(CODIGO_CUBIERTA = value, N_PIXELES = count) %>%
  filter(!is.na(CODIGO_CUBIERTA) & CODIGO_CUBIERTA != 0) # Eliminar filas NA y 0's
View(frecuencia_pixeles)

# Calcular el área de un solo píxel en m2
res_m <- res(visual_acumulada)[1] # Desde el CRS
area_pixel_m2 <- (res_m * res_m)
print(area_pixel_m2)

# Unir tablas y validar
tabla_frecuencias <- frecuencia_pixeles %>%
  mutate(
    ID = row_number()) %>% 
  mutate(
    AREA_HA = (N_PIXELES * area_pixel_m2)/10000
  ) %>% 
  left_join(
    df_cubierta_tabla_clean %>% 
      select(CODIGO_CUBIERTA = nivel_2, CATEGORIA = categoria), 
    by = "CODIGO_CUBIERTA"
  ) %>% 
  select(ID, CODIGO_CUBIERTA, CATEGORIA, AREA_HA)

# Validar  
print(tabla_frecuencias)
View(tabla_frecuencias)

# Exportar a CSV
tabla_frecuencias %>%
  write_excel_csv("resultados/tabla_frecuencia_cubierta.csv")

# Descargar datos de CatastRo ---------------------------------------------

# Convertir raster impacto a vector y filtrar
# names(impacto_maximo_visual_muni)
impacto_pol <- as.polygons(impacto_maximo_visual_muni) %>% 
  st_as_sf() %>% 
  filter(viewshed == 1) # viewshed es el nombre de la columna

# Validar
plot(impacto_pol$geom, border = "black", col = "grey") # Mapa estático
# View(impacto_pol)
# crs(impacto_pol)

# Crear una rejilla de 100m x 100m (1km2) sobre el área de impacto
grid <- st_make_grid(impacto_pol, cellsize = 100, square = TRUE) %>% 
  st_as_sf() %>%
  st_filter(impacto_pol, .predicate = st_intersects) # Filtrar grillas solapadas

# Visualizar mapa
mapview(grid) +
  mapview(impacto_pol, color = "red")

# Descargar de CatastRo

# Máximo de iteraciones (celdas)
n_iter <- nrow(grid) # Útil para hacer test

# Función iterada
descargar_y_validar <- function(i) {
  message(paste0("Celda ", i, " de ", n_iter, "...")) # Mostrar celda ejecutada
  bbox_celda <- st_bbox(grid[i, ]) # El extent
  
  parcelas <- tryCatch({
    catr_wfs_get_parcels_bbox(bbox_celda, srs = 25831)
  }, error = function(e) {
    message(paste0("Error en celda ", i, ": ", e$message))
    return(NULL)
  })
  
  Sys.sleep(0.2) # Pausar para no saturar el servicio 
  return(parcelas)
}

# Iterar solo hasta el número definido
max_celdas <- min(n_iter, nrow(grid)) # iteraciones = row_number
# Aplicar función
lista_capas_parcelas <- map(seq_len(max_celdas), descargar_y_validar)

# Unir capas descargadas
todas_parcelas <- bind_rows(lista_capas_parcelas)
print(paste("Entidades descargadas:", nrow(todas_parcelas)))
# Limpieza de archivo (conservar valores únicos)
parcelas_final <- unique(todas_parcelas)
print(paste("Entidades limpias:", nrow(parcelas_final)))

# Validar
# crs(parcelas_final)
View(parcelas_final)

# Transformar y guardar
parcela_afectada <- st_transform(parcelas_final, 25831)
st_write(parcela_afectada, "resultados/parcela_afectada.geojson", driver = "GeoJSON", delete_dsn = TRUE)

# Crear plot de parcelas afectadas ----------------------------------------

# Crear y abrir archivo de imagen
png("plots/7_parcela_afectada.png", 
    width = 1840, 
    height = 1440, 
    units = "px", 
    res = 300)

# Plot con título principal
plot(st_geometry(municipio_estudio), 
     border = "grey", 
     lwd = 1.5, # Ancho de borde
     main = "Parcelas afectadas con impacto visual máximo",
     axes= TRUE,
     cex.axis = 0.7) # Controlar el tamaño de letra

# Añadir parcelas afectadas
plot(st_geometry(parcelas_final), 
     border = "black", 
     lwd = 0.5, 
     col = "#E0E0FF", # Color
     add = TRUE)

# Añadir las zonas de impacto
plot(st_geometry(impacto_pol), 
     border = NA, # Sin borde
     col = "red", 
     add = TRUE)

legend("topleft", 
       legend = c("Parcela afectada", "Zonas de impacto", "Límite municipal"),
       fill = c("#E0E0FF", "red", "grey"),
       cex = 0.75, # Tamaño de la fuente
)
# Guardar el archivo
dev.off()

# Crear objeto lista de códigos catastrales -------------------------------

# names(parcelas_final)
lista_codigos <- list(codigo = parcelas_final$nationalCadastralReference)
print(lista_codigos)

# Guardar los objetos de la sesión R --------------------------------------
save.image(file=".RData")
