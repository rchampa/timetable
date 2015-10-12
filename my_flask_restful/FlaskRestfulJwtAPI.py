__author__ = 'Ricardo'

from flask_restful import Api
from flask_jwt import JWTError
from flask import jsonify

class FlaskRestfulJwtAPI(Api):
    def error_router(self, original_handler, e):
        print(type(e))
        if isinstance(e,JWTError):#KeyError:
            data =  {
                "code":400,
                "message":"errror"
            }
            return jsonify(data), 400
        elif isinstance(e,KeyError):
            # return original_handler(e)
            data =  {
                "code":400,
                "message":"errror"
            }
            return jsonify(data), 400
        else:
            return super(FlaskRestfulJwtAPI, self).error_router(original_handler, e)

    def handle_error(self, e):
        if isinstance(e, JWTError):
            code = 400
            data = {'status_code': code, 'message': "JWTError already exists."}
        elif isinstance(e, KeyError):
            code = 400
            data = {'status_code': code, 'message': "KeyError already exists."}
        else:
            # Did not match a custom exception, continue normally
            return super(FlaskRestfulJwtAPI, self).handle_error(e)
        return self.make_response(data, code)
# #api = ErrorFriendlyApi(app)#, errors=errors)