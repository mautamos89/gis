-- Crear la DB
CREATE DATABASE practica3
  ENCODING = 'UTF8';

-- Crear la extensión postgis
CREATE EXTENSION postgis;

-- Crear las relaciones del ejercicio

-- Relación geográfica
-- parque
-- EJECUTAR PARQUE.SQL

-- Eliminar la llave existente y borrar el campo
ALTER TABLE parque DROP CONSTRAINT parque_pkey;
ALTER TABLE parque DROP COLUMN gid;

-- Asignar una nueva llave primaria
ALTER TABLE parque ADD CONSTRAINT parque_pkey PRIMARY KEY (ParId);

-- Ajustar estructura de relación
ALTER TABLE parque ALTER COLUMN ParNom SET NOT NULL;
ALTER TABLE parque ALTER COLUMN ParSuper SET NOT NULL;

-- Relación alfanumérica
create table comarca (
	ComId smallint primary key,
    NomCom varchar(50) not null, -- índice
    HabitaCom integer
);

-- espacio_natural
create table espacio_natural (
-- 	EsnatId serial primary key,
	EsnaCod varchar(3) primary key,
	EsnaNom varchar(50) not null, -- índice
	EsnaSuper decimal(11,2),
	EsnaCom varchar(100) not null 
);

-- coord_general
create table coord_general(
	CordGenDni varchar(9) primary key,
	CordGenNom varchar(20) not null,
	CordGenApe varchar(20) not null,
	CordGenTlf varchar(11),
	ComId smallint not null --Llave foránea | índice
);

-- coord_tecnico
create table coord_tecnico(
	CordTecDni varchar(9) primary key,
	CordTecNom varchar(20) not null,
	CordTecApe varchar(20) not null,
	CordTecTlf varchar(11),
	CordGenDni varchar(9) not null --Llave foránea  | índice
);

-- parque_comarca
create table parque_comarca(
	ParComId serial primary key,
	ParId varchar(3) not null, -- Llave foránea | índice
	ComId smallint not null, -- Llave foránea | índice
	CordTecDni varchar(9) not null -- Llave foránea | índice
);

-- agente_rural
create table agente_rural(
	AgeRurDni varchar(9) primary key,
	AgeRurNom varchar(20) not null,
	AgeRurApe varchar(20) not null,
	AgeRurTlf varchar(11),
	AgeRurFec date not null,
	ParId varchar(3) not null --Llave foránea | índice
);

-- Agente rural: Identificar los códigos de los parques
select parid, parnom, geom from parque where
parnom ilike '%avarre%' or
parnom ilike '%cadire%' or
parnom ilike '%aiguamoll%'
order by parid asc
;

-- incidencia
create table incidencia(
	IncidId serial primary key,
	AgeRurDni varchar(9) not null, --Llave foránea | índice
	IncidFec date not null,
	IncidLat numeric not null,
	IncidLon numeric not null,
	IncidDesc varchar(100) not null 
);

-- Importar datos de forma masiva
copy comarca from 'D:\msc\3_bases_datos_espaciales\practica_3\comarca.csv' delimiter ';' csv header;
copy espacio_natural from 'D:\msc\3_bases_datos_espaciales\practica_3\espacio_natural.csv' delimiter ';' csv header;
copy coord_general from 'D:\msc\3_bases_datos_espaciales\practica_3\coord_general.csv' delimiter ';' csv header;
copy coord_tecnico from 'D:\msc\3_bases_datos_espaciales\practica_3\coord_tecnico.csv' delimiter ';' csv header;
copy parque_comarca (ParId, ComId, CordTecDni)
from 'D:\msc\3_bases_datos_espaciales\practica_3\parque_comarca.csv' delimiter ';' csv header;
copy agente_rural from 'D:\msc\3_bases_datos_espaciales\practica_3\agente_rural.csv' delimiter ';' csv header;
copy incidencia(AgeRurDni, IncidFec, IncidLat, IncidLon, IncidDesc)
from 'D:\msc\3_bases_datos_espaciales\practica_3\incidencia.csv' delimiter ';' csv header;

-- Validar registros importados
select * from comarca;
select * from espacio_natural;
select * from coord_general;
select * from coord_tecnico;
select * from parque_comarca;
select * from parque;
select * from agente_rural;
select * from incidencia;

-- Especificar claves foráneas
-- Relación Coordinador general
alter table coord_general add foreign key (ComId) references comarca(ComId);

-- Relación Coordinador técnico
alter table coord_tecnico add foreign key (CordGenDni) references coord_general(CordGenDni);

-- Relación Parque comarca
alter table parque_comarca add foreign key (ParId) references parque(ParId);
alter table parque_comarca add foreign key (ComId) references comarca(ComId);
alter table parque_comarca add foreign key (CordTecDni) references coord_tecnico(CordTecDni);

-- Relación Agente rural
alter table agente_rural add foreign key (ParId) references parque(ParId);

-- Relación Incidencia
alter table incidencia add foreign key (AgeRurDni) references agente_rural(AgeRurDni);

-- índices para optimizar consultas
create index idx_parque_parnom on parque(parnom);
create index idx_comarca_nomcom on comarca(NomCom);
create index idx_espacio_natural_esnanom on espacio_natural(EsnaNom);
create index idx_coord_general_comid on coord_general(ComId);
create index idx_coord_tecnico_cordgendni on coord_tecnico(CordGenDni);
create index idx_parque_comarca_parid on parque_comarca(ParId);
create index idx_parque_comarca_comid on parque_comarca(ComId);
create index idx_parque_comarca_cordtecdni on parque_comarca(CordTecDni);
create index idx_agente_rural_parid on agente_rural(ParId);
create index idx_incidencia_agerurdni on incidencia(AgeRurDni);