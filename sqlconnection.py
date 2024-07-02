database_type = 'mssql+pyodbc'
user = 'sa'
password = 'wU#DjES!I3k@j?ZW9ZJ'
host = '75.101.154.23'
database = 'amz_renault'

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Configurar a string de conexão
connection_string = f'mssql+pyodbc://{user}:{password}@{host}:1433/{database}?driver=FreeTDS'

# Criar a engine de conexão
engine = create_engine(connection_string)

# Criar uma sessão
Session = sessionmaker(bind=engine)
session = Session()

# Testar a conexão com uma consulta simples
try:
    result = session.execute(text("SELECT 1"))
    for row in result:
        print(row)
    print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")

# Fechar a sessão
session.close()