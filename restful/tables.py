from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

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

class TodoSimple(Resource):
    def get(self, usuario_id, tabla_id):

    	from datetime import datetime
    	from pytz import timezone
    	fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    	now_time = datetime.now(timezone('Europe/Madrid'))

    	return 	{
	        		str(usuario_id)	: 	usuarios[usuario_id],
	        		tabla_id 		: 	tablas[tabla_id],
	        		'timezone'		:	now_time.strftime(fmt),
	        		'week_of_year'	:	int(now_time.strftime("%U"))
	        	}


api.add_resource(TodoSimple, '/tables/<int:usuario_id>/<string:tabla_id>')

if __name__ == '__main__':
    app.run(debug=True)