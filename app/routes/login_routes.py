from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.auth.login import login

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = login(email, password)
        if user:
            session['UsuarioID'] = user[0]  # Almacenar UsuarioID en la sesión
            session['nombre'] = user[2]
            session['apellido1'] = user[3]
            session['apellido2'] = user[4]
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('inventory.menu_view'))
        else:
            flash('Correo o contraseña incorrecta', 'danger')
    return render_template('login.html')

