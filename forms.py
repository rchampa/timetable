from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField

from models import db, Administrador

class SignupForm(Form):
  email = TextField("Email",  [validators.Required("Please enter a email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    admin = Administrador.query.filter_by(email = self.email.data.lower()).first() #SELECT * FROM users WHERE email = self.email.data.lower() 
    if admin:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True



class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please a valid email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    admin = Administrador.query.filter_by(email = self.email.data.lower()).first()
    if admin and admin.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False

