from app.data.database import Database

def login(email, password):
    db = Database()
    user = db.fetch_query("SELECT UsuarioID, Contraseña, Nombre, Apellido1, Apellido2 FROM Usuario WHERE Email = ?", (email,))
    if user and db.verify_password(password, user[0][1]):
        return user[0]  # Retorna la tupla completa (UsuarioID, Contraseña, Nombre, Apellido1, Apellido2)
    return None
