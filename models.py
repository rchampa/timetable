from myglobal import db
from werkzeug import generate_password_hash, check_password_hash
import json
import datetime

def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if type(v) is datetime.datetime:
          v = str(v)

        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)


class Administrador(db.Model):
  __tablename__ = 'administradores'
  email = db.Column(db.String(15), primary_key = True)
  password_hash = db.Column(db.String(54))
  creado_en = db.Column(db.DateTime)
  actualizado_en = db.Column(db.DateTime)
  estado = db.Column(db.Integer)
  ultima_conexion = db.Column(db.DateTime)

   
  def __init__(self, email, new_password):
    self.email = email
    self.set_password(new_password)
    self.estado = 0
     
  def set_password(self, new_password):
    self.password_hash = generate_password_hash(new_password)
   
  def check_password(self, new_password):
    return check_password_hash(self.password_hash, new_password)

  @property
  def json(self):
    return to_json(self, self.__class__)


class Usuario(db.Model):
  __tablename__ = 'usuarios'
  id_usuario = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(64))
  password_hash = db.Column(db.String(54))
  borrado = db.Column(db.Boolean)
  estado = db.Column(db.Integer)
  creado_en = db.Column(db.DateTime)
  actualizado_en = db.Column(db.DateTime)
  ultima_conexion = db.Column(db.DateTime)
  #tablas que viene de tablas
   
  def __init__(self, email, password):
    self.email = email
    self.password_hash = password
    self.borrado = False
    self.estado = 0 #por defecto 'no validado'
    dtutcnow = datetime.datetime.utcnow()
    self.creado_en = dtutcnow

  @property
  def json(self):
    return to_json(self, self.__class__)


class Tabla(db.Model):
  __tablename__ = 'tablas'
  id_tabla = db.Column(db.Integer, primary_key = True)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
  descripcion = db.Column(db.String(120))
  semana_del_anio = db.Column(db.Integer)
  anio = db.Column(db.Integer)
  borrado = db.Column(db.Boolean)
  creado_en = db.Column(db.DateTime)
  actualizado_en = db.Column(db.DateTime)
  usuario = db.relationship('Usuario', backref=db.backref('tablas', lazy='dynamic'))
  #eventos

   
  def __init__(self, descripcion, semana_del_anio, anio, activo, usuario):
    self.descripcion = descripcion
    self.semana_del_anio = semana_del_anio
    self.anio = anio
    self.activo = activo
    self.usuario = usuario
    self.activo = True
    
  @property
  def json(self):
    return to_json(self, self.__class__)


class Evento(db.Model):
  __tablename__ = 'eventos'
  id_evento = db.Column(db.Integer, primary_key = True)
  id_tabla = db.Column(db.Integer, db.ForeignKey('tablas.id_tabla'))
  borrado = db.Column(db.Boolean)
  status = db.Column(db.Integer)#0 no validado, 1 validado
  privado = db.Column(db.Integer)#0 privado, 1 publico
  color = db.Column(db.String(13))#RGBA
  comienza = db.Column(db.String(5))#19:00
  finaliza = db.Column(db.String(5))#20:00
  titulo = db.Column(db.String(30))
  descripcion = db.Column(db.String(100))
  url_imagen = db.Column(db.String(100))# intentaré que sean cortas
  dia = db.Column(db.Integer)# es mejor un numero del 1 al 7
  direccion = db.Column(db.String(100))
  latitud = db.Column(db.Float)
  longitud = db.Column(db.Float)
  lugar = db.Column(db.String(50))# descripcion del lugar
  creado_en = db.Column(db.DateTime)
  actualizado_en = db.Column(db.DateTime)
  #datos precalculados para la carga del evento
  timediff_h  = db.Column(db.String(2))
  timediff_inmins = db.Column(db.String(4))
  timediff_m  = db.Column(db.String(2))
  tabla = db.relationship('Tabla', backref=db.backref('eventos', lazy='dynamic'))
  
  def __init__(self, tabla, borrado, status, privado, color, comienza, finaliza, titulo, descripcion, url_imagen, dia, direccion, latitud, longitud, lugar, timediff_h, timediff_inmins, timediff_m):
    self.tabla = tabla
    self.borrado = borrado
    self.status = status
    self.privado = privado
    self.color = color
    self.comienza = comienza
    self.finaliza = finaliza
    self.titulo = titulo
    self.descripcion = descripcion
    self.url_imagen = url_imagen
    self.dia = dia
    self.direccion = direccion
    self.latitud = latitud
    self.longitud = longitud
    self.lugar = lugar
    self.timediff_h = timediff_h
    self.timediff_inmins = timediff_inmins
    self.timediff_m = timediff_m

    dtutcnow = datetime.datetime.utcnow()
    self.creado_en = dtutcnow

  @property
  def json(self):
    return to_json(self, self.__class__)
