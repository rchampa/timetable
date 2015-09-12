from myglobal import app,db,api,auth
from flask import Flask, request
from flask_restful import Resource, Api, Resource, reqparse, fields, marshal
from models import Usuario,Tabla,Evento
from restful.formatResponse import formatOutput
from datetime import datetime

events_fields = {
    'id_evento': fields.Integer,
    'id_tabla': fields.Integer,
    'fecha': fields.String,
    'borrado': fields.Boolean,
    'privacidad':fields.Integer,
    'color': fields.String,
    'comienza': fields.String,
    'finaliza': fields.String,
    'titulo': fields.String,
    'descripcion': fields.String,
    'url_imagen': fields.String,
    'direccion': fields.String,
    'latitud': fields.Float,
    'longitud': fields.Float,
    'lugar': fields.String,
    'timediff_h': fields.String,
    'timediff_inmins': fields.String,
    'timediff_m': fields.String,
    'creado_en': fields.DateTime(dt_format='iso8601'),
    'actualizado_en': fields.DateTime(dt_format='iso8601')
}


class EventoAPI(Resource):
    def get(self, evento_id):
        evento = Evento.query.filter_by(id_evento=evento_id).first()
        if evento is not None:
            content = { 'event': marshal(evento, events_fields) }
            return formatOutput(3000,content)
        else:
            return formatOutput(3001)

api.add_resource(EventoAPI, '/events/<int:evento_id>')


class EventosAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id_tabla', type = str, required = True, help = 'No id_tabla provided', location = 'json')
        self.reqparse.add_argument('fecha', type = str, required = True, help = 'No fecha provided', location = 'json')
        self.reqparse.add_argument('privacidad', type = int, required = True, help = 'No privacidad provided', location = 'json')
        self.reqparse.add_argument('color', type = str, required = True, help = 'No color provided', location = 'json')
        self.reqparse.add_argument('comienza', type = str, required = True, help = 'No comienza provided', location = 'json')
        self.reqparse.add_argument('finaliza', type = str, required = True, help = 'No finaliza provided', location = 'json')
        self.reqparse.add_argument('titulo', type = str, required = True, help = 'No titulo provided', location = 'json')
        self.reqparse.add_argument('descripcion', type = str, required = True, help = 'No descripcion provided', location = 'json')
        self.reqparse.add_argument('url_imagen', type = str, location = 'json')
        self.reqparse.add_argument('direccion', type = str, location = 'json')
        self.reqparse.add_argument('latitud', type = float, location = 'json')
        self.reqparse.add_argument('longitud', type = float, location = 'json');
        self.reqparse.add_argument('lugar', type = str, location = 'json');
        self.reqparse.add_argument('timediff_h', type = str, required = True, help = 'No timediff_h provided', location = 'json')
        self.reqparse.add_argument('timediff_inmins', type = str, required = True, help = 'No timediff_inmins provided', location = 'json')
        self.reqparse.add_argument('timediff_m', type = str, required = True, help = 'No titutimediff_mlo provided', location = 'json')
        super(EventosAPI, self).__init__()

    def get(self):
        lista_eventos = Evento.query.all()
        content = { 'events': list(map(lambda t: marshal(t, events_fields), lista_eventos)) }
        return formatOutput(3002,content)

    def post(self):
        args = self.reqparse.parse_args()
        f1 = Tabla.id_tabla
        f2 = Tabla.borrado
        tabla = Tabla.query.filter(f1==args['id_tabla'],f2==False).first()
        if tabla is None:
            return formatOutput(3003)
        else:
            fecha = args['fecha']
            privacidad = args['privacidad']
            color = args['color']
            comienza = args['comienza']
            finaliza = args['finaliza']
            titulo = args['titulo']
            descripcion = args['descripcion']
            timediff_h = args['timediff_h']
            timediff_inmins = args['timediff_inmins']
            timediff_m = args['timediff_m']
            nuevo_evento = Evento(tabla, fecha, privacidad, color, comienza, finaliza, titulo, descripcion, timediff_h, timediff_inmins, timediff_m)
            if args['url_imagen'] is not None:
                nuevo_evento.url_imagen = args['url_imagen']
            if args['direccion'] is not None:
                nuevo_evento.direccion = args['direccion']
            if args['latitud'] is not None:
                nuevo_evento.latitud = args['latitud']
            if args['longitud'] is not None:
                nuevo_evento.longitud = args['longitud']
            if args['lugar'] is not None:
                nuevo_evento.lugar = args['lugar']
            db.session.add(nuevo_evento)
            db.session.commit()
            return formatOutput(3004), 201

        
api.add_resource(EventosAPI, '/events')


