import pandas as pd
import pyodbc
from datetime import datetime

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
    WITH Totais AS (
        SELECT
            SUM(vlr_TotalPago) AS SUM_vlr_Valor
            --,vlr_TotalPago - ( (vlr_Comissao + 0 + 0) - vlr_CustoEnvio) AS vlr_Liquido
        FROM
            fato_Venda
    )
    SELECT 
        id_Periodo
        ,id_Vendedor
        ,nom_Vendedor
        ,id_Pedido
        ,id_Pacote
        ,CASE WHEN id_Pacote IS NULL THEN id_Pedido ELSE id_Pacote END AS id_PedidoFinal
        ,id_Envio
        ,dat_Criacao
        ,vlr_TotalPago
        ,flg_Fulfilled
        ,id_Mediacao
        ,num_NotaFiscal
        ,cod_SKU
        ,nom_Item
        ,nom_Marca
        ,vlr_ValorEnvio
        ,nom_TipoEnvio
        ,vlr_CustoEnvio
        ,cod_Cliente
        ,id_Cliente
        ,nom_ClienteNickname
        ,nom_StatusEnvio
        ,dat_PrevisaoEnvio
        ,vlr_Comissao
        ,qtd_Quantidade
        ,DATEDIFF(day, GETDATE(), dat_PrevisaoEnvio) num_DiasAtraso
        ,CASE
        WHEN f.vlr_TotalPago > 79.90 AND f.nom_TipoEnvio = 'self_service' THEN f.vlr_CustoEnvio
        WHEN f.vlr_TotalPago <= 79.90 AND f.nom_TipoEnvio = 'self_service' THEN f.vlr_ValorEnvio
        WHEN f.vlr_TotalPago <= 79.90 AND f.nom_TipoEnvio = 'self_service' AND f.vlr_CustoEnvio = 0 THEN f.vlr_ValorEnvio
        ELSE -f.vlr_CustoEnvio
        END AS vlr_FreteFinal
        ,CASE
        WHEN f.id_Mediacao <> 'NULL' AND f.nom_StatusEnvio <> 'cancelled' THEN - f.vlr_TotalPago + f.vlr_CustoEnvio
        ELSE 0
        END AS vlr_Devolucao
        ,CASE
        WHEN f.id_Mediacao <> 'NULL' AND f.nom_StatusEnvio <> 'cancelled' THEN 'D'
        WHEN f.nom_StatusEnvio = 'cancelled' THEN 'C'
        ELSE 'V'
        END AS flg_Devolucao
        ,vlr_TotalPago - ( (vlr_Comissao + 0 + 0) - vlr_CustoEnvio) AS vlr_Liquido
        ,CASE
        WHEN t.SUM_vlr_Valor = 0 THEN 0.12
        ELSE ((vlr_TotalPago - ( (vlr_Comissao + 0 + 0) - vlr_CustoEnvio))/ t.SUM_vlr_Valor) * 100
        END AS perc_MargemVenda
    FROM
        fato_Venda f
    CROSS JOIN
        Totais t;
    '''

df = pd.read_sql(query, sqlConn)


def kpi_icon(current_value):
    if current_value >= 0.12:
        return f"🟢 {current_value:.2%}"
    elif 0.08 <= current_value < 0.12:
        return f"🟡 {current_value:.2%}"
    else:
        return f"🔴 {current_value:.2%}"

dfTop10 = pd.DataFrame(df,
                       columns=['dat_Criacao', 'id_PedidoFinal', 'vlr_TotalPago', 'vlr_FreteFinal', 'vlr_Liquido',
                                'perc_MargemVenda'])

for col in dfTop10.columns:
    if col.startswith('vlr_'):
        dfTop10[col] = dfTop10[col].apply(lambda x: f"{x:,.2f}")

dfTop10 = dfTop10.sort_values(by='dat_Criacao', ascending=False).head(10).rename(
    columns={'dat_Criacao':'Data'
     ,'id_PedidoFinal': 'Pedido'
    ,'vlr_TotalPago': 'Venda'
    ,'vlr_FreteFinal': 'Frete'
    ,'vlr_Liquido':'Líq. ML'
    ,'perc_MargemVenda':'%'
     })

dfTop10['%'] = dfTop10['%'].apply(kpi_icon)

queryMetrica = '''
    select * from fato_NotaMetrica
    '''

dfMetrica = pd.read_sql(queryMetrica, sqlConn)

queryMetricaTempoResp = '''
    select * from fato_TempoResposta
    '''

dfMetricaTempoResp = pd.read_sql(queryMetricaTempoResp, sqlConn)

queryVisita = '''
    select * from fato_Visita where dat_Visita >= DATEADD(DAY,-30,GETDATE())
    '''

dfVisita = pd.read_sql(queryVisita, sqlConn)


queryPosVenda = '''
    select * from fato_PosVenda
    '''

dfPosVenda = pd.read_sql(queryPosVenda, sqlConn)

queryPergunta = '''
    select * from fato_Pergunta
    '''

dfPergunta = pd.read_sql(queryPergunta, sqlConn)