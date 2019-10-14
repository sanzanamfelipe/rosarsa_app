from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User, Productos, TipoFamilia

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido')
    email = StringField('Email', validators=[Email(), DataRequired()])
    rut = StringField('Rut')
    dv = StringField('DV')
    direccion = StringField('Direccion')
    numero = StringField('Numero')
    depto = StringField('Depto')
    comuna = StringField('Comuna')
    latitud = StringField('Latitud')
    longitud = StringField('Longitud')
    telefono_movil = StringField('Telefono Movil')
    telefono_fijo = StringField('Telefono Fijo')
    web = StringField('Sitio Web')
    tipo_cliente = SelectField('Tipo Cliente',coerce=int, validators=[DataRequired()])
    observaciones = TextAreaField('Observaciones')
    submit = SubmitField('Enviar')