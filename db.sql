create table administradores
(
    email varchar(64) primary key,
    password_hash text,
    creado_en datetime,
    actualizado_en datetime,
    estado integer not null default 0, # 0 no validado, 1 validado, 2 administrador supremo
    ultima_conexion datetime
);

create table usuarios
(
	id_usuario int(8) AUTO_INCREMENT primary key,
    email varchar(64),
    password_hash text,
    borrado boolean,
    creado_en datetime,
    actualizado_en datetime,
    estado integer not null default 0, # 0 no validado, 1 validado
    ultima_conexion datetime
);

create table tablas
(
	id_tabla int(8) AUTO_INCREMENT primary key,
	id_usuario int(8),
	descripcion varchar(120),
	semana_del_anio int, # la semana del año siempre es unica, se tendrá en cuenta como clave, al menos internamente.
	borrado boolean,
	FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

create table eventos
(
	id_evento int(8) AUTO_INCREMENT primary key,
	id_tabla int(8),
	fecha datetime,
	borrado boolean,

	status int(2),
	color varchar(7),
	comienza varchar(5),
	finaliza varchar(5),
	titulo varchar(30),
	descripcion varchar(100),
	url_imagen varchar(100), # intentaré que sean cortas
	dia int(1), # es mejor un numero del 1 al 7
	lugar varchar(50),# aqui molaria poner algo de google maps, no?
	timediff_h varchar(2),
	timediff_inmins varchar(4),
	timediff_m varchar(2),

	FOREIGN KEY (id_tabla) REFERENCES tablas(id_tabla)
);

	
#timediff-h: "01",
#timediff-inmins: "6000",
#timediff-m: "00"