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

from my_flask_restful.FlaskRestfulJwtAPI import FlaskRestfulJwtAPI
api = FlaskRestfulJwtAPI(app, catch_all_404s=True)
# api = FlaskRestfulJwtAPI(app)
# from flask_restful import Api
# api = Api(app, catch_all_404s=True)

#import my_jwt

# from flask import jsonify
# from flask_jwt import JWTError
#
# def handle_user_exception_again(e):
#     if isinstance(e, JWTError):
#         data = {'status_code': 1132, 'message': "JWTError already exists."}
#         return jsonify(data), e.status_code, e.headers
#     return e
#
# app.handle_user_exception = handle_user_exception_again

