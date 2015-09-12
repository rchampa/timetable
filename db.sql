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
    estado integer not null default 0, # 0 no validado, 1 validado
    creado_en datetime,
    actualizado_en datetime,
    ultima_conexion datetime
);

#http://localhost:5000/schedules/2/02-09-2015
#http://localhost:5000/schedules/id_usuario/fecha
create table tablas
(
	id_tabla int(8) AUTO_INCREMENT primary key,
	id_usuario int(8),
	descripcion varchar(120),
	semana_del_anio int, # la semana del año siempre es unica, se tendrá en cuenta como clave, al menos internamente.
	anio int,
	borrado boolean,
	creado_en datetime,
    actualizado_en datetime,
	CONSTRAINT uc_semana_anio UNIQUE (semana_del_anio,anio),
	FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

create table eventos
(
	id_evento int(8) AUTO_INCREMENT primary key,
	id_tabla int(8),
	#fecha datetime, no hace falta este campo, ya se tiene el id_tabla
	borrado boolean,

	status int(2),#0 no validado, 1 validado
	privado int(2),#0 privado, 1 publico
	color varchar(13), #RGBA
	comienza varchar(5),#19:00
	finaliza varchar(5),#20:00
	titulo varchar(30),
	descripcion varchar(100),
	url_imagen varchar(100), # intentaré que sean cortas
	dia int(1), # es mejor un numero del 1 al 7
	direccion varchar(100),
	latitud DECIMAL(10, 8) NOT NULL, 
	longitud DECIMAL(11, 8) NOT NULL,
	lugar varchar(50),# descripcion del lugar
	creado_en datetime,
    actualizado_en datetime,
	#datos precalculados para la carga del evento
	timediff_h varchar(2),
	timediff_inmins varchar(4),
	timediff_m varchar(2),

	FOREIGN KEY (id_tabla) REFERENCES tablas(id_tabla)
);

	
#timediff-h: "01",
#timediff-inmins: "6000",
#timediff-m: "00"