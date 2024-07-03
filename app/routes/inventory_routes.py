from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.data.database import Database
import os

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/menu', methods=['GET'])
def menu_view():
    return render_template('menu.html')

@inventory_bp.route('/consult_inventory', methods=['GET', 'POST'])
def consult_inventory():
    db = Database()
    results = []
    user_id = session.get("UsuarioID") # Id de la sesion abierta
    if request.method == 'POST':
        search_text = request.form['search']
        results = db.fetch_query(
            "SELECT Nombre, Pais, Año, Condicion, ValorReferencial, UsuarioID, Cantidad, ImagenPath FROM Estampilla WHERE Nombre LIKE ? AND UsuarioID = ?",
            ('%' + search_text + '%', user_id)
        )
    return render_template('consult_inventory.html', results=results)

@inventory_bp.route('/manage_inventory', methods=['GET', 'POST'])
def manage_inventory():
    db = Database()
    if request.method == 'POST':
        stamp_id = request.form['stamp_id']
        name = request.form['name']
        country = request.form['country']
        year = request.form['year']
        condition = request.form['condition']
        value = request.form['value']
        image = request.files['image_path']
        quantity = request.form['quantity']
        user_id = session.get('UsuarioID')  # Obtener UsuarioID de la sesión
        
        if image.filename == '':
            flash('Por favor seleccione una imagen.', 'danger')
            return redirect(url_for('inventory.manage_inventory'))

        # Guardar el archivo temporalmente
        image_path = os.path.join('uploads', image.filename)
        image.save(image_path)

        # Subir imagen a Azure Blob Storage
        blob_name = os.path.basename(image_path)
        image_url = db.upload_to_azure(image_path, 'imagenes', blob_name)

        # Eliminar el archivo temporalmente guardado
        os.remove(image_path)

        if db.value_exists('Estampilla', 'EstampillaID', stamp_id):
            flash('La ID de la estampilla ya existe. Use una ID diferente.', 'danger')
            return redirect(url_for('inventory.manage_inventory'))

        query = "INSERT INTO Estampilla (EstampillaID, Nombre, Pais, Año, Condicion, ValorReferencial, UsuarioID, Cantidad, ImagenPath) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        params = (stamp_id, name, country, year, condition, value, user_id, quantity, image_url)
        db.execute_query(query, params)
        flash('Estampilla registrada con éxito', 'success')
        return redirect(url_for('inventory.manage_inventory'))

    return render_template('manage_inventory.html')

@inventory_bp.route('/modify_profile', methods=['GET'])
def modify_profile():
    return render_template('modify_profile.html')

@inventory_bp.route('/modify_email', methods=['GET', 'POST'])
def modify_email():
    if request.method == 'POST':
        new_email = request.form['new_email']
        db = Database()
        user_id = session['UsuarioID']
        db.execute_query("UPDATE Usuario SET Email = ? WHERE UsuarioID = ?", (new_email, user_id))
        flash('Correo electrónico actualizado con éxito', 'success')
        return redirect(url_for('inventory.menu_view'))
    return render_template('modify_email.html')

@inventory_bp.route('/modify_password', methods=['GET', 'POST'])
def modify_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']
        if new_password != confirm_new_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return redirect(url_for('inventory.modify_password'))
        db = Database()
        user_id = session['UsuarioID']
        hashed_password = db.hash_password(new_password)
        db.execute_query("UPDATE Usuario SET Contraseña = ? WHERE UsuarioID = ?", (hashed_password, user_id))
        flash('Contraseña actualizada con éxito', 'success')
        return redirect(url_for('inventory.menu_view'))
    return render_template('modify_password.html')

@inventory_bp.route('/modify_name', methods=['GET', 'POST'])
def modify_name():
    if request.method == 'POST':
        new_first_name = request.form['new_first_name']
        new_last_name1 = request.form['new_last_name1']
        new_last_name2 = request.form['new_last_name2']
        db = Database()
        user_id = session['UsuarioID']
        db.execute_query("UPDATE Usuario SET Nombre = ?, Apellido1 = ?, Apellido2 = ? WHERE UsuarioID = ?", (new_first_name, new_last_name1, new_last_name2, user_id))
        session['nombre'] = new_first_name
        session['apellido1'] = new_last_name1
        session['apellido2'] = new_last_name2
        flash('Nombre actualizado con éxito', 'success')
        return redirect(url_for('inventory.menu_view'))
    return render_template('modify_name.html')

@inventory_bp.route('/modify_all', methods=['GET', 'POST'])
def modify_all():
    if request.method == 'POST':
        new_email = request.form['new_email']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']
        new_first_name = request.form['new_first_name']
        new_last_name1 = request.form['new_last_name1']
        new_last_name2 = request.form['new_last_name2']
        if new_password != confirm_new_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return redirect(url_for('inventory.modify_all'))
        db = Database()
        user_id = session['UsuarioID']
        hashed_password = db.hash_password(new_password)
        db.execute_query("UPDATE Usuario SET Email = ?, Contraseña = ?, Nombre = ?, Apellido1 = ?, Apellido2 = ? WHERE UsuarioID = ?", 
                          (new_email, hashed_password, new_first_name, new_last_name1, new_last_name2, user_id))
        session['nombre'] = new_first_name
        session['apellido1'] = new_last_name1
        session['apellido2'] = new_last_name2
        flash('Información del usuario actualizada con éxito', 'success')
        return redirect(url_for('inventory.menu_view'))
    return render_template('modify_all.html')