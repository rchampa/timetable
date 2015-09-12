
#app = Flask(__name__)
from myglobal import app

import routes

import restful.users
import restful.tables
import restful.events