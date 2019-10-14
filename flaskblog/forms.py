from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, TextField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flaskblog.models import User, TipoCliente, Cliente, Producto, TipoFamilia


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile File', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Password Reset')

class ClienteForm(FlaskForm):
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

    def validate_email(self, email):
        cliente = Cliente.query.filter_by(email=email.data).first()
        if cliente:
            raise ValidationError('Este email de cliente ya fué ingresado.')


class ClienteUpdateForm(FlaskForm):
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
    observaciones = TextAreaField('Observaciones')
    submit = SubmitField('Enviar')

class ProductoForm(FlaskForm):
    codigoproducto = StringField('Codigo Producto', validators=[DataRequired()])
    ean11 = StringField('EAN11')
    nombreproducto = StringField('Nombre Producto')
    descripcion = TextAreaField('Descripcion')
    ancho = StringField('ancho', default='0')
    alto = StringField('alto', default='0')
    volumen = StringField('volumen', default='0')
    tipovolumen = StringField('Un. Vol.', default='ml.')
    peso = StringField('peso', default='0')
    tipopeso = StringField('Un. Peso', default='gr.')
    precio = StringField('Precio Venta',  validators=[DataRequired()])
    observaciones = TextAreaField('observaciones')
    imagen = FileField('Subir Imagen Producto', validators=[FileAllowed(['jpg', 'png'])])
    idproducto_hijo = StringField('idproducto_hijo')
    cantidad_producto_hijo = StringField('cantidad_producto_hijo')
    tipo_familia = SelectField('Tipo Familia',coerce=int, validators=[DataRequired()])
    visible_web = BooleanField('Visible')
    nombreproducto_web = StringField('Nombre Producto Web')
    descripcion_web = StringField('Descripcion Web')
    submit = SubmitField('Enviar')

class ContactosForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido')
    tratamiento = StringField('Tratamiento', default='Sr.')
    email = StringField('Email', validators=[Email(), DataRequired()])
    apellido = StringField('Apellido')
    telefono_movil = StringField('Telefono Movil')
    cargo = StringField('Cargo')
    observaciones = TextAreaField('Observaciones')
    submit = SubmitField('Enviar')


class CotizacionDetalleForm(FlaskForm):
    selProducto = SelectField('Seleccionar Producto', coerce=int, validators=[DataRequired()], default=1)
    cantidad = StringField('Cantidad')
    precio = StringField('Precio')
    idCotizacion = HiddenField('')
    submit_add_detalle = SubmitField('Enviar')




