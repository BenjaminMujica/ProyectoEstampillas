import pyodbc
from passlib.context import CryptContext
from azure.storage.blob import BlobServiceClient
import os

class Database:
    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=servidorumayor.database.windows.net;DATABASE=TrabajoUMayor;UID=EstudianteUM;PWD=Umayor69')
        self.cursor = self.conn.cursor()
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        self.blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=imagenesumayor;AccountKey=Rn7MPeRpAt8il+yhyzJ1EBGJaSTbmlbPWu4TqrdvwGOvCEqMcDrLDssfSfItPPJdXo002Pn3URIG+AStk5ecNg==;EndpointSuffix=core.windows.net")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
        except pyodbc.Error as e:
            print(f"Database error: {e}")

    def fetch_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            return []

    def hash_password(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, password, hashed):
        return self.pwd_context.verify(password, hashed)

    def value_exists(self, table, column, value):
        query = f"SELECT 1 FROM {table} WHERE {column} = ?"
        result = self.fetch_query(query, (value,))
        return bool(result)

    def upload_to_azure(self, file_path, container_name, blob_name):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        return blob_client.url

    def download_from_azure(self, container_name, blob_name, download_path):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(download_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())