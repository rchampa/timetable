print("just called once :)")

from flask import Flask
app = Flask(__name__)
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

from flask_restful import Api
api = Api(app, catch_all_404s=True)


from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
import datetime
from models import Administrador

@auth.verify_password
def verify_pw(username, password):
	admin = Administrador.query.filter_by(email = username).first()
	admin.ultima_conexion = datetime.datetime.utcnow()
	db.session.add(admin)
	db.session.commit()
	return (admin and admin.check_password(password) and (admin.estado==1 or admin.estado==2))

@auth.error_handler
def unauthorized():
	from flask import make_response, jsonify
	return make_response(jsonify( { 'message': 'Unauthorized access' } ), 403)
	# return 403 instead of 401 to prevent browsers from displaying the default auth dialog
