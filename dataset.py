import pandas as pd
import pyodbc
import streamlit as st
from datetime import datetime

sqlOptions = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=75.101.154.23;'
            'DATABASE=amz_renault;'
            'UID=sa;'
            'PWD=wU#DjES!I3k@j?ZW9ZJ;'
            'TrustedServerCertificate=yes;'
            'Encrypt=no'
        )

sqlConn = pyodbc.connect(sqlOptions)
sqlCursor = sqlConn.cursor()

sqlOptionsEstoque = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=75.101.154.23;'
            'DATABASE=dw_mercadolivre;'
            'UID=sa;'
            'PWD=wU#DjES!I3k@j?ZW9ZJ;'
            'TrustedServerCertificate=yes;'
            'Encrypt=no'
        )

sqlConnEstoque = pyodbc.connect(sqlOptionsEstoque)
sqlCursorEstoque = sqlConnEstoque.cursor()

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
        ,f.nom_Vendedor
        ,f.id_Pedido
        ,id_Pacote
        ,CASE WHEN id_Pacote IS NULL THEN f.id_Pedido ELSE id_Pacote END AS id_PedidoFinal
        ,id_Envio
        ,dat_Criacao
        ,vlr_TotalPago
        ,flg_Fulfilled
        ,id_Mediacao
        ,b.num_NotaFiscal
        ,cod_SKU
        ,nom_Item
        ,nom_Marca
        ,vlr_ValorEnvio
        ,nom_TipoEnvio
        ,vlr_CustoEnvio
        ,f.cod_Cliente
        ,id_Cliente
        ,nom_ClienteNickname
        ,nom_StatusEnvio
        ,dat_PrevisaoEnvio
        ,vlr_Comissao
        ,qtd_Quantidade
        ,ISNULL(CASE WHEN nom_StatusEnvio NOT IN ('NOT_DELIVERED', 'DELIVERED', 'SHIPPED', 'CANCELLED') 
            THEN DATEDIFF(day, GETDATE(), dat_PrevisaoEnvio) ELSE 0 END,0) num_DiasAtraso
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
        WHEN f.id_Mediacao <> 'NULL' AND f.nom_StatusEnvio <> 'cancelled' THEN 'Decolução'
        WHEN f.nom_StatusEnvio = 'cancelled' THEN 'Cancelado'
        ELSE 'Venda'
        END AS nom_TipoVenda
        ,vlr_TotalPago - ( (vlr_Comissao + ISNULL(b.vlr_Custo,0) + ISNULL(b.vlr_Impostos,0)) - vlr_CustoEnvio) AS vlr_Liquido
        ,ISNULL(CASE
        WHEN b.vlr_Venda = 0 THEN 0.12
        ELSE 
            CASE 
                WHEN f.vlr_TotalPago < 79 THEN 
                    (f.vlr_TotalPago + (CASE
        WHEN f.vlr_TotalPago > 79.90 AND f.nom_TipoEnvio = 'self_service' THEN f.vlr_CustoEnvio
        WHEN f.vlr_TotalPago <= 79.90 AND f.nom_TipoEnvio = 'self_service' THEN f.vlr_ValorEnvio
        WHEN f.vlr_TotalPago <= 79.90 AND f.nom_TipoEnvio = 'self_service' AND f.vlr_CustoEnvio = 0 THEN f.vlr_ValorEnvio
        ELSE -f.vlr_CustoEnvio
        END) - b.vlr_Impostos - vlr_Custo - ((f.vlr_TotalPago * 0.17) + 5)) / b.vlr_Venda
                ELSE 
                    (f.vlr_TotalPago + (CASE
        WHEN f.vlr_TotalPago > 79.90 AND f.nom_TipoEnvio = 'self_service' THEN f.vlr_CustoEnvio
        WHEN f.vlr_TotalPago <= 79.90 AND f.nom_TipoEnvio = 'self_service' THEN f.vlr_ValorEnvio
        WHEN f.vlr_TotalPago <= 79.90 AND f.nom_TipoEnvio = 'self_service' AND f.vlr_CustoEnvio = 0 THEN f.vlr_ValorEnvio
        ELSE -f.vlr_CustoEnvio
        END) - b.vlr_Impostos - vlr_Custo - (f.vlr_TotalPago * 0.17)) / b.vlr_Venda
            END
        END,-999) AS perc_MargemVenda
        ,ISNULL(b.vlr_Custo,0) AS vlr_Custo
        ,ISNULL(b.vlr_Impostos,0) AS vlr_Impostos
    FROM
        fato_Venda f
    left join nbs.dbo.fato_VendaNBS b
    on f.cod_Cliente = b.cod_Cliente
    and f.dat_Criacao = b.dat_Data
    and f.vlr_TotalPago = b.vlr_Venda
    CROSS JOIN
        Totais t
    
    '''

df = pd.read_sql(query, sqlConn)


def kpi_icon(current_value):
    if current_value >= 0.12:
        return f"🟢 {current_value:.2%}"
    elif 0.08 <= current_value < 0.12:
        return f"🟡 {current_value:.2%}"
    elif current_value == -999:
        current_value = 0
        return f"🟠 {current_value:.2%}"
    else:
        return f"🔴 {current_value:.2%}"

dfDetalhado = df

dfDetalhado['%'] = dfDetalhado['perc_MargemVenda'].apply(kpi_icon)

dfDetalhado = dfDetalhado[['dat_Criacao','id_PedidoFinal','num_NotaFiscal','nom_TipoVenda','vlr_TotalPago','vlr_Comissao','vlr_FreteFinal','vlr_Impostos','vlr_Custo','vlr_Liquido','%','nom_Item']].rename(
    columns={'dat_Criacao': 'Data'
        ,'id_PedidoFinal': 'Pedido'
        ,'vlr_TotalPago': 'Venda'
        ,'num_NotaFiscal': 'Nota Fiscal'
        ,'nom_TipoVenda': 'Tipo Venda'
        ,'vlr_Comissao': 'Comissão'
        ,'vlr_FreteFinal': 'Frete'
        ,'vlr_Impostos': 'Impostos'
        ,'vlr_Custo': 'Custo'
        ,'vlr_Liquido': 'Líq. ML'
        ,'nom_Item': 'Descrição Item'
     })


dfTop10 = pd.DataFrame(df,
                       columns=['dat_Criacao', 'id_PedidoFinal', 'vlr_TotalPago', 'vlr_FreteFinal', 'vlr_Liquido',
                                'perc_MargemVenda'])

for col in dfTop10.columns:
    if col.startswith('vlr_'):
        dfTop10[col] = dfTop10[col].apply(lambda x: f"{x:.2f}")

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

@st.cache_data
def get_api_data():
    queryEstoque = '''
        select top 100 * FROM nbs.fato_Estoque
        '''

    dfEstoque = pd.read_sql(queryEstoque, sqlConnEstoque)

    def kpi_iconQTD(current_value):
        if current_value >= 10:
            return f"🟢"
        elif current_value >= 5:
            return f"🟡"
        elif current_value >= 0:
            return f"🟠"
        else:
            return f"🔴"

    dfEstoque['Status'] = dfEstoque['qtd_Estoque'].apply(kpi_iconQTD)

    dfEstoque = dfEstoque[['Status'
                            ,'cod_Matriz'
                            ,'cod_Empresa'
                            ,'cod_Fornecedor'
                            ,'nom_Fornecedor'
                            ,'cod_Item'
                            ,'nom_Item'
                            ,'qtd_Estoque'
                            ,'qtd_Alocado'
                            ,'vlr_CustoContabil'
                            ,'vlr_Reposicao'
                            ,'vlr_Markup'
                            ,'vlr_Venda'
                            ,'cod_CFV'
                            ,'nom_GrupoINTerno']].rename(
        columns={'cod_Matriz' : 'Cod. Matriz'
          ,'cod_Empresa' : 'Cod. Empresa'
          ,'cod_Fornecedor' : 'Cod. Forcenedor'
          ,'nom_Fornecedor' : 'Fornecedor'
          ,'cod_Item' : 'SKU'
          ,'nom_Item' : 'Item'
          ,'qtd_Estoque' : 'Quantidade'
          ,'qtd_Alocado' : 'Alocado'
          ,'vlr_CustoContabil' : 'Custo Contabil'
          ,'vlr_Reposicao' : 'Reposição'
          ,'vlr_Markup' : 'Markup'
          ,'vlr_Venda' : 'Venda'
          ,'cod_CFV' : 'CFV'
          ,'nom_GrupoINTerno' : 'Grupo Interno'
         })

    return dfEstoque

