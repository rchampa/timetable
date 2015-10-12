from myglobal import app,db,api
from flask import Flask, request
from flask_restful import Resource, Api, Resource, reqparse, fields, marshal
from models import Usuario
from restful.formatResponse import formatOutput



class RegisterAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type = str, required = True, help = 'No email provided', location = 'json')
        self.reqparse.add_argument('password', type = str, required = True, help = 'No password provided', location = 'json')
        super(RegisterAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        email = args['email']
        password = args['password'];
        nuevo_usuario = Usuario(email,password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return formatOutput(1003), 201


api.add_resource(RegisterAPI, '/users', endpoint = 'users')

