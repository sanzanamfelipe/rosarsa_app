from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table_name = 'user'
    __table_args__ = {'schema':'rosarsa_crm'}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.load(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    __table_name = 'post'
    __table_args__ = {'schema':'rosarsa_crm'}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    #user = db.relationship('User', backref='user')
    user_id = db.Column(db.Integer, db.ForeignKey('rosarsa_crm.user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

#############################################################################################################
#dimension cliente
class Cliente(db.Model):
    __table_name = 'cliente'
    __table_args__ = {'schema':'rosarsa_crm'}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    apellido = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(200),unique=True, nullable=True)
    rut = db.Column(db.Integer, nullable=True)
    dv = db.Column(db.String(1), nullable=True)
    direccion = db.Column(db.String(1000), nullable=True)
    numero = db.Column(db.String(50), nullable=True)
    depto = db.Column(db.String(50), nullable=True)
    comuna = db.Column(db.String(150), nullable=True)
    latitud = db.Column(db.String(100), nullable=True)
    longitud = db.Column(db.String(100), nullable=True)
    telefono_movil = db.Column(db.String(50), nullable=True)
    telefono_fijo = db.Column(db.String(50), nullable=True)
    web = db.Column(db.String(500), nullable=True)
    fechacreacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fechamodificacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    activo = db.Column(db.Boolean, nullable=False)
    tipo_cliente = db.relationship('TipoCliente', backref='cliente', lazy=True)
    idtipo_cliente = db.Column(db.Integer, db.ForeignKey('rosarsa_crm.tipo_cliente.id'), nullable=False)
    observaciones = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Cliente('{self.nombre}','{self.apellido}', '{self.email}')"
    

class TipoCliente(db.Model):
    __table_name = 'tipo_cliente'
    __table_args__ = {'schema':'rosarsa_crm'}
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return self.descripcion

class Contactos(db.Model):
    __table_name = 'contactos'
    __table_args__ = {'schema':'rosarsa_crm'}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    apellido = db.Column(db.String(200), nullable=True)
    tratamiento = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    telefono_movil = db.Column(db.String(100), nullable=True)
    cargo = db.Column(db.String(200), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)
    fechacreacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fechamodificacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    activo = db.Column(db.Boolean, nullable=False)
    cliente = db.relationship('Cliente', backref='contactos', lazy=True)
    idcliente = db.Column(db.Integer, db.ForeignKey('rosarsa_crm.cliente.id'), nullable=False)  


#fin dimension cliente
###################################################################################################

###################################################################################################
#dimension producto

class Producto(db.Model):
    __table_name = 'producto'
    __table_args__ = {'schema':'rosarsa_crm'}
    id = db.Column(db.Integer, primary_key=True)
    codigoproducto = db.Column(db.String(50), nullable=False)
    ean11 = db.Column(db.String(50), nullable=True)
    nombreproducto = db.Column(db.String(200), nullable=True)
    descripcion = db.Column(db.String(2000), nullable=True)
    ancho = db.Column(db.Integer, nullable=True)
    alto = db.Column(db.Integer, nullable=True)
    volumen = db.Column(db.Integer, nullable=True)
    tipovolumen = db.Column(db.String(100), nullable=True)
    peso = db.Column(db.Integer, nullable=True)
    tipopeso = db.Column(db.String(100), nullable=True)
    precio = db.Column(db.Integer, nullable=False)
    observaciones = db.Column(db.Text, nullable=True)
    fechacreacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fechamodificacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    imagen = db.Column(db.String(500), nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    idproducto_hijo = db.Column(db.Integer, nullable=True)
    cantidad_producto_hijo = db.Column(db.Integer, nullable=True)
    idproducto_padre = db.Column(db.Integer, nullable=True)
    cantidad_producto_padre = db.Column(db.Integer, nullable=True)
    tipo_familia = db.relationship('TipoFamilia', backref='producto', lazy=True)
    idtipo_familia = db.Column(db.Integer, db.ForeignKey('rosarsa_crm.tipo_familia.id'), nullable=False)
    visible_web = db.Column(db.Boolean, nullable=True, default=True)
    nombreproducto_web = db.Column(db.String(200), nullable=True)
    descripcion_web = db.Column(db.String(2000), nullable=True)



class TipoFamilia(db.Model):
    __table_name = 'tipo_familia'
    __table_args__ = {'schema':'rosarsa_crm'}
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
#fin dimension producto
###################################################################################################

###################################################################################################
#fact cotizacion

class Cotizacion(db.Model):
    __table_name = 'cotizacion'
    __table_args__ = {'schema':'rosarsa_crm'}
    id = db.Column(db.Integer, primary_key=True)
    fechacotizacion = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    fechacreacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cliente = db.relationship('Cliente', backref='cotizacion', lazy=True)
    idcliente = db.Column(db.Integer, db.ForeignKey('rosarsa_crm.cliente.id'), nullable=False)
    email_destino = db.Column(db.String(500), nullable=True)
    precio_total = db.Column(db.Integer, nullable=False, default=0)
    observaciones = db.Column(db.Text, nullable=True)
    texto_email = db.Column(db.Text, nullable=True)
    enviado = db.Column(db.Boolean, nullable=False, default=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    

class CotizacionDetalle(db.Model):
    __table_name = 'cotizacion_detalle'
    __table_args__ = {'schema':'rosarsa_crm'}
    id = db.Column(db.Integer, primary_key=True)
    fechacreacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cotizacion = db.relationship('Cotizacion', backref='cotizacion_detalle', lazy=True)
    idcotizacion = db.Column(db.Integer, db.ForeignKey('rosarsa_crm.cotizacion.id'), nullable=False)
    producto = db.relationship('Producto', backref='cotizacion_detalle', lazy=True)
    idproducto = db.Column(db.Integer, db.ForeignKey('rosarsa_crm.producto.id'), nullable=False)
    cantidad_producto = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.String(2000), nullable=True)
    precio_bruto = db.Column(db.Integer, nullable=False)
    precio_iva = db.Column(db.Integer, nullable=False)
    precio_neto = db.Column(db.Integer, nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    
#end fact cotizacion
###################################################################################################


