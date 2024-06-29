import pyodbc
from flask import jsonify

def send_response(message, status_code=200):
    """Fonction pour envoyer des réponses JSON standardisées."""
    return jsonify({"message": message}), status_code

def connect_to_sql_server():
    """Function to connect to SQL Server database."""
    server = 'sql-sb-marc-weu.database.windows.net'
    database = 'librasky'
    username = 'librasky'
    password = 'Aze89Rty!'
    driver = '{ODBC Driver 17 for SQL Server}'
    
    try:
        conn = pyodbc.connect(f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}')
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server: {e}")
        return None