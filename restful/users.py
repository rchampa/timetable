from myglobal import app,db,api,auth
from flask import Flask, request
from flask_restful import Resource, Api, Resource, reqparse, fields, marshal
from models import Usuario
from restful.formatResponse import formatOutput

users_fields = {
    'id_usuario': fields.Integer,
    'email': fields.String,
    'borrado': fields.Boolean,
    'estado':fields.Integer,
    'creado_en': fields.DateTime(dt_format='iso8601'),
    'actualizado_en': fields.DateTime(dt_format='iso8601'),
    'ultima_conexion': fields.DateTime(dt_format='iso8601')
}

class UsuarioAPI(Resource):
    def get(self, usuario_id):
        usuario = Usuario.query.filter_by(id_usuario=usuario_id).first()
        if usuario is not None:
            content = { 'user': marshal(usuario, users_fields) }
            return formatOutput(1001,content)
        else:
            return formatOutput(1002)

api.add_resource(UsuarioAPI, '/api/users/<int:usuario_id>', endpoint = 'user')

class UsuariosAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type = str, required = True, help = 'No email provided', location = 'json')
        self.reqparse.add_argument('password', type = str, required = True, help = 'No password provided', location = 'json')
        super(UsuariosAPI, self).__init__()

    def get(self):
        lista_usuarios = Usuario.query.all()
        content = { 'users': list(map(lambda t: marshal(t, users_fields), lista_usuarios)) }
        return formatOutput(1000,content)

    def post(self):
        args = self.reqparse.parse_args()
        email = args['email']
        password = args['password'];
        nuevo_usuario = Usuario(email,password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return formatOutput(1003), 201

        
api.add_resource(UsuariosAPI, '/api/users', endpoint = 'users')

