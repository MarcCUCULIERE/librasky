import os
import pyodbc
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Azure Key Vault configuration
key_vault_name = os.environ.get('KEY_VAULT_NAME')
key_vault_uri = f"https://{key_vault_name}.vault.azure.net"

# Initialize the Azure Key Vault client
credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_uri, credential=credential)

def get_secret(secret_name):
    """Retrieve a secret from Azure Key Vault."""
    try:
        secret = client.get_secret(secret_name)
        logger.debug(f"Secret {secret_name} retrieved successfully")
        return secret.value
    except Exception as e:
        logger.error(f"Error retrieving secret {secret_name}: {e}")
        return None

def get_connection_string():
    """Generate the connection string for SQL Server."""
    server = 'sql-sb-marc-weu-01.database.windows.net'
    database = 'LIBRASKY'
    driver = '{ODBC Driver 17 for SQL Server}'
    username = get_secret('DB-USERNAME')
    password = get_secret('DB-PASSWORD')
    logger.debug(f"Username: {username}")
    logger.debug(f"Password: {password}")
    logger.debug(f"Server: {server}")
    logger.debug(f"Database: {database}")
    return f'DRIVER={driver};SERVER={server};DATABASE={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'

def connect_to_sql_server():
    """Function to connect to SQL Server database using username and password."""
    connection_string = get_connection_string()
    try:
        conn = pyodbc.connect(connection_string)
        logger.info("Connected to SQL Server")
        return conn
    except pyodbc.Error as e:
        logger.error(f"Error connecting to SQL Server: {e}")
        return None

def execute_query(query, params=None):
    """Execute a SQL query with optional parameters."""
    logger.debug(f"Executing query: {query} with params: {params}")
    conn = connect_to_sql_server()
    if conn is None:
        logger.error("Connection to SQL Server failed")
        return None, None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        logger.info("Query executed successfully")
        return conn, cursor
    except pyodbc.Error as e:
        logger.error(f"Error executing query: {e}")
        if conn:
            conn.close()
        return None, None

def fetch_data():
    """Fetch data from the database."""
    query = "SELECT Quantite, Nom, Distillerie, Année, Age, Degrés, Date_achat, Prix FROM Collection"
    conn = connect_to_sql_server()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in data]
            conn.close()
            return results
        except pyodbc.Error as e:
            logger.error(f"Error executing query: {e}")
            conn.close()
            return None
    else:
        return None

def create_database_and_schema():
    database_creation_query = "IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'LIBRASKY') CREATE DATABASE [LIBRASKY]"
    table_creation_query = '''
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
    '''
    if execute_query(database_creation_query):
        logger.info("Database 'LIBRASKY' created or already exists.")
    if execute_query(table_creation_query):
        logger.info("Table 'Collection' created or already exists.")

if __name__ == "__main__":
    create_database_and_schema()