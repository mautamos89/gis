-----------------------------
--TABLA: TKINTER APP PYTHON--
-----------------------------

--EXPORTAR PARA TKINTER APP A CSV--
copy(
select ide.id_predio,ide.npn,ide.direccion,ide.sesemanlad,ide.est_def,ide.tipo_est,ide.est_atipes,pnt.lat_y,pnt.lon_x
from tab_pnt_pre_wgs84 as pnt
right join est_bd_maestra_20230630 as ide
on ide.idterreno=pnt.idterreno
order by ide.id_predio)
to 'd:\bdmas_2023-08-01.csv' delimiter '|' encoding 'latin1' null as ''
;

--EXPORTAR REPORTE MENSUAL A CSV--
copy(
select est_def as estrato,count(id_predio) as predios from est_bd_maestra_20230630 group by est_def order by est_def) to
'd:\bdmas_reporte_mes.csv' delimiter '|' csv header
;

--CALCULAR CENTROIDE COMO GEOMETRÍA Y OBTENER TABLA COORDENADAS DENTRO DE POLÍGONO—
SELECT st_x(st_pointonsurface(geom)), st_y(st_pointonsurface(geom)), st_pointonsurface(geom) as geom
FROM cat_terrenos_magna;

--CALCULAR CENTROIDE COMO GEOMETRÍA Y TRANSFORMAR COORDENADAS DE 6249 A WGS84 GRADOS DECIMALES--
SELECT conexion,
	   --st_x(st_pointonsurface(geom)) as x,
	   --st_y(st_pointonsurface(geom)) as y,
       round(st_y(st_transform(st_pointonsurface(geom),4326))::numeric,5) as lat,
	   round(st_x(st_transform(st_pointonsurface(geom),4326))::numeric,5) as lon
	   --st_pointonsurface(geom) as geom
FROM geo_terrenos
WHERE char_length(conexion) in (12)
ORDER BY conexion asc;

--QUERYS DE TKINTER ESTRATO APP: # 1 DICCIONARIO DE DATOS
select ide.id_predio,ide.npn,ide.direccion,ide.sesemanlad,ide.est_def,ide.tipo_est,ide.est_atipes,
	   round(st_y(st_transform(st_pointonsurface(geom),4326))::numeric,5) as lat_y,round(st_x(st_transform(st_pointonsurface(geom),4326))::numeric,5) as lon_x
from geo_terrenos as pnt
right join est_bd_maestra_20231031 as ide
on ide.idterreno=pnt.conexion
order by ide.id_predio
--limit 10
;

--QUERY DICCIONARIO #2 EN IDESC [CATASTRO: ALFA-CARTO]
select ide.id_predio,ide.npn,ide.direpred,
	   round(st_y(st_transform(st_pointonsurface(the_geom),4326))::numeric,5) as lat_y,round(st_x(st_transform(st_pointonsurface(the_geom),4326))::numeric,5) as lon_x
from cat_bas_terrenos as pnt
right join dat_cat_bas_catastral as ide
on ide.idterreno=pnt.conexion
--order by ide.id_predio
where ide.id_predio = 406
limit 10
;

--QUERYS DE TKINTER ESTRATO APP: # 2 DICCIONARIO DE REPORTE MENSUAL
select est_def as estrato,count(id_predio) as predios
from est_bd_maestra_20231031
group by est_def
order by est_def
;

--DBLINK WORKING ENTRE BASES DE DATOS
select terlink.conexion,terlink.munipred from dblink('dbname=postgis_default port=5432 host=localhost user=postgres password=postgres'::text,
		'select conexion,munipred from public.geo_terrenos'::text) as terlink(
		conexion varchar(15),
		munipred varchar(3))
limit 10;

--DBLINK WORKING ENTRE BASES DE DATOS GEOGRÁFICO
select terlink.conexion,terlink.lat_y,terlink.lon_x from dblink('dbname=postgis_default port=5432 host=localhost user=postgres password=postgres'::text,
		'select conexion,round(st_y(st_transform(st_pointonsurface(geom),4326))::numeric,5) as lat_y,
		round(st_x(st_transform(st_pointonsurface(geom),4326))::numeric,5) as lon_x from public.geo_terrenos'::text) as terlink(
		conexion varchar(15),
		lat_y numeric,
		lon_x numeric)
limit 10;

--DBLINK WORKING ENTRE BASES DE DATOS GEOGRÁFICO
select ide.id_predio,ide.npn,ide.direccion,ide.sesemanlad,ide.est_def,ide.tipo_est,ide.est_atipes,
	   pnt.lat_y as lat_y,pnt.lon_x as lon_x
from est_bd_maestra_20231031 as ide
right join(
		select terlink.conexion,terlink.lat_y,terlink.lon_x
		from dblink('dbname=postgis_default port=5432 host=localhost user=postgres password=postgres'::text,
		'select conexion,round(st_y(st_transform(st_pointonsurface(geom),4326))::numeric,5) as lat_y,
		round(st_x(st_transform(st_pointonsurface(geom),4326))::numeric,5) as lon_x from public.geo_terrenos'::text) as terlink(
		conexion varchar(15),
		lat_y numeric,
		lon_x numeric)
		) as pnt
on ide.idterreno=pnt.conexion
where ide.id_predio = 1
order by ide.id_predio
limit 10
;



--FUNCIÓN PARA CREAR USER EDIT--
CREATE OR REPLACE FUNCTION update_user_edit() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.user_edit = (SELECT USER);
    RETURN NEW; 
END;
$$ language 'plpgsql';
--CREAR ACTIVADOR--
CREATE TRIGGER update_test_user_edit BEFORE UPDATE ON test FOR EACH ROW EXECUTE PROCEDURE  update_user_edit();

--FUNCIÓN PARA CREAR FECHA EDIT--
CREATE OR REPLACE FUNCTION update_edit_time() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_edit = NOW();
    RETURN NEW; 
END;
$$ language 'plpgsql';
--CREAR ACTIVADOR--
CREATE TRIGGER update_test_fecha_edit BEFORE UPDATE ON test FOR EACH ROW EXECUTE PROCEDURE  update_edit_time();

--DEFINIR ROLES A TABLAS--
--CREAR USUARIO CON ROL PREDEFINIDO O NINGUNO--
revoke all on test from sql_read_test;
grant select, update, insert,delete on test to sql_read_test;
