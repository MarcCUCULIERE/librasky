import pyodbc

def create_database_and_schema(server, database, username, password):
    driver = '{ODBC Driver 17 for SQL Server}'
    master_conn_str = f'DRIVER={driver};SERVER={server};DATABASE=master;UID={username};PWD={password}'
    db_conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Étape 1 & 2: Connexion à la base de données système et création de la base de données
    try:
        with pyodbc.connect(master_conn_str) as conn:
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{database}') CREATE DATABASE [{database}]")
            print(f"Base de données '{database}' créée ou déjà existante.")
    except pyodbc.Error as e:
        print("Erreur lors de la création de la base de données:", str(e))
        return
    
    # Étape 3 & 4: Connexion à la nouvelle base de données et création de la table
    try:
        with pyodbc.connect(db_conn_str) as conn:
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
            print("Table 'Collection' créée ou déjà existante.")
    except pyodbc.Error as e:
        print("Erreur lors de la création de la table 'Collection':", str(e))

if __name__ == "__main__":
    server = 'sql-sb-marc-weu.database.windows.net'
    database = ''
    username = ''
    password = ''
create_database_and_schema(server, database, username, password)
