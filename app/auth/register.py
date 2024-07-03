from app.data.database import Database
from app.utils.email_validator import email_valido

def register(email, password, first_name, last_name1, last_name2):
    db = Database()
    if db.value_exists('Usuario', 'Email', email):
        return "Este email ya está registrado."
    if not email_valido(email):
        return "El email ingresado no es válido."
    if len(password) < 8:
        return "La contraseña debe estar entre 8 y 64 caracteres."
    if len(password) > 64:
        return "La contraseña debe estar entre 8 y 64 caracteres"

    hashed_password = db.hash_password(password)
    query = "INSERT INTO Usuario (Nombre, Apellido1, Apellido2, Email, Contraseña) VALUES (?, ?, ?, ?, ?)"
    params = (first_name, last_name1, last_name2, email, hashed_password)
    db.execute_query(query, params)
    return "Registro exitoso."

