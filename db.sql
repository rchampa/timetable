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
	id_usuario int(4) AUTO_INCREMENT primary key,
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
	id_tabla int(4) AUTO_INCREMENT primary key,
	id_usuario int(4),
	descripcion varchar(120),
	semana_del_anio int, # la semana del año siempre es unica, se tendrá en cuenta como clave, al menos internamente.
	anio int,
	borrado boolean,
	estado int(4),
	creado_en datetime,
    actualizado_en datetime,
	CONSTRAINT uc_semana_anio UNIQUE (semana_del_anio,anio),
	FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

create table eventos
(
	id_evento int(4) AUTO_INCREMENT primary key,
	id_tabla int(4),
	fecha varchar(10),
	comienza varchar(5),#19:00
	finaliza varchar(5),#20:00
	borrado boolean,
	privacidad int(2), #0 privado, 1 publico
	color varchar(13), #RGBA
	titulo varchar(30),
	descripcion varchar(100),
	url_imagen varchar(100), # intentaré que sean cortas
	#dia int(1), # es mejor un numero del 1 al 7, NO hace falta, por la fecha se puede deducir que día es
	direccion varchar(100),
	latitud DECIMAL(10, 8), 
	longitud DECIMAL(11, 8),
	lugar varchar(50),# descripcion del lugar
	creado_en datetime,
    actualizado_en datetime,
	#datos precalculados para la carga del evento
	timediff_h varchar(2),
	timediff_inmins varchar(4),
	timediff_m varchar(2),

	FOREIGN KEY (id_tabla) REFERENCES tablas(id_tabla)
);

--
-- Volcado de datos para la tabla `tablas`
--

INSERT INTO `usuarios` (`email`, `password_hash`, `borrado`, `estado`, `creado_en`, `actualizado_en`, `ultima_conexion`) VALUES
('ricardo@gmail.com', '1111', 0, 0, '2015-09-12 18:48:25', NULL, NULL),
('javier@gmail.com', '2222', 0, 0, '2015-09-12 18:48:36', NULL, NULL);


INSERT INTO `tablas` (`id_usuario`, `descripcion`, `semana_del_anio`, `anio`, `borrado`, `estado`, `creado_en`, `actualizado_en`) VALUES
(1, 'Descripción 11 bo', 35, 2015, 0, 0, NULL, '2015-09-12 19:42:22');


INSERT INTO `eventos` (`id_tabla`, `fecha`, `comienza`, `finaliza`, `borrado`, `privacidad`, `color`, `titulo`, `descripcion`, `url_imagen`, `direccion`, `latitud`, `longitud`, `lugar`, `creado_en`, `actualizado_en`, `timediff_h`, `timediff_inmins`, `timediff_m`) VALUES
(1, '01-09-2015', '09:00', '10:00', 0, 0, '#3498db', 'Un titulo del evento 1', 'Una descripcion del evento 1', NULL, NULL, NULL, NULL, 'Algun lugar del evento 1', '2015-09-12 22:48:10', NULL, '01', '6000', '00'),
(1, '02-09-2015', '09:00', '10:00', 0, 0, '#3498db', 'Un titulo del evento 2', 'Una descripcion del evento 2', NULL, NULL, NULL, NULL, 'Algun lugar del evento 2', '2015-09-12 22:51:07', NULL, '01', '6000', '00');



