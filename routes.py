from myglobal import app,db

from flask import Flask, request, flash, url_for, redirect, \
render_template, abort, send_from_directory, \
session, make_response, jsonify, send_file

from myglobal import app


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)


@app.route('/login',methods=['GET'])
def login():
    return send_file("static/index.html")


@app.route('/home',methods=['GET'])
def home():
    return send_file("static/home.html")

from models import Administrador


@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'


@app.route('/timezone')
def timezone():
  from tzlocal import get_localzone
  tz = get_localzone()
  import datetime
  dtnow = datetime.datetime.now()
  return "Local timezone: "+str(tz)+"<BR>"+str(dtnow)

@app.route('/timezones')
def timezones():
  import pytz
  return str(pytz.all_timezones)

@app.route('/prueba2')
def prueba2():
  import datetime
  dtnow = datetime.datetime.now()
  dtutcnow = datetime.datetime.utcnow()
  salida = "now "+str(dtnow) +"<br>"
  salida = salida + "utcnow "+str(dtutcnow) +"<br>"

  salida = salida + "diferencia horaria" +"<br>"
  delta = dtnow - dtutcnow
  salida = salida + "delta "+str(delta) +"<br>"

  hh,mm = divmod((delta.days * 24*60*60 + delta.seconds + 30) // 60, 60)
  salida = salida + str(hh)+" hours" +"<br>"
  salida = salida + str(mm)+" minutes" +"<br>"

  salida = salida + "%s%+03d:%02d" % (dtnow.isoformat(), hh, mm) +"<br>"

  return salida 

# @app.route('/home')
# def home():
#
#   if 'email' not in session:
#     return redirect(url_for('signin'))
#
#   user = Administrador.query.filter_by(email = session['email']).first()
#
#   if user is None:
#     return redirect(url_for('signin'))
#   else:
#     return render_template('home.html')


