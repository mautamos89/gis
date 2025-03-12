-- Crear la DB
CREATE DATABASE practica4
  ENCODING = 'UTF8';

-- Crear la extensión postgis
CREATE EXTENSION postgis;

-- Crear el archivo sql para importar el shapefile
-- .\shp2pgsql.exe -s 4326 -I "D:\msc\3_bases_datos_espaciales\practica_4\shp\municipios" municipio > "D:\msc\3_bases_datos_espaciales\practica_4\municipio.sql"
-- Ejecutar en PostgreSQL el archivo creado

-- Ejecutar archvo Comandos.sql para estructurar relaciones

-- Importar datos de forma masiva
-- Primero relaciones con clave externa
copy estacion_a from 'D:\msc\3_bases_datos_espaciales\practica_4\estaciones_a.csv' delimiter ',' csv header;
copy estacion_m from 'D:\msc\3_bases_datos_espaciales\practica_4\estacion_m.csv' delimiter ',' csv header;
copy variable from 'D:\msc\3_bases_datos_espaciales\practica_4\variables.csv' delimiter ',' csv header;
-- Segundo relaciones con referencia a clave externa
copy comarca from 'D:\msc\3_bases_datos_espaciales\practica_4\comarca.csv' delimiter e'\t' csv header; -- Delimitado por tabulación
copy datos_aire(codigo_estacion, fecha, contaminante, unidades, valor)
from 'D:\msc\3_bases_datos_espaciales\practica_4\datos_aire.csv' delimiter ',' csv header;
copy datos_meteo(codigo_estacion, codigo_variable, fecha_lectura, valor_lectura)
from 'D:\msc\3_bases_datos_espaciales\practica_4\datos_meteo.csv' delimiter ',' csv header;

-- Validar registros importados
select * from municipio order by gid asc;
select * from estacion_a;
select * from estacion_m;
select * from variable;
select * from comarca;
select * from datos_aire limit 5;
select * from datos_meteo limit 5;

-- Añadir columna geometría
alter table estacion_m add column geom geometry(point, 4326); -- Definir el tipo de geometría y el SRID
alter table estacion_a add column geom geometry(point, 4326);

-- Crear geometría de tipo punto
update estacion_m set geom = st_setsrid(st_makepoint(longitud, latitud),4326);
update estacion_a set geom = st_setsrid(st_makepoint(longitud, latitud),4326);

-- índices para optimizar consultas geográficas
create index idx_estacion_a_geom on estacion_a using gist(geom);
create index idx_estacion_m_geom on estacion_m using gist(geom);

-- Solución

-- 1. Obtener un listado con los valores de ozono superiores a 180 µg/m3.
-- El listado debe contener, como mínimo, la fecha de la medición, la estación y las coordenadas de la estación.

-- select * from datos_aire where contaminante in ('O3') and valor >= 180;
-- select * from estacion_a where codigo = '8298008';

select datos_aire.codigo_estacion, estacion_a.nombre, datos_aire.fecha, datos_aire.contaminante,
datos_aire.valor, datos_aire.unidades, estacion_a.latitud, estacion_a.longitud, estacion_a.geom 
from (datos_aire
	  inner join estacion_a on datos_aire.codigo_estacion=estacion_a.codigo)
where contaminante in ('O3') and valor >= 180;

-- 2. Obtener un listado con los valores máximos y mínimos de la tabla datos_meteo para cada variable
-- (temperatura, precipitación, presión atmosférica máxima, etc.)

-- select * from datos_meteo limit 10;
-- select distinct codigo_variable from datos_meteo;
-- select * from variable order by codigo;
-- select codigo_variable, avg(valor_lectura), min(valor_lectura), max(valor_lectura) from datos_meteo group by codigo_variable;

select datos_meteo.codigo_variable, variable.variable, variable.unidad, min(datos_meteo.valor_lectura),
max(datos_meteo.valor_lectura), avg(datos_meteo.valor_lectura) as promedio
from (datos_meteo
	  inner join variable on datos_meteo.codigo_variable=variable.codigo)
group by codigo_variable,variable, unidad;

-- 3. Obtener un listado de todas las precipitaciones DIARIAS de cada estación ordenadas por fecha.
-- En el listado final, cada estación debe aparecer UNA SOLA VEZ PARA CADA DÍA.
-- Cualquier información adicional útil será valorada positivamente.

-- select * from variable where variable ilike '%preci%' order by codigo;
-- select * from datos_meteo where codigo_variable = 35 and valor_lectura <> 0 order by codigo_estacion asc, fecha_lectura asc;
-- select * from estacion_m where codigo = 'XT';

select datos_meteo.codigo_estacion,estacion_m.nombre, variable.variable,variable.unidad,datos_meteo.fecha_lectura::date as fecha,
sum(datos_meteo.valor_lectura) as precipitacion_diaria, estacion_m.latitud,estacion_m.longitud, estacion_m.geom
from ((datos_meteo
	   inner join variable on datos_meteo.codigo_variable=variable.codigo)
	   inner join estacion_m on datos_meteo.codigo_estacion=estacion_m.codigo)
where codigo_variable = 35 and datos_meteo.valor_lectura > 0
group by codigo_estacion,nombre,fecha,variable.variable,variable.unidad,estacion_m.latitud,estacion_m.longitud, estacion_m.geom
order by codigo_estacion asc, fecha asc;

-- 4. Municipio de cada comarca con mayor precipitación total acumulada.
-- La precipitación total acumulada de cada municipio se calculará como
-- la suma de todas las precipitaciones acumuladas de las estaciones que pertenecen a ese municipio
-- dividido por el número de estaciones que se encuentran dentro de ese mismo municipio.

-- select * from comarca order by codigo asc;
-- select * from municipio order by codigo_com desc;

select distinct on (municipio.codigo_com)
-- select
  municipio.codigo as cod_muni, municipio.nombre as nom_muni, municipio.codigo_com as cod_comarca,
  sum(datos_meteo.suma_prep) as suma_prep, count(estacion_m.codigo) as num_estacion,
  sum(datos_meteo.suma_prep) / count(estacion_m.codigo) as precipitacion_total, municipio.geom
from
  municipio
  join estacion_m on st_intersects(municipio.geom, estacion_m.geom)
  left join (
    select estacion_m.codigo, sum(datos_meteo.valor_lectura) as suma_prep
    from estacion_m
    join datos_meteo on estacion_m.codigo = datos_meteo.codigo_estacion
    where datos_meteo.codigo_variable = 35
    group by estacion_m.codigo
  ) datos_meteo on estacion_m.codigo = datos_meteo.codigo
-- where municipio.codigo_com  = '13'
group by municipio.codigo, municipio.nombre, municipio.codigo_com, municipio.geom
order by municipio.codigo_com asc, precipitacion_total desc;

-- 5. Obtener un listado en el que aparezcan todas las comarcas junto con la estación, dentro de cada comarca,
-- que ha tenido más precipitaciones en el mes de agosto. El listado final debe mostrar el nombre de cada comarca,
-- el nombre de la estación y la precipitación acumulada durante el mes de agosto para esa estación.
-- Las comarcas que no tengan estaciones o que no hayan registrado ninguna precipitación pueden, o no, aparecer en el listado.

-- select * from comarca order by codigo asc;
-- select * from municipio order by codigo_com desc;
-- select * from estacion_m limit 5;
-- select * from datos_meteo where codigo_variable = 35 order by codigo_estacion asc, fecha_lectura asc;

select distinct on (comarca.codigo)
    comarca.codigo as codigo_com, comarca.nombre as comarca, estacion_m.codigo as codigo_est, estacion_m.nombre as estacion,
    sum(datos_meteo.valor_lectura) as precipitacion_acumulada, estacion_m.geom
from (((comarca
		inner join municipio on comarca.codigo = municipio.codigo_com)
	  inner join estacion_m on st_intersects(municipio.geom, estacion_m.geom))
	  inner join datos_meteo on estacion_m.codigo = datos_meteo.codigo_estacion)
where 
    datos_meteo.codigo_variable = 35
group by 
    comarca.codigo, comarca.nombre, estacion_m.codigo, estacion_m.nombre, estacion_m.geom
order by 
    comarca.codigo, precipitacion_acumulada desc;
