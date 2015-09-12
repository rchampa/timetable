from myglobal import app,db,api,auth
from flask import Flask, request
from flask_restful import Resource, Api, Resource, reqparse, fields, marshal
from models import Usuario,Tabla,Evento
from restful.formatResponse import formatOutput
from datetime import datetime

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
    'id_tabla': fields.Integer,
    'fecha': fields.DateTime(dt_format='iso8601'),
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

class TablaEventosAPI(Resource):
    def get(self, usuario_id, tabla_fecha):
        #print(str(datetime.strptime('30-08-2015', '%d-%m-%Y')))
        fecha = datetime.strptime(tabla_fecha, '%d-%m-%Y')
        week_of_year = int(fecha.strftime("%U"))

        f1 = Tabla.id_usuario
        f2 = Tabla.semana_del_anio
        f3 = Tabla.anio
        tabla = Tabla.query.filter(f1==usuario_id,f2==week_of_year, f3==fecha.year).first()
        if tabla is not None:
            lista_eventos = Evento.query.filter(tabla.id_tabla).all()
            
            if (lista_eventos is None) or (count(lista_eventos)==0):
                content = { 'table': marshal(tabla, table_fields) }
                return formatOutput(2001,content)
            else:
                content =   { 
                                'table' : marshal(tabla, table_fields),
                                'events': list(map(lambda t: marshal(t, events_fields), lista_eventos))
                            }
                return formatOutput(2000, content)

        else:
            return formatOutput(2002)

        # from datetime import datetime
        # from pytz import timezone
        # fmt = "%Y-%m-%d %H:%M:%S %Z%z"
        # now_time = datetime.now(timezone('Europe/Madrid'))

        # return    {
        #           str(usuario_id) :   usuarios[usuario_id],
        #           tabla_fecha     :   tablas[tabla_fecha],
        #           'timezone'      :   now_time.strftime(fmt),
        #           'week_of_year'  :   int(now_time.strftime("%U"))
        #       }


api.add_resource(TablaEventosAPI, '/<int:usuario_id>/<string:tabla_fecha>')

class TablasAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id_usuario', type = int, required = True, help = 'No id_usuario provided', location = 'json')
        self.reqparse.add_argument('descripcion', type = str, required = True, help = 'No descripcion provided', location = 'json')
        self.reqparse.add_argument('fecha', type = str, required = True, help = 'No fecha provided', location = 'json')
        super(TablasAPI, self).__init__()

    def get(self):
        lista_tablas = Tabla.query.all()
        content = { 'tables': list(map(lambda t: marshal(t, tables_fields), lista_tablas)) }
        return formatOutput(2003,content)

    def post(self):
        args = self.reqparse.parse_args()
        id_usuario = args['id_usuario']
        descripcion = args['descripcion'];
        fecha = args['fecha'];

        fecha = datetime.strptime(fecha, '%d-%m-%Y')
        week_of_year = int(fecha.strftime("%U"))

        usuario = Usuario.query.filter(Usuario.id_usuario==id_usuario).first()

        if usuario is None:
            return formatOutput(2004)
        else:
            f1 = Tabla.id_usuario
            f2 = Tabla.semana_del_anio
            f3 = Tabla.anio
            f4 = Tabla.borrado
            tabla = Tabla.query.filter(f1==id_usuario,f2==week_of_year, f3==fecha.year, f4==False).first()
            if tabla is None:
                nueva_tabla = Tabla(descripcion, week_of_year, fecha.year, usuario)
                db.session.add(nueva_tabla)
                db.session.commit()
                return formatOutput(2005), 201
            else:
                return formatOutput(2006)


api.add_resource(TablasAPI, '/tables')

class TablaAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('descripcion', type = str, location = 'json')
        self.reqparse.add_argument('borrado', type = bool, location = 'json')
        self.reqparse.add_argument('estado', type = int, location = 'json')
        super(TablaAPI, self).__init__()

    def put(self, tabla_id):
        args = self.reqparse.parse_args()
        tabla = Tabla.query.filter_by(id_tabla=tabla_id).first()
        if tabla is None:
            return formatOutput(2007)
        else:

            if args['descripcion'] is not None:
                tabla.descripcion = args['descripcion']

            if args['borrado'] is not None:
                tabla.borrado = args['borrado']

            if args['estado'] is not None:
                tabla.estado = args['estado']

            tabla.actualizado_en = datetime.utcnow()

            db.session.add(tabla)
            db.session.commit()
            return formatOutput(2008)
            

api.add_resource(TablaAPI, '/tables/<int:tabla_id>')
