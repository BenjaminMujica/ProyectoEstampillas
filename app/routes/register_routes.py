from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.auth.register import register
from app.utils.login_user import login_and_redirect  # Importar la nueva función

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register_view():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name1 = request.form['last_name1']
        last_name2 = request.form['last_name2']
        result = register(email, password, first_name, last_name1, last_name2)
        if result == "Registro exitoso.":
            if login_and_redirect(email, password):  # Usar la nueva función
                return redirect(url_for('inventory.menu_view'))
        else:
            flash(result, 'danger')
    return render_template('register.html')