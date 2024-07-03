from app.data.database import Database

def test_connection():
    db = Database()
    results = db.fetch_query("SELECT 1")
    if results:
        print("Conexión exitosa a la base de datos")
    else:
        print("Error al conectar a la base de datos")

if __name__ == "__main__":
    test_connection()