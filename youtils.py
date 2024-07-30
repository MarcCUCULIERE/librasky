import os
import pyodbc

def connect_to_sql_server():
    """Function to connect to SQL Server database using username and password."""
    server = 'tcp:sql-sb-marc-weu.database.windows.net:1443'
    database = 'LIBRASKY'
    driver = '{ODBC Driver 17 for SQL Server}'
    username = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'

    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server: {e}")
        return None

def create_database_and_schema(server, database):
    try:
        # Connexion au serveur avec nom d'utilisateur et mot de passe
        conn = connect_to_sql_server()
        if conn is None:
            return
        cursor = conn.cursor()
        cursor.execute(f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{database}') CREATE DATABASE [{database}]")
        conn.commit()
        print(f"Base de données '{database}' créée ou déjà existante.")
    except pyodbc.Error as e:
        print("Erreur lors de la création de la base de données:", str(e))
        return
    
    try:
        # Connexion à la nouvelle base de données et création de la table
        conn = connect_to_sql_server()
        if conn is None:
            return
        cursor = conn.cursor()
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Collection')
            CREATE TABLE Collection (
                id INT PRIMARY KEY IDENTITY(1,1),
                Quantite INT,
                Nom NVARCHAR(255),
                Distillerie NVARCHAR(255),
                Année INT,
                Age INT,
                Degrés FLOAT,
                Date_achat DATE,
                Prix FLOAT
            )
        ''')
        conn.commit()
        print("Table 'Collection' créée ou déjà existante.")
    except pyodbc.Error as e:
        print("Erreur lors de la création de la table 'Collection':", str(e))

if __name__ == "__main__":
    server = 'tcp:sql-sb-marc-weu.database.windows.net'
    database = 'LIBRASKY'
    create_database_and_schema(server, database)