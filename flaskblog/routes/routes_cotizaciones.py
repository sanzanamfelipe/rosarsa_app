import os
import secrets
from datetime import datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, mail
from flaskblog.forms import ProductoForm
from flaskblog.models import User, Producto, TipoFamilia, Cliente, Cotizacion, CotizacionDetalle
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


#codigo productos
@app.route("/cotizaciones/<int:cliente_id>/new", methods=['GET', 'POST'])
@login_required
def cotizaciones_new(cliente_id):
    
    return render_template('cotizaciones/cotizaciones_new.html')