from myglobal import app,db,api,auth
from flask import Flask, request
from flask_restful import Resource, Api, Resource, reqparse, fields, marshal
from models import Usuario,Tabla,Evento
from restful.formatResponse import formatOutput
from datetime import datetime

usuarios = {
			0:"Ricardo",
			1:"Javier",
			2:"Carlos"	
		}

tablas = {
			'30-08-2015':"Evento 1",
			'31-08-2015':"Evento 2",
			'01-09-2015':"Evento 3",
			'02-09-2015':"Evento 4",
			'03-09-2015':"Evento 5",
			'04-09-2015':"Evento 6",
			'2015':"Eventooooo 6",
		}

users_fields = {
    'id_usuario': fields.Integer,
    'email': fields.String,
    'borrado': fields.Boolean,
    'estado':fields.Integer,
    'creado_en': fields.DateTime(dt_format='iso8601'),
    'actualizado_en': fields.DateTime(dt_format='iso8601'),
    'ultima_conexion': fields.DateTime(dt_format='iso8601')
}

tables_fields = {
	'id_tabla': fields.Integer,
    'id_usuario': fields.Integer,
    'descripcion': fields.String,
    'semana_del_anio': fields.Integer,
    'anio': fields.Integer,
    'borrado': fields.Boolean,
    'estado':fields.Integer,
    'creado_en': fields.DateTime(dt_format='iso8601'),
    'actualizado_en': fields.DateTime(dt_format='iso8601')
}

events_fields = {
    'id_evento': fields.Integer,
    'email': fields.String,
    'borrado': fields.Boolean,
    'estado':fields.Integer,
    'creado_en': fields.DateTime(dt_format='iso8601'),
    'actualizado_en': fields.DateTime(dt_format='iso8601'),
    'ultima_conexion': fields.DateTime(dt_format='iso8601')
}

class TablaAPI(Resource):
    def get(self, usuario_id, tabla_fecha):
    	#print(str(datetime.strptime('30-08-2015', '%d-%m-%Y')))
    	fecha = datetime.strptime(tabla_fecha, '%d-%m-%Y')
    	week_of_year = int(fecha.strftime("%U"))

    	tabla = Tabla.query.filter(id_usuario==usuario_id,semana_del_anio==week_of_year, anio==fecha.year).first()
    	if tabla is not None:
    		lista_eventos = Evento.query.filter(tabla.id_tabla).all()
    		
    		if (lista_eventos is None) or (count(lista_eventos)==0):
    			content = { 'table': marshal(tabla, table_fields) }
    			return formatOutput(2001,content)
    		else:
    			content = 	{ 
    							'table'	: marshal(tabla, table_fields),
    							'events': list(map(lambda t: marshal(t, events_fields), lista_eventos))
    						}
    			return formatOutput(2000, content)

    	else:
    		return formatOutput(2002)

    	# from datetime import datetime
    	# from pytz import timezone
    	# fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    	# now_time = datetime.now(timezone('Europe/Madrid'))

    	# return 	{
	    #     		str(usuario_id)	: 	usuarios[usuario_id],
	    #     		tabla_fecha 	: 	tablas[tabla_fecha],
	    #     		'timezone'		:	now_time.strftime(fmt),
	    #     		'week_of_year'	:	int(now_time.strftime("%U"))
	    #     	}


api.add_resource(TablaAPI, '/tables/<int:usuario_id>/<string:tabla_fecha>')
