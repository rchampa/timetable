print("just called once :)")

from flask import Flask
app = Flask(__name__, static_url_path = "")
app.config.from_pyfile('flaskapp.cfg')

import logging
from logging import StreamHandler
file_handler = StreamHandler()
app.logger.setLevel(logging.DEBUG)  # set the desired logging level here
#app.logger.setLevel(logging.ERROR)  # set the desired logging level here
app.logger.addHandler(file_handler)


import os
here = os.path.dirname(__file__)
app.logger.debug(str(here))


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
from constants import MYSQL_URI
app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_URI
app.config['SQLALCHEMY_ECHO'] = True


from flask_restful import Api
api = Api(app, catch_all_404s=True)


from flask import jsonify
from flask_jwt import JWT
from restful.UserPayload import UserPayload
from models import Usuario
from _datetime import datetime
jwt = JWT(app)

#autentica al usuario
@jwt.authentication_handler
def authenticate(username, password):
    print("authenticate")
    usuario = Usuario.query.filter(Usuario.email==username, Usuario.password_hash == password).first()
    if usuario is not None:
        return UserPayload(id_usuario=usuario.id_usuario, email=usuario.email)
    else:
        return None #si se devuelve None se entiende que el las credenciales no son válidas

@jwt.error_handler
def error_handler(e):
    data =  {
                "code":e.status_code,
                "message":e.error+" "+e.description
            }
    return jsonify(data), 400

@jwt.payload_handler
def make_payload(user):
    print("make_payload")
    return {
        'id_usuario': user.id_usuario,
        'email': user.email,
        'exp': (datetime.utcnow()+ app.config['JWT_EXPIRATION_DELTA']).isoformat()
    }

#Cuando el usuario es autenticado entonces se devuelve su payload
@jwt.user_handler
def load_user(payload):
    usuario = Usuario.query.filter(Usuario.id_usuario==payload['id_usuario']).first()
    if usuario is not None:
        return UserPayload(id_usuario=usuario.id_usuario, email=usuario.email)
    else:
        return None #si se devuelve None se entiende que el usuario que viene en el payload no existe
