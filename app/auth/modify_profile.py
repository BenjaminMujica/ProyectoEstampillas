from utils.email_validator import email_valido
from data.database import Database  # Importar la clase Database

def modify_profile(current_user_email):
    db = Database()  # Crear instancia de la base de datos
    user = db.fetch_query("SELECT UsuarioID, Email, Nombre, Apellido1, Apellido2 FROM Usuario WHERE Email = ?", (current_user_email,))
    if not user:
        print("Usuario no encontrado.")
        return current_user_email  # Retornar el correo actual si no se encuentra el usuario

    while True:
        print("\n-----Modificar Perfil-----")
        print("1. Cambiar Correo Electrónico")
        print("2. Cambiar Contraseña")
        print("3. Cambiar Nombres")
        print("4. Cambiar Todo")
        print("5. Regresar")

        choice = input("Seleccione una opción: ")

        if choice == '1':
            new_email = input("Ingrese el nuevo correo electrónico: ")
            if not email_valido(new_email):
                print("Correo electrónico no válido.")
                return current_user_email  # Retornar el correo actual si el nuevo correo no es válido
            query = "UPDATE Usuario SET Email = ? WHERE UsuarioID = ?"
            db.execute_query(query, (new_email, user[0][0]))
            print("Correo electrónico actualizado exitosamente.")
            return new_email  # Retornar el nuevo correo electrónico

        elif choice == '2':
            while True:
                new_password = input("Ingrese la nueva contraseña: ")
                confirm_password = input("Confirme la nueva contraseña: ")
                if new_password != confirm_password:
                    print("Las contraseñas no coinciden.")
                elif len(new_password) < 8:
                    print("La contraseña es muy corta, inténtelo de nuevo.")
                else:
                    hashed_password = db.hash_password(new_password)
                    query = "UPDATE Usuario SET Contraseña = ? WHERE UsuarioID = ?"
                    db.execute_query(query, (hashed_password, user[0][0]))
                    print("Contraseña actualizada exitosamente.")
                    return current_user_email  # Retornar el correo actual ya que no se ha cambiado

        elif choice == '3':
            new_nombre = input("Ingrese el nuevo nombre: ")
            new_apellido_paterno = input("Ingrese el nuevo apellido paterno: ")
            new_apellido_materno = input("Ingrese el nuevo apellido materno: ")
            query = "UPDATE Usuario SET Nombre = ?, Apellido1 = ?, Apellido2 = ? WHERE UsuarioID = ?"
            db.execute_query(query, (new_nombre, new_apellido_paterno, new_apellido_materno, user[0][0]))
            print("Nombres actualizados exitosamente.")
            return current_user_email  # Retornar el correo actual ya que no se ha cambiado

        elif choice == '4':
            new_email = input("Ingrese el nuevo correo electrónico: ")
            if not email_valido(new_email):
                print("Correo electrónico no válido.")
                return current_user_email  # Retornar el correo actual si el nuevo correo no es válido
            
            while True:
                new_password = input("Ingrese la nueva contraseña: ")
                confirm_password = input("Confirme la nueva contraseña: ")
                if new_password != confirm_password:
                    print("Las contraseñas no coinciden.")
                elif len(new_password) < 8:
                    print("La contraseña es muy corta, inténtelo de nuevo.")
                else:
                    hashed_password = db.hash_password(new_password)
                    break
            
            new_nombre = input("Ingrese el nuevo nombre: ")
            new_apellido_paterno = input("Ingrese el nuevo apellido paterno: ")
            new_apellido_materno = input("Ingrese el nuevo apellido materno: ")
            
            query = "UPDATE Usuario SET Email = ?, Contraseña = ?, Nombre = ?, Apellido1 = ?, Apellido2 = ? WHERE UsuarioID = ?"
            db.execute_query(query, (new_email, hashed_password, new_nombre, new_apellido_paterno, new_apellido_materno, user[0][0]))
            print("Correo electrónico, contraseña y nombres actualizados exitosamente.")
            return new_email  # Retornar el nuevo correo electrónico

        elif choice == '5':
            return current_user_email  # Regresar al menú principal

        else:
            print("Opción no válida.")


"""
from utils.email_validator import email_valido

def modify_profile(users, current_user_email):
    user = next((user for user in users if user['email'] == current_user_email), None)
    if not user:
        print("Usuario no encontrado.")
        return current_user_email  # Retornar el correo actual si no se encuentra el usuario

    while True:
        print("\n-----Modificar Perfil-----")
        print("1. Cambiar Correo Electrónico")
        print("2. Cambiar Contraseña")
        print("3. Cambiar Nombres")
        print("4. Cambiar Todo")
        print("5. Regresar")

        choice = input("Seleccione una opción: ")

        if choice == '1':
            new_email = input("Ingrese el nuevo correo electrónico: ")
            if not email_valido(new_email):
                print("Correo electrónico no válido.")
                return current_user_email  # Retornar el correo actual si el nuevo correo no es válido
            user['email'] = new_email
            print("Correo electrónico actualizado exitosamente.")
            return new_email  # Retornar el nuevo correo electrónico

        elif choice == '2':
            while True:
                new_password = input("Ingrese la nueva contraseña: ")
                confirm_password = input("Confirme la nueva contraseña: ")
                if new_password != confirm_password:
                    print("Las contraseñas no coinciden.")
                elif len(new_password) < 8:
                    print("La contraseña es muy corta, inténtelo de nuevo.")
                else:
                    user['password'] = new_password
                    print("Contraseña actualizada exitosamente.")
                    return current_user_email  # Retornar el correo actual ya que no se ha cambiado

        elif choice == '3':
            new_nombre = input("Ingrese el nuevo nombre: ")
            new_apellido_paterno = input("Ingrese el nuevo apellido paterno: ")
            new_apellido_materno = input("Ingrese el nuevo apellido materno: ")
            user['nombre'] = new_nombre
            user['apellido_paterno'] = new_apellido_paterno
            user['apellido_materno'] = new_apellido_materno
            print("Nombres actualizados exitosamente.")
            return current_user_email  # Retornar el correo actual ya que no se ha cambiado

        elif choice == '4':
            new_email = input("Ingrese el nuevo correo electrónico: ")
            if not email_valido(new_email):
                print("Correo electrónico no válido.")
                return current_user_email  # Retornar el correo actual si el nuevo correo no es válido
            
            while True:
                new_password = input("Ingrese la nueva contraseña: ")
                confirm_password = input("Confirme la nueva contraseña: ")
                if new_password != confirm_password:
                    print("Las contraseñas no coinciden.")
                elif len(new_password) < 8:
                    print("La contraseña es muy corta, inténtelo de nuevo.")
                else:
                    break
            
            new_nombre = input("Ingrese el nuevo nombre: ")
            new_apellido_paterno = input("Ingrese el nuevo apellido paterno: ")
            new_apellido_materno = input("Ingrese el nuevo apellido materno: ")
            
            user['email'] = new_email
            user['password'] = new_password
            user['nombre'] = new_nombre
            user['apellido_paterno'] = new_apellido_paterno
            user['apellido_materno'] = new_apellido_materno
            print("Correo electrónico, contraseña y nombres actualizados exitosamente.")
            return new_email  # Retornar el nuevo correo electrónico

        elif choice == '5':
            return current_user_email  # Regresar al menú principal

        else:
            print("Opción no válida.")
"""
