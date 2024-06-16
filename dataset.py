import pandas as pd
import pyodbc

sqlOptions = (
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=75.101.154.23;'
            'DATABASE=amz_renault;'
            'UID=sa;'
            'PWD=wU#DjES!I3k@j?ZW9ZJ;'
            'TrustedServerCertificate=yes;'
            'Encrypt=no'
        )

sqlConn = pyodbc.connect(sqlOptions)
sqlCursor = sqlConn.cursor()

query = '''
    select 
        *
    from 
        fato_Venda
    '''

df = pd.read_sql(query, sqlConn)