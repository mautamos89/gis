---------------------------------------------------
--REPORTE ENTRE TABLAS CATASTRO Y ESTRATIFICACIÓN--
---------------------------------------------------

--------------------------------------------------
--TABLA: BASE_MAESTRA | GEO_EST_RURAL | ES_RURAL--
--------------------------------------------------

--COMPARAR VALOR NPN ENTRE BASE_MAESTRA <> GEO_EST_RURAL <> ES_RURAL
select ide.id_predio as bdm_id_predio,ide.npn as bdm_npn,ide.est_def as bdm_est_def,rur.eridpredio::integer as rur_id_predio,rur.ernpn as rur_npn,rur.erestrato as rur_estrato,es.id_predio as es_id_predio,es.npn as es_npn,es.estrato as es_estrato
from ((est_bd_maestra_20231031 as ide
left join pdt_est_estrato_rural as rur
on ide.id_predio=rur.eridpredio)
left join est_es_rural_202308 as es
on ide.id_predio=es.id_predio)
where ide.npn <> rur.ernpn or ide.npn <> es.npn
;

-----------------------------------------------
--TABLA: BASE_MAESTRA_ALFA | BASE_MAESTRA_GEO--
-----------------------------------------------

--COMPARAR VALORES ENTRE BASE MAESTRA ALFA <> BASE MAESTRA GEO
select geo.id_predio as geo_id_predio,geo.npn as geo_npn, geo.comuna as geo_comuna, geo.barrio as geo_barrio, geo.manzana as geo_manzana,geo.condicion as geo_condicion,geo.direccion as geo_direccion,geo.seseman as geo_seseman,geo.lado as geo_lado,geo.sesemanlad as geo_sesemanlad,geo.estrato as geo_estrato,geo.tipo_est as geo_tipo_est,geo.uso_princi as geo_uso_princi,geo.destino_ec as geo_destino_ec, geo.revlad as geo_revlad,
alf.id_predio as alf_id_predio,alf.npn as alf_npn,alf.condicion as alf_condicion,alf.direccion as alf_direccion,alf.seseman as alf_seseman,alf.lado as alf_lado,alf.sesemanlad as alf_sesemanlad,alf.estrato as alf_estrato,alf.tipo_est as alf_tipo_est,alf.uso_princi as alf_uso_princi,alf.destino_ec as alf_destino_ec
from (tab_alf as alf
left join tab_geo as geo
on alf.id_predio=geo.id_predio)
where (alf.npn <> geo.npn or alf.comuna <> geo.comuna or alf.barrio <> geo.barrio or alf.manzana <> geo.manzana or alf.direccion <> alf.direccion or alf.seseman <> geo.seseman or alf.lado not in (geo.lado) or geo.lado not in (alf.lado) or alf.sesemanlad <> geo.sesemanlad or alf.estrato <> geo.estrato
or alf.tipo_est <> geo.tipo_est or alf.uso_princi <> geo.uso_princi or alf.destino_ec <> geo.destino_ec) and geo.revlad not in (8)
;


---------------------------------------
--TABLA: BASE_MAESTRA_ALFA | ES_RURAL--
---------------------------------------
--SELECCIONAR PREDIOS RETIRADOS ENTRE BD_MAS<>ES_RURAL
select rur.id_predio,rur.npn,rur.estrato
from (est_bd_maestra_20231130 as ide
full join est_es_rural_202311 as rur on rur.id_predio=ide.id_predio)
where rur.id_predio is not null and ide.id_predio is null
order by rur.id_predio
;


----------------------------------------------------
--ESTADÍSTICAS TABLA: BASE_MAESTRA | ESTRATOPREDIO--
----------------------------------------------------
--SELECCIONAR PREDIOS DIFERENTES CON ESTRATO EST_ESTRATOPREDIO
select count(distinct idpredio) as "Predios", estratoactual as "Estrato" from est_estratopredio group by estratoactual;
--SELECCIONAR PREDIOS DIFERENTES CON ESTRATO EST_BD_MAESTRA
select count(distinct id_predio) as "Predios", est_def as "Estrato" from est_bd_maestra_20231229 group by est_def;


--------------------------------------------------------------------------
--TABLA: BASE_MAESTRA | LISTADO DE LADOS, PREDIOS Y ESTRATOS PARA RENTAS--
--------------------------------------------------------------------------
select distinct count(id) as predios,sesemanlad as lados, est_def as estrato_def, idterreno, fecha_edit
from est_bd_maestra_20231229
where idterreno in ('177500660002','177500010001','177500030001','059800700001','059400170002','059500040768','177500040001','081800010012','177400500001','059800690001','019900290840','189100050004','189100050008')
group by lados, est_def, idterreno, fecha_edit
--order by idterreno asc, lados asc
order by predios desc
;

---------------------------------------------------------
--TABLA: BASE_MAESTRA | GEOGRAFICA | LISTADO RENTAS 12K--
---------------------------------------------------------
--ALFANUMERICA OK--
select ide.id_predio as id_predio_ide,ide.npn as npn_ide,ide.est_def,ide.sesemanlad,ide.idterreno,ide.fecha_edit
from est_bd_maestra_20240216 as ide
right join info_bd_12k as info
on info.id_predio=ide.id_predio
where ide.est_def in ('8','9') and info.numero_pre = ide.npn-- and char_length(ide.sesemanlad) = 9
order by ide.est_def asc, ide.sesemanlad asc
;
--CSV--
copy(
select ide.id_predio as id_predio_ide,ide.npn as npn_ide, info.numero_pre as npn_cat,ide.est_def,ide.fecha_edit,ide.sesemanlad
from est_bd_maestra_20240216 as ide
right join info_bd_12k as info
on info.id_predio=ide.id_predio
where ide.est_def not in ('8','9') and info.numero_pre = ide.npn
order by ide.est_def asc, ide.sesemanlad asc) to
'd:/info_bd_ok.csv' delimiter '=' csv header
;
--ALFANUMERICA REV--
select ide.id_predio as id_predio_ide,ide.npn as npn_ide,ide.est_def,ide.sesemanlad,ide.idterreno,ide.fecha_edit
from est_bd_maestra_20240216 as ide
right join info_bd_12k as info
on info.id_predio=ide.id_predio
where ide.est_def in ('8','9') and info.numero_pre = ide.npn-- and char_length(ide.sesemanlad) = 9
order by ide.est_def asc, ide.sesemanlad asc
;
--CSV--
copy(
select ide.id_predio as id_predio_ide,ide.npn as npn_ide,ide.est_def,ide.sesemanlad,ide.idterreno,ide.fecha_edit
from est_bd_maestra_20240216 as ide
right join info_bd_12k as info
on info.id_predio=ide.id_predio
where ide.est_def in ('8','9') and info.numero_pre = ide.npn-- and char_length(ide.sesemanlad) = 9
order by ide.est_def asc, ide.sesemanlad asc) to
'd:/info_bd_rev.csv' delimiter '=' csv header
;

--GEOGRAFICA--
select ide.id_predio as id_predio_ide,ide.npn as npn_ide,ide.est_def,ide.sesemanlad,ide.idterreno,ide.fecha_edit, geo.geom 
from est_bd_maestra_20240216 as ide
right join info_bd_12k as info
on info.id_predio=ide.id_predio
right join geo_terrenos as geo
on ide.idterreno=geo.conexion
where ide.est_def in ('8','9') and info.numero_pre = ide.npn-- and char_length(ide.sesemanlad) = 9
order by ide.est_def asc, ide.sesemanlad asc
;
--CSV--
copy
(select ide.id_predio as id_predio_ide,ide.npn as npn_ide,ide.est_def,ide.sesemanlad,ide.idterreno,ide.fecha_edit--, geo.geom 
from est_bd_maestra_20240216 as ide
right join info_bd_12k as info
on info.id_predio=ide.id_predio
right join geo_terrenos as geo
on ide.idterreno=geo.conexion
where ide.est_def in ('8','9') and info.numero_pre = ide.npn-- and char_length(ide.sesemanlad) = 9
order by ide.est_def asc, ide.sesemanlad asc) to
'd:/info_bd_geo.csv' delimiter '=' csv header
;