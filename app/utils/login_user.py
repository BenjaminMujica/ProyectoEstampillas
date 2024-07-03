from flask import session, flash
from app.auth.login import login

def login_and_redirect(email, password):
    user = login(email, password)
    if user:
        session['user_id'] = user[0]
        session['nombre'] = user[2]
        session['apellido1'] = user[3]
        session['apellido2'] = user[4]
        flash('Registro exitoso.', 'success')
        return True
    return False
