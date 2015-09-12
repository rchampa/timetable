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
  id_centro = db.Column(db.Integer)
  creado_en = db.Column(db.DateTime)
  actualizado_en = db.Column(db.DateTime)
  #notificaciones que viene de rel_notificacion_usuario
  #dispositivos que viene de rel_dispositivo_usuario
   
  def __init__(self, id_usuario, id_centro):
    self.id_usuario = id_usuario
    self.id_centro = id_centro
    dtutcnow = datetime.datetime.utcnow()
    self.creado_en = dtutcnow

  @property
  def json(self):
    return to_json(self, self.__class__)


class Dispositivo(db.Model):
  __tablename__ = 'dispositivos'
  id_dispositivo = db.Column(db.Integer, primary_key = True)
  id_tipo = db.Column(db.Integer)
  activado = db.Column(db.Boolean)
  creado_en = db.Column(db.DateTime)
  actualizado_en = db.Column(db.DateTime)
  gcm_id = db.Column(db.Text)
  friendly_name = db.Column(db.String(32))
  model = db.Column(db.String(32))
  version = db.Column(db.String(32))
  product = db.Column(db.String(32))
  manufacter = db.Column(db.String(32))
  #usuarios que viene de RelDispositivoUsuario

  #id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
  #usuario = db.relationship('Usuario', backref=db.backref('dispositivos', lazy='dynamic'))
  
   
  #def __init__(self, id_tipo, gcm_id, usuario):
  def __init__(self, id_tipo, gcm_id=None, friendly_name=None, model=None, version=None, product=None, manufacter=None):
    self.id_tipo = id_tipo
    self.activado = True
    self.gcm_id = gcm_id
    dtutcnow = datetime.datetime.utcnow()
    self.creado_en = dtutcnow
    self.friendly_name = friendly_name
    self.model = model
    self.version = version
    self.product = product
    self.manufacter = manufacter

  @property
  def json(self):
    return to_json(self, self.__class__)


class RelDispositivoUsuario(db.Model):
  __tablename__ = 'rel_dispositivo_usuario'
  id = db.Column(db.Integer, primary_key = True)
  id_dispositivo = db.Column(db.Integer, db.ForeignKey('dispositivos.id_dispositivo'))
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
  activo = db.Column(db.Boolean)
  usuario = db.relationship('Usuario', backref=db.backref('dispositivos', lazy='dynamic'))
  dispositivo = db.relationship('Dispositivo', backref=db.backref('usuarios', lazy='dynamic'))

   
  def __init__(self, dispositivo, usuario):
    self.dispositivo = dispositivo
    self.usuario = usuario
    self.activo = True
    
  @property
  def json(self):
    return to_json(self, self.__class__)


class Notificacion(db.Model):
  __tablename__ = 'notificaciones'
  id_notificacion = db.Column(db.Integer, primary_key = True)
  titulo = db.Column(db.Text)
  mensaje = db.Column(db.Text)
  bulk = db.Column(db.Boolean)
  fecha = db.Column(db.DateTime)
  creado_en = db.Column(db.DateTime)
  actualizado_en = db.Column(db.DateTime)
  #notificaciones que viene de rel_notificacion_usuario
   
  def __init__(self,titulo,mensaje,fecha,bulk=False):
    #self.id_notificacion = id_notificacion
    self.titulo = titulo
    self.mensaje = mensaje
    self.fecha = fecha
    dtutcnow = datetime.datetime.utcnow()
    self.creado_en = dtutcnow
    self.bulk = bulk

  @property
  def json(self):
    return to_json(self, self.__class__)


class RelNotificacionUsuario(db.Model):
  __tablename__ = 'rel_notificacion_usuario'
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key = True)
  id_notificacion = db.Column(db.Integer, db.ForeignKey('notificaciones.id_notificacion'), primary_key = True)
  borrado = db.Column(db.Boolean)
  leido = db.Column(db.Boolean)
  usuario = db.relationship('Usuario', backref=db.backref('notificaciones', lazy='dynamic'))
  notificacion = db.relationship('Notificacion', backref=db.backref('notificaciones', lazy='dynamic'))

   
  def __init__(self, usuario, notificacion, borrado=False, leido=False):
    self.usuario = usuario
    self.notificacion = notificacion
    self.borrado = borrado
    self.leido = leido

  @property
  def json(self):
    return to_json(self, self.__class__)

  