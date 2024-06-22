----------------------------
--TABLA: EST_ESTRATOPREDIO--
----------------------------
--SELECCIONAR PREDIOS RETIRADOS BDMAS<>EST_ESTRATOPREDIO--
select pre.idprediocatastro as idprediocatastro,pre.codigounico as npn, sau.idpredio,sau.idestratopredio,sau.activa,sau.estratoanterior,sau.estratoactual,sau.updated_at
from ((est_bd_maestra_20231130 as ide
full join predio as pre on ide.id_predio=pre.idprediocatastro)
full join est_estratopredio as sau on pre.idpredio=sau.idpredio)
where ide.id_predio is null and sau.idpredio is not null and sau.estratoactual <> '-'
order by pre.idprediocatastro asc
;

--EXPORTAR PREDIOS RETIRADOS BDMAS<>EST_ESTRATOPREDIO--
copy (select pre.idprediocatastro as idprediocatastro,pre.codigounico as npn, sau.idpredio,sau.idestratopredio,sau.activa,sau.estratoanterior,sau.estratoactual,sau.updated_at
from ((est_bd_maestra_20231130 as ide
full join predio as pre on ide.id_predio=pre.idprediocatastro)
full join est_estratopredio as sau on pre.idpredio=sau.idpredio)
where ide.id_predio is null and sau.idpredio is not null and sau.estratoactual <> '-'
order by pre.idprediocatastro asc) to
'd:\upt_est_retirado_estratopredio_20231229.csv' delimiter '|' csv header
;

--SELECCIONAR ESTRATOS DIFERENTES BDMAS<>EST_ESTRATOPREDIO: ACTIVOS--
select ide.id_predio as id_prediocat, ide.npn,ide.est_def,ide.tipo_est,ide.sesemanlad,ide.fecha_edit,sau.idpredio,sau.idestratopredio,sau.activa,sau.estratoanterior,sau.estratoactual,sau.updated_at,pre.idprediocatastro,pre.codigounico,pre.idpredio as idpredio_datic
from ((est_bd_maestra_20231130 as ide
full join predio as pre on ide.id_predio=pre.idprediocatastro)
full join est_estratopredio as sau on pre.idpredio=sau.idpredio)
where ide.est_def <> sau.estratoactual and sau.activa = '1' and (ide.est_def not in ('8','9') or sau.estratoactual <> '-')
order by ide.id_predio--ide.sesemanlad--ide.id_predio
--limit 500
;

--EXPORTAR ESTRATOS DIFERENTES BDMAS<>EST_ESTRATOPREDIO: ACTIVOS--
copy (select ide.id_predio as id_prediocat, ide.npn,ide.est_def,ide.tipo_est,ide.sesemanlad,ide.fecha_edit,sau.idpredio,sau.idestratopredio,sau.activa,sau.estratoanterior,sau.estratoactual,sau.updated_at
from ((est_bd_maestra_20231130 as ide
full join predio as pre on ide.id_predio=pre.idprediocatastro)
full join est_estratopredio as sau on pre.idpredio=sau.idpredio)
where ide.est_def <> sau.estratoactual and sau.activa = '1' and (ide.est_def not in ('8','9') or sau.estratoactual <> '-')
order by ide.id_predio) to
'd:\upt_est_activo_estratopredio_20231229.csv' delimiter '|' csv header
;

--SELECCIONAR ESTRATOS 8 Y 9 CON ESTRATO EN EST_ESTRATOPREDIO: ACTIVOS--
select ide.id_predio as id_prediocat, ide.npn,ide.est_def,ide.tipo_est,ide.sesemanlad,ide.fecha_edit,sau.idpredio,sau.idestratopredio,sau.activa,sau.estratoanterior,sau.estratoactual,sau.updated_at,pre.idpredio,pre.codigounico
from ((est_bd_maestra_20231130 as ide
full join predio as pre on ide.id_predio=pre.idprediocatastro)
full join est_estratopredio as sau on pre.idpredio=sau.idpredio)
where ide.est_def not in (sau.estratoactual) and sau.activa = '1' and ide.tipo_est in ('8','9')-- and sau.estratoactual not in ('0')
order by ide.id_predio--ide.sesemanlad--ide.id_predio
;

--SELECCIONAR ESTRATOS DIFERENTES BDMAS<>ESTRATOPREDIO: ACTIVOS [LLAVE: NPN]--
select ide.id_predio as id_prediocat, ide.npn,ide.est_def,ide.tipo_est,ide.sesemanlad,ide.fecha_edit,sau.idpredio,sau.idestratopredio,sau.activa,sau.estratoanterior,sau.estratoactual,sau.updated_at,pre.idprediocatastro,pre.codigounico,pre.idpredio as idpredio_datic
from ((est_bd_maestra_20231130 as ide
full join predio as pre on ide.npn=pre.codigounico)
full join est_estratopredio as sau on pre.idpredio=sau.idpredio)
where ide.est_def <> sau.estratoactual and sau.activa = '1' and (ide.est_def not in ('8','9') or sau.estratoactual <> '-')
order by ide.id_predio
;

--EXPORTAR ESTRATOS DIFERENTES BDMAS<>ESTRATOPREDIO: ACTIVOS [LLAVE: NPN]--
copy (select ide.id_predio as id_prediocat, ide.npn,ide.est_def,ide.tipo_est,ide.sesemanlad,ide.fecha_edit,sau.idpredio,sau.idestratopredio,sau.activa,sau.estratoanterior,sau.estratoactual,sau.updated_at
from ((est_bd_maestra_20231130 as ide
full join predio as pre on ide.npn=pre.codigounico)
full join est_estratopredio as sau on pre.idpredio=sau.idpredio)
where ide.est_def <> sau.estratoactual and sau.activa = '1' and (ide.est_def not in ('8','9') or sau.estratoactual <> '-')
order by ide.id_predio) to
'd:\upt_est_activo_npn_estratopredio_20231229.csv' delimiter '|' csv header
;

--SELECCIONAR ESTRATOS DIFERENTES BDMAS<>EST_ESTRATOPREDIO: INACTIVOS (HAY REPETIDOS)--
select ide.id_predio as id_prediocat, ide.npn,ide.est_def,ide.tipo_est,ide.sesemanlad,ide.fecha_edit,sau.idpredio,sau.idestratopredio,sau.activa,sau.estratoanterior,sau.estratoactual,sau.updated_at,pre.idpredio,pre.codigounico
from ((est_bd_maestra_20231130 as ide
full join predio as pre on ide.id_predio=pre.idprediocatastro)
full join est_estratopredio as sau on pre.idpredio=sau.idpredio)
where ide.est_def <> sau.estratoactual and sau.activa = '0'
order by ide.id_predio--ide.sesemanlad--ide.id_predio
--limit 500
;

--EXPORTAR ESTRATOS DIFERENTES BDMAS<>EST_ESTRATOPREDIO: INACTIVOS (HAY REPETIDOS)--
copy (select ide.id_predio as id_prediocat, ide.npn,ide.est_def,ide.tipo_est,ide.sesemanlad,ide.fecha_edit,sau.idpredio,sau.idestratopredio,sau.activa,sau.estratoanterior,sau.estratoactual,sau.updated_at
from ((est_bd_maestra_20231130 as ide
full join predio as pre on ide.id_predio=pre.idprediocatastro)
full join est_estratopredio as sau on pre.idpredio=sau.idpredio)
where ide.est_def <> sau.estratoactual and sau.activa = '0'
order by ide.id_predio) to
'd:\upt_est_inactivo_estratopredio_20231229.csv' delimiter '|' csv header
;

--SELECCIONAR ESTRATOS DIFERENTES BDMAS<>ESTRATOPREDIO: INACTIVOS [LLAVE: NPN]--
select ide.id_predio as id_prediocat, ide.npn,ide.est_def,ide.tipo_est,ide.sesemanlad,ide.fecha_edit,sau.idpredio,sau.idestratopredio,sau.activa,sau.estratoanterior,sau.estratoactual,sau.updated_at,pre.idprediocatastro,pre.codigounico,pre.idpredio as idpredio_datic
from ((est_bd_maestra_20231130 as ide
full join predio as pre on ide.npn=pre.codigounico)
full join est_estratopredio as sau on pre.idpredio=sau.idpredio)
where ide.est_def <> sau.estratoactual and sau.activa = '0'
order by ide.est_def
;

--EXPORTAR ESTRATOS DIFERENTES BDMAS<>ESTRATOPREDIO: INACTIVOS [LLAVE: NPN]--
copy (select ide.id_predio as id_prediocat, ide.npn,ide.est_def,ide.tipo_est,ide.sesemanlad,ide.fecha_edit,sau.idpredio,sau.idestratopredio,sau.activa,sau.estratoanterior,sau.estratoactual,sau.updated_at
from ((est_bd_maestra_20231130 as ide
full join predio as pre on ide.npn=pre.codigounico)
full join est_estratopredio as sau on pre.idpredio=sau.idpredio)
where ide.est_def <> sau.estratoactual and sau.activa = '0'
order by ide.est_def) to
'd:\upt_est_inactivo_npn_estratopredio_20231229.csv' delimiter '|' csv header
;

--SELECCIONAR PREDIOS INEXISTENTES BDMAS<>EST_ESTRATOPREDIO--
select id_predio as id_prediocat, npn,est_def,estra_ant,tipo_est,sesemanlad,fecha_edit,sau.idpredio,sau.idestratopredio,activa,estratoanterior,estratoactual,sau.updated_at,pre.idpredio,pre.codigounico
from ((est_bd_maestra_20231031 as ide
full join predio as pre on ide.id_predio=pre.idprediocatastro)
full join est_estratopredio as sau on pre.idpredio=sau.idpredio)
--where ide.sesemanlad = '01020050B' and ide.tipo_est not in ('8','9')
where ide.id_predio is not null and sau.idpredio is null and pre.idpredio is not null and ide.tipo_est not in ('8','9')
order by ide.id_predio--ide.sesemanlad--ide.id_predio
;

--EXPORTAR A CSV PREDIOS INEXISTENTES BDMAS<>EST_ESTRATOPREDIO--
copy(select id_predio as id_prediocat,npn,est_def,tipo_est,sesemanlad,sau.estratoactual,pre.idpredio
from ((est_bd_maestra_20231031 as ide
full join predio as pre on ide.id_predio=pre.idprediocatastro)
full join est_estratopredio as sau on pre.idpredio=sau.idpredio)
where ide.id_predio is not null and sau.idpredio is null and pre.idpredio is not null and ide.tipo_est not in ('8','9')
order by ide.id_predio) to
--order by ide.sesemanlad) to
'd:\ins_pre_estratopred_20231031.csv' delimiter '|' csv header
;


--SELECCIONAR LOS ÚLTIMOS REGISTROS EN EST_ESTRATOPREDIO--

select sau.idestratop,sau.estratoant,sau.estratoact,sau.activa,sau.idpredio,sau.created_at,sau.updated_at
from est_estratopredio as sau
order by
idestratop desc
limit 20
;



--SELECCIONAR CUENTA DE REPETIDOS EN EST_ESTRATOPREDIO--

select idpredio,count(*)
from est_estratopredio
group by idpredio
having count(*)>1
order by count desc
;



--SELECCIONAR REGISTROS REPETIDOS EN EST_ESTRATOPREDIO--
select sau.idestratop,sau.estratoant,sau.estratoact,sau.activa,sau.idpredio,sau.created_at,sau.updated_at,b.count,pre.idpredioca,ide.npn,ide.est_def,ide.tipo_est--sau.*
from (((est_estratopredio as sau
inner join (select idpredio,count(*)
from est_estratopredio
group by idpredio
having count(*)>1) as b on sau.idpredio=b.idpredio)
inner join predio as pre on sau.idpredio=pre.idpredio)
inner join est_bd_maestra_20230630 as ide on ide.id_predio=pre.idpredioca)
where ide.est_def not in ('8','9')--where sau.activa = '1'--where sau.idpredio = 798159
order by sau.idpredio, sau.activa desc
;

--EXPORTAR A CSV REGISTROS REPETIDOS EN EST_ESTRATOPREDIO--
copy(
select sau.idestratop,sau.activa,sau.idpredio,b.count,pre.idpredioca,ide.npn
from (((est_estratopredio as sau
inner join (select idpredio,count(*)
from est_estratopredio
group by idpredio
having count(*)>1) as b on sau.idpredio=b.idpredio)
inner join predio as pre on sau.idpredio=pre.idpredio)
inner join est_bd_maestra_20230630 as ide on ide.id_predio=pre.idpredioca)
where ide.est_def not in ('8','9')--where sau.activa = '1'--where sau.idpredio = 798159
order by sau.idpredio, sau.activa desc
) to
'd:\rep_est_estratopredio.csv' delimiter '|' csv header
;


--SELECCIONAR PREDIOS EN EST_ESTRATOPREDIO--

select *
from est_estratopredio
where idpredio in (798569,798555)
order by idpredio asc, idestratop asc
;

-----------------

--TABLA: PREDIO--

-----------------

--SELECCIONAR PREDIOS Y ESTRATOS EN TABLA PREDIO--
select ide.id_predio, ide.npn,ide.est_def,ide.tipo_est,ide.lado as ide_lado,ide.sesemanlad,pre.idpredio,pre.idprediocatastro,pre.lado,pre.codigounico
from ((est_bd_maestra_20230630 as ide
full join predio as pre on ide.id_predio=pre.idprediocatastro)
full join est_estratopredio as sau on pre.idpredio=sau.idpredio)
where pre.idprediocatastro in (931582)--ide.id_predio = 820474--sau.idestratop = 578035--ide.est_def<>sau.estratoact and ide.tipo_est not in ('8','9') and sau.activa = 1-- and ide.est_atipes = 'A'
order by ide.id_predio
--limit 500
;

select * from predio where idpredioca = 931581;

--SELECCIONAR LADOS DE MANZANA DIFERENTES BDMAS <> PREDIO--
select ide.id_predio, ide.npn,ide.est_def,ide.tipo_est,ide.lado as ide_lado,ide.sesemanlad,pre.idpredio,pre.idprediocatastro,pre.lado--,pre.codigounico
from ((est_bd_maestra_20231130 as ide
right join predio as pre on ide.id_predio=pre.idprediocatastro
full join est_estratopredio as sau on pre.idpredio=sau.idpredio))
--where ide.lado is null or ide.lado not in ('1','2','3','4','5','6','7','8','9') and (pre.lado is null or ide.lado not in (pre.lado))
where (pre.lado not in (ide.lado) or (ide.lado is null and pre.lado is not null) or (ide.lado is not null and pre.lado is null)) and ide.tipo_est not in ('8','9')
order by ide.id_predio--ide.lado
--limit 10
;

--COPIAR LADOS DE MANZANA DIFERENTES BDMAS <> PREDIO--
copy(
select ide.id_predio, ide.npn,ide.est_def,ide.tipo_est,ide.lado as ide_lado,ide.sesemanlad,pre.idpredio,pre.idprediocatastro,pre.lado--,pre.codigounico
from ((est_bd_maestra_20231031 as ide
right join predio as pre on ide.id_predio=pre.idprediocatastro
full join est_estratopredio as sau on pre.idpredio=sau.idpredio))
where (pre.lado not in (ide.lado) or (ide.lado is null and pre.lado is not null) or (ide.lado is not null and pre.lado is null)) and ide.tipo_est not in ('8','9')
order by ide.lado) to
'd:\upt_tpredio_lado_manzana_20231031.csv' delimiter '|' csv header
--limit 10
;

--SELECCIONAR NPN DIFERENTES BDMAS <> PREDIO--
select ide.id_predio as idpredio_cat, ide.npn,ide.est_def,ide.tipo_est,ide.lado,ide.sesemanlad,pre.idpredio,pre.idprediocatastro,pre.codigounico
from ((est_bd_maestra_20231031 as ide
right join predio as pre on ide.id_predio=pre.idprediocatastro
full join est_estratopredio as sau on pre.idpredio=sau.idpredio))
where ide.npn not in (pre.codigounico) and (pre.codigounico is null or ide.npn not in (pre.codigounico)) and tipo_est not in ('8','9')
order by ide.id_predio--ide.lado--ide.id_predio
--limit 10
;

--SELECCIONAR PREDIOS INEXISTENTES BDMAS<>PREDIO--
select id_predio as id_prediocat, ide.npn,ide.est_def,ide.estra_ant,ide.tipo_est,ide.sesemanlad,ide.fecha_edit,sau.idpredio,sau.idestratopredio,sau.activa,sau.estratoanterior,sau.estratoactual,sau.updated_at,pre.idprediocatastro,pre.codigounico,pre.idpredio as idpredio_datic
from ((est_bd_maestra_20231031 as ide
left join predio as pre on ide.id_predio=pre.idprediocatastro)
full join est_estratopredio as sau on pre.idpredio=sau.idpredio)
--where ide.sesemanlad = '01020050B' and ide.tipo_est not in ('8','9')
where ide.id_predio is not null and pre.idpredio is null and ide.tipo_est not in ('8','9')
order by ide.id_predio--ide.sesemanlad
;
------------------------------
--TABLA: DAT_EST_BDCATASTRAL--
------------------------------

--SELECIONAR LADOS DE MANZANA DIFERENTES BDMAS<>DAT_EST--
select ide.id_predio as id_prediocat, ide.npn,ide.est_def,ide.tipo_est,ide.sesemanlad,ide.lado,ide.fecha_edit,est.sesemanlad,est.lado,est.id_predio,est.objectid
from est_bd_maestra_20231031 as ide
inner join dat_est_bdcatastral as est on ide.id_predio=est.id_predio
where ide.sesemanlad <> est.sesemanlad and ide.tipo_est not in ('8','9')
order by ide.id_predio --est.objectid--ide.sesemanlad--
;

--EXPORTAR LADOS DE MANZANA DIFERENTES BDMAS<>DAT_EST--
copy(select ide.id_predio as id_prediocat, ide.npn,ide.est_def,ide.tipo_est,ide.sesemanlad,ide.lado,ide.fecha_edit,est.sesemanlad,est.lado,est.objectid
from est_bd_maestra_20231031 as ide
inner join dat_est_bdcatastral as est on ide.id_predio=est.id_predio
where ide.sesemanlad <> est.sesemanlad and ide.tipo_est not in ('8','9')
order by ide.id_predio) to
'd:\upt_dat_est_bdcatastral_20231031.csv' delimiter '|' csv header
;


--SELECIONAR NPN DIFERENTES BDMAS<>DAT_EST--
select ide.id_predio as id_prediocat, ide.npn,ide.est_def,ide.tipo_est,ide.sesemanlad,ide.lado,ide.fecha_edit,est.npn_2017,est.npn_2018,est.objectid
from est_bd_maestra_20230630 as ide
inner join dat_est_bdcatastral as est on ide.id_predio=est.id_predio
where ide.npn<>est.npn_2017 or est.npn_2017 is null or ide.npn<>est.npn_2018-- and ide.tipo_est not in ('8','9')
order by est.objectid--ide.id_predio asc, ide.est_def asc
--order by ide.id_predio asc, ide.est_def asc
;

--EXPORTAR A CSV NPN DIFERENTES BDMAS<>DAT_EST--
copy(select ide.id_predio as id_prediocat, ide.npn,est.npn_2017,est.npn_2018,est.objectid
from est_bd_maestra_20230630 as ide
inner join dat_est_bdcatastral as est on ide.id_predio=est.id_predio
where ide.npn<>est.npn_2017 or est.npn_2017 is null or ide.npn<>est.npn_2018-- and ide.tipo_est not in ('8','9')
order by ide.id_predio asc, ide.est_def asc) to
'd:\upt_dat_est_bdcatastral_npn_20230801.csv' delimiter '|' csv header
;

--SELECIONAR PREDIOS INEXISTENTES BDMAS<>DAT_EST--
select ide.objectid as objectid, ide.id_predio as id_predio, ide.npn as npn_2018,ide.npn as npn_2017,ide.numepred as numeropre,ide.tipo_avalu as tipo,ide.comuna as comuna,
ide.barrio as barrio, ide.manzana as manzana, ide.terreno as terreno19, ide.seseman as seseman, ide.sesemanlad as sesemanlad, ide.lado as lado, ide.matriz as matriz,
ide.uso_princi as uso_princi, ide.actividad_ as actividad, ide.destino_ec as destino_1, ide.idterreno as conexion
from est_bd_maestra_20230630 as ide
full join dat_est_bdcatastral as est on ide.id_predio=est.id_predio
where est.id_predio is null
order by ide.id_predio asc
--limit 10
;


--EXPORTAR A CSV PREDIOS INEXISTENTES BDMAS<>DAT_EST--
copy(select ide.objectid as objectid, ide.id_predio as id_predio, ide.npn as npn_2018,ide.npn as npn_2017,ide.numepred as numeropre,ide.tipo_avalu as tipo,ide.comuna as comuna,
ide.barrio as barrio, ide.manzana as manzana, ide.terreno as terreno19, ide.seseman as seseman, ide.sesemanlad as sesemanlad, ide.lado as lado, ide.matriz as matriz,
ide.uso_princi as uso_princi, ide.actividad_ as actividad, ide.destino_ec as destino_1, ide.idterreno as conexion
from est_bd_maestra_20230630 as ide
full join dat_est_bdcatastral as est on ide.id_predio=est.id_predio
where est.id_predio is null
order by ide.id_predio asc) to 'd:\ins_dat_est_bdcatastral_20230801.csv' delimiter '|' csv header
;

select * from est_bd_maestra_20230630 where id_predio = 6081;

select * from dat_est_bdcatastral order by objectid desc limit 10;--where id_predio = 6081;

copy(select * from dat_est_bdcatastral where id_predio <= 3000) to 'd:\test_dat_est.csv' delimiter '|' csv header

--SELECCIONAR CUENTA DE REPETIDOS EN DAT_EST_BDCATASTRAL--
select id_predio,count(*)
from dat_est_bdcatastral
group by id_predio
having count(*)>1
order by count desc
;


--SELECCIONAR REGISTROS REPETIDOS EN DAT_EST_BDCATASTRAL--
select dat.objectid,dat.id_predio,dat.sesemanlad,dat.npn_2018,ide.est_def,ide.tipo_est,pre.idpredioca,pre.codigounic,b.count
from (((dat_est_bdcatastral as dat
inner join (select id_predio,count(*)
from dat_est_bdcatastral
group by id_predio
having count(*)>1) as b on dat.id_predio=b.id_predio)
inner join predio as pre on dat.id_predio=pre.idpredioca)
inner join est_bd_maestra_20230630 as ide on ide.id_predio=dat.id_predio)
where ide.est_def not in ('8','9')-- and dat.npn_2018 <> pre.codigounic --where sau.activa = '1'--where sau.idpredio = 798159
order by b.count desc, pre.idpredioca asc, npn_2018 desc
;

--EXPORTAR A CSV REGISTROS REPETIDOS EN DAT_EST_BDCATASTRAL--

copy(
select dat.objectid,dat.id_predio,dat.sesemanlad,dat.npn_2018,ide.est_def,ide.tipo_est,pre.idpredioca,pre.codigounic,b.count
from (((dat_est_bdcatastral as dat
inner join (select id_predio,count(*)
from dat_est_bdcatastral
group by id_predio
having count(*)>1) as b on dat.id_predio=b.id_predio)
inner join predio as pre on dat.id_predio=pre.idpredioca)
inner join est_bd_maestra_20230630 as ide on ide.id_predio=dat.id_predio)
where ide.est_def not in ('8','9')--and dat.npn_2018 <> pre.codigounic --where sau.activa = '1'--where sau.idpredio = 798159
order by b.count desc, pre.idpredioca asc, npn_2018 desc
) to
'd:\rep_est_dat_bdcatastral.csv' delimiter '|' csv header
;
