import os
import secrets
import json
from datetime import datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, Response
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (ClienteForm, ClienteUpdateForm, ContactosForm,
                             CotizacionDetalleForm)
from flaskblog.models import User, Cliente, TipoCliente, Contactos, Producto, Cotizacion, CotizacionDetalle
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flask import jsonify
import numpy as np

#codigo clientes
@app.route("/clientes/clientes")
@login_required
def clientes():
    page = request.args.get('page', 1, type=int)
    clientes = Cliente.query.filter_by(activo=True).order_by(Cliente.fechacreacion.desc()).paginate(page=page, per_page=5)
    return render_template('clientes/clientes.html', clientes=clientes)

@app.route("/clientes/new", methods=['GET', 'POST'])
@login_required
def clientes_new():
    form = ClienteForm()
    tipo_cliente = [(tc.id, tc.descripcion) for tc in TipoCliente.query.all()] 
    form.tipo_cliente.choices=tipo_cliente
    if form.validate_on_submit():
        cliente = Cliente(nombre=form.nombre.data, 
                apellido=form.apellido.data, 
                email= form.email.data, 
                rut=form.rut.data, 
                dv=form.dv.data,
                direccion=form.direccion.data,
                numero=form.numero.data,
                depto=form.depto.data,
                comuna=form.comuna.data,
                latitud=form.latitud.data,
                longitud=form.longitud.data,
                telefono_movil=form.telefono_movil.data,
                telefono_fijo=form.telefono_fijo.data,
                web=form.web.data,
                activo=True,
                idtipo_cliente=form.tipo_cliente.data,
                observaciones=form.observaciones.data
                )
        db.session.add(cliente)
        db.session.commit()
        if cliente.id > 0:
            flash('El cliente se ha agregado correctamente', 'success')
            return redirect(url_for('clientes'))
        else:
             flash('Error al cargar datos de nuevo cliente', 'warning') 
             return render_template('clientes_new.html', form=form, legend='Agregar Cliente')
    elif request.method == 'POST': 
        flash('Corregir datos del formulario', 'warning')
    return render_template('clientes_new.html', form=form, legend='Agregar Cliente')

@app.route("/clientes/<int:cliente_id>/update", methods=['GET', 'POST'])
@login_required
def clientes_update(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id) 
    form = ClienteUpdateForm()
    if form.validate_on_submit():
        cliente.nombre = form.nombre.data
        cliente.apellido = form.apellido.data
        cliente.direccion = form.direccion.data
        #cliente.email = form.email.data
        #cliente.idtipo_cliente = cliente.idtipo_cliente
        cliente.numero = form.numero.data
        cliente.comuna = form.comuna.data
        cliente.depto = form.depto.data
        cliente.latitud = form.latitud.data
        cliente.longitud = form.longitud.data
        cliente.rut = form.rut.data
        cliente.dv = form.dv.data
        cliente.telefono_fijo = form.telefono_fijo.data
        cliente.telefono_movil = form.telefono_movil.data
        cliente.web = form.web.data
        cliente.observaciones = form.observaciones.data
        cliente.fechamodificacion = datetime.now()
        db.session.commit()
        flash('¡El cliente se ha editado correctamente!', 'success')
        return redirect(url_for('clientes'))
    elif request.method == 'GET':
         form.nombre.data = cliente.nombre
         form.apellido.data = cliente.apellido 
         form.direccion.data = cliente.direccion
         form.email.data = cliente.email
         #form.tipo_cliente.data = cliente.tipo_cliente
         form.numero.data  = cliente.numero
         form.comuna.data  = cliente.comuna
         form.depto.data = cliente.depto
         form.latitud.data = cliente.latitud
         form.longitud.data = cliente.longitud
         form.rut.data = cliente.rut
         form.dv.data = cliente.dv 
         form.telefono_fijo.data = cliente.telefono_fijo
         form.telefono_movil.data = cliente.telefono_movil
         form.web.data = cliente.web
         form.observaciones.data = cliente.observaciones
    return render_template('clientes_update.html', title = 'Actualiza Cliente', form=form)


@app.route("/clientes/<int:cliente_id>/delete", methods=['GET', 'POST'])
@login_required
def clientes_delete(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    cliente.activo = False
    cliente.fechamodificacion = datetime.now()
    db.session.commit()
    flash('El cliente se ha eliminado!', 'success')
    return redirect(url_for('clientes'))

#ficha cliente con sus contactos
@app.route("/clientes/clientes/<int:cliente_id>", methods=['GET', 'POST'])
@login_required
def clientes_ficha(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    clientes_contactos = Contactos.query.filter_by(idcliente=cliente_id)
    return render_template('clientes/clientes_ficha.html', cliente=cliente, clientes_contactos=clientes_contactos)

@app.route("/clientes/<int:cliente_id>/new_contacto", methods=['GET', 'POST'])
@login_required
def clientes_contactos_new(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    form = ContactosForm()
    if form.validate_on_submit():
        contacto = Contactos(idcliente=cliente_id,
                    nombre=form.nombre.data,
                    apellido=form.apellido.data,
                    tratamiento=form.tratamiento.data,
                    email=form.email.data,
                    telefono_movil=form.telefono_movil.data,
                    cargo=form.cargo.data,
                    observaciones=form.observaciones.data,
                    activo=True)
        db.session.add(contacto)
        db.session.commit()
        if contacto.id > 0:
            flash('El contacto se ha agregado correctamente', 'success')
            clientes_contactos = Contactos.query.filter_by(idcliente=cliente_id)
            #return render_template('clientes/clientes_ficha.html', cliente=cliente, clientes_contactos=clientes_contactos)
            return redirect(url_for('clientes_ficha', cliente_id=cliente_id))
        else:
             flash('Error al cargar datos de nuevo cliente', 'warning') 
             return render_template('clientes_new.html', form=form, legend='Agregar Cliente')
    return render_template('clientes/clientes_new_contacto.html', cliente=cliente, form=form)

@app.route("/clientes/<int:cliente_id>/mail", methods=['GET', 'POST'])
@login_required
def clientes_mail(cliente_id):
    Pass

@app.route("/cotizaciones/<int:cliente_id>/new", methods=['GET', 'POST'])
@login_required
def clientes_cotizacion(cliente_id):

    form_cot_detalle = CotizacionDetalleForm()
    if form_cot_detalle.validate_on_submit():
        producto_id = request.form['selProducto']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        cotizacion_id = request.form['idCotizacion']
        
        cotizacion = Cotizacion.query.filter_by(id=cotizacion_id)
        cliente = Cliente.query.get_or_404(cotizacion.idcliente)
        cotizacion_detalle = CotizacionDetalle(idcotizacion= cotizacion_id, 
                            idproducto = producto_id,  cantidad_producto=cantidad, precio_neto=precio,
                            precio_bruto= np.round(precio*0.19))
        return render_template('cotizaciones/cotizaciones_new.html', cliente=cliente,
                        form_cot_detalle=form_cot_detalle, cotizacion=cotizacion)
    else:
        cliente = Cliente.query.get_or_404(cliente_id)
        productos = Producto.query.filter_by(activo=True)
        productos_list = [( p.id, p.nombreproducto) for p in productos]
        
        form_cot_detalle.selProducto.choices = productos_list
        cotizacion = Cotizacion(cliente=cliente)
        db.session.add(cotizacion)
        db.session.commit()
        form_cot_detalle.idCotizacion = cotizacion.id
        return render_template('cotizaciones/cotizaciones_new.html', cliente=cliente,
                        form_cot_detalle=form_cot_detalle, cotizacion=cotizacion)

@app.route("/cotizaciones/clientes_cotizacion_producto", methods=['POST'])
def clientes_cotizacion_producto():
    idProducto = request.form['idProducto']
    producto = Producto.query.get_or_404(idProducto)
    if producto.precio:
        return jsonify({'precio':producto.precio})
    return jsonify({'error' : '0'})

@app.route("/cotizaciones/clientes_cotizacion_producto/add", methods=['POST'])
@login_required
def clientes_cotizacion_producto_add():
    producto_id = request.form['selProducto']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    cotizacion_id = request.form['idCotizacion']
    cliente = Cliente.query.get_or_404(cliente_id)
    cotizacion = Cotizacion.query.filter_by(id=cotizacion_id)

    cotizacion_detalle = CotizacionDetalle(idcotizacion= cotizacion_id, 
                            idproducto = producto_id,  cantidad_producto=cantidad, precio_neto=precio,
                            precio_bruto= np.round(precio*0.19))


