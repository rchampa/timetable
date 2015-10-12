from flask import jsonify
from flask_jwt import JWT
from _datetime import datetime
from myglobal import app,db
from my_jwt import UserPayload
from models import Usuario
jwt = JWT(app)

#autentica al usuario
@jwt.authentication_handler
def authenticate(username, password):
    print("authenticate")
    usuario = Usuario.query.filter(Usuario.id_usuario==username, Usuario.password_hash == password).first()
    if usuario is not None:
        return UserPayload(id_usuario=usuario.id_usuario, email=usuario.email)

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
    print(user.username)
    return {
        'id_usuario': user.id_usuario,
        'email': user.email,
        'exp': (datetime.utcnow()+ app.config['JWT_EXPIRATION_DELTA']).isoformat()
    }

#Cuando el usuario es autenticado entonces se devuelve su payload
@jwt.user_handler
def load_user(payload):
    usuario = Usuario.query.filter(Usuario.id_usuario==payload.id_usuario).first()
    if usuario is not None:
        return UserPayload(id_usuario=usuario.id_usuario, email=usuario.email)


