import os
import secrets
from datetime import datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import ProductoForm
from flaskblog.models import User, Producto, TipoFamilia
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


#codigo productos
@app.route("/productos/")
@login_required
def productos():
    page = request.args.get('page', 1, type=int)
    productos = Producto.query.filter_by(activo=True).order_by(Producto.fechacreacion.desc()).paginate(page=page, per_page=10)
    return render_template('productos/productos.html', productos=productos)

def guardar_img_producto(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/productos/img', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/productos/new", methods=['GET', 'POST'])
@login_required
def productos_new():
    form = ProductoForm()
    tipo_familia = [(tf.id, tf.descripcion) for tf in TipoFamilia.query.all()] 
    form.tipo_familia.choices=tipo_familia
    if form.validate_on_submit():
        if form.imagen.data:
            picture_file = guardar_img_producto(form.imagen.data)
        else:
            picture_file = '/static/productos/img/default.png'
        producto = Producto(codigoproducto=form.codigoproducto.data,
                        ean11=form.ean11.data,
                        nombreproducto=form.nombreproducto.data,
                        descripcion=form.descripcion.data,
                        precio=form.precio.data,
                        ancho=form.ancho.data,
                        alto=form.alto.data,
                        volumen=form.volumen.data,
                        tipovolumen=form.tipovolumen.data,
                        peso=form.peso.data,
                        tipopeso=form.tipopeso.data,
                        observaciones=form.observaciones.data,
                        imagen='/static/productos/img/'+picture_file,
                        activo=True,
                        idtipo_familia=form.tipo_familia.data,
                        visible_web=form.visible_web.data,
                        nombreproducto_web=form.nombreproducto_web.data,
                        descripcion_web=form.descripcion_web.data
                        )
            
        db.session.add(producto)
        db.session.commit()
        if producto.id > 0:
                flash('El producto se ha agregado correctamente', 'success')
                return redirect(url_for('productos'))
        else:
                flash('Error al cargar datos de nuevo producto', 'warning') 
                return render_template('productos/productos_new.html', form=form, legend='Agregar Producto')
    elif request.method == 'POST': 
        flash('Corregir datos del formulario', 'warning')
    return render_template('productos/productos_new.html', form=form, legend='Agregar Producto')


@app.route("/productos/<int:producto_id>")
@login_required
def productos_ficha(producto_id):
    producto = Productos.query.get_or_404(producto_id)
    return render_template('productos/productos_ficha.html', producto=producto)

@app.route("/productos/<int:producto_id>/delete", methods=['GET', 'POST'])
@login_required
def productos_delete(producto_id):
    producto = Productos.query.get_or_404(producto_id)
    producto.activo = False
    producto.fechamodificacion = datetime.now()
    db.session.commit()
    flash('El Producto se ha eliminado!', 'success')
    return redirect(url_for('productos'))

@app.route("/productos/")
@login_required
def productos_update():
    Pass

@app.route("/productos/tipofamilia")
@login_required
def productos_tipofamilia():
    producto_tipofamilia = TipoFamilia.query.all()
    return render_template('productos/productos_tipofamilia.html', producto_tipofamilia=producto_tipofamilia)

@app.route("/productos/tipofamilia_new")
@login_required
def productos_tipofamilia_new():
    Pass

@app.route("/productos/tipofamilia_delete")
@login_required
def productos_tipofamilia_delete():
    Pass