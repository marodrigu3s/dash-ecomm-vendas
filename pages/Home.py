import streamlit as st
import pandas as pd
from dataset import df
from utils import locale
import plotly.express as px
import plotly.graph_objects as go
from streamlit_card import card


st.set_page_config(
    layout='wide'
    ,initial_sidebar_state="collapsed"
    ,page_title='Dashboard'
)

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=False,
)

valor = 0

def main():
    # st.title('Página Inicial')

    marcas = st.multiselect(
        'Marcas'
        ,df['nom_Marca'].unique()
        ,df['nom_Marca'].unique()
    )

    query = '''`nom_Marca` in @marcas'''

    filtered = df.query(query)

    st.markdown('''
        ## Resumo de Vendas Ecommerce
        Dados dos últimos 30 dias.
        ''')

    # st.title('Vendas Ecommerce')
    # st.subheader('Dados dos últimos 30 dias')

    # Cards
    col_Card1, col_Card2, col_Card3 = st.columns(3)
    with st.container():
        valorPedido = 'R$ ' + locale.format_string('%.2f', filtered['vlr_TotalPago'].sum(), grouping=True)
        valorPedidoDia = 'R$ ' + locale.format_string('%.2f',filtered[filtered['dat_Criacao'] == filtered['dat_Criacao'].max()]['vlr_TotalPago'].sum(), grouping=True)
        valorTicketMedio = 'R$ ' + locale.format_string('%.2f',filtered[filtered['dat_Criacao'] > filtered['dat_Criacao'].max() - pd.Timedelta(days=30)]['vlr_TotalPago'].mean(), grouping=True)

        col_Card1.metric(label='Valor Pedidos', value=valorPedido)
        col_Card2.metric(label='Valor Pedidos Dia', value=valorPedidoDia)
        col_Card3.metric(label='Ticket Médio', value=valorTicketMedio)

    with st.container():
        c1, c2 = st.columns(1, 3)
        Card1, Card2, Card3 = st.columns(3)
        quantidadePedido = filtered['id_Pedido'].count()
        quantidadeAguardandoEnvio = filtered[filtered['nom_StatusEnvio'] == 'READY_TO_SHIP']['id_Pedido'].count()


        with c1:
            st.metric(label='Pedidos do Dia', value=quantidadePedido)
            st.metric(label='Aguard. Envio', value=quantidadeAguardandoEnvio)
            st.metric(label='Atrasados', value=quantidadePedido)

        with c2:
            st.dataframe(filtered, hide_index=True)

    with st.container():
        fig1 = go.Figure(go.Indicator(
            mode="number+gauge+delta",
            value=75,
            delta={'reference': 50},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'threshold': {
                    'line': {'color': "black", 'width': 2},
                    'thickness': 0.75,
                    'value': 75},
                'shape': "bullet",
                'axis': {'range': [None, 100]},
                'steps': [
                    {'range': [0, 20], 'color': "#ff4000"},
                    {'range': [20, 40], 'color': "#ffbf00"},
                    {'range': [40, 60], 'color': "#ffff00"},
                    {'range': [60, 80], 'color': "#bfff00"},
                    {'range': [80, 100], 'color': "#00ff00"}],
                'bar': {'color': "black"}
            }))
        fig1.update_layout(height=30, margin={'t': 0, 'b': 0, 'l': 0})
        fig2 = go.Figure(go.Indicator(
            mode="number+gauge+delta",
            value=75,
            delta={'reference': 50},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'threshold': {
                    'line': {'color': "black", 'width': 2},
                    'thickness': 0.75,
                    'value': 75},
                'shape': "bullet",
                'axis': {'range': [None, 100]},
                'steps': [
                    {'range': [0, 20], 'color': "#ff4000"},
                    {'range': [20, 40], 'color': "#ffbf00"},
                    {'range': [40, 60], 'color': "#ffff00"},
                    {'range': [60, 80], 'color': "#bfff00"},
                    {'range': [80, 100], 'color': "#00ff00"}],
                'bar': {'color': "black"}
            }))
        fig2.update_layout(height=30, margin={'t': 0, 'b': 0, 'l': 0})
        fig3 = go.Figure(go.Indicator(
            mode="number+gauge+delta",
            value=75,
            delta={'reference': 50},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'threshold': {
                    'line': {'color': "black", 'width': 2},
                    'thickness': 0.75,
                    'value': 75},
                'shape': "bullet",
                'axis': {'range': [None, 100]},
                'steps': [
                    {'range': [0, 20], 'color': "#ff4000"},
                    {'range': [20, 40], 'color': "#ffbf00"},
                    {'range': [40, 60], 'color': "#ffff00"},
                    {'range': [60, 80], 'color': "#bfff00"},
                    {'range': [80, 100], 'color': "#00ff00"}],
                'bar': {'color': "black"}
            }
        ))
        fig3.update_layout(height=30, margin={'t': 0, 'b': 0, 'l': 0})
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.markdown('Atraso no Envio')
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.markdown('Reclamação')
            st.plotly_chart(fig2, use_container_width=True)
        with col3:
            st.markdown('Cancelamento')
            st.plotly_chart(fig3, use_container_width=True)
        with col4:
            st.markdown('Comercial(9 às 18h)')
            st.plotly_chart(fig1, use_container_width=True)
        with col5:
            st.markdown('Comercial(18 às 00h)')
            st.plotly_chart(fig2, use_container_width=True)
        with col6:
            st.markdown('Sábado e Domingo')
            st.plotly_chart(fig3, use_container_width=True)
    with st.container():
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1:
            st.metric(label='Valor Comissão', value=valor)
        with c2:
            st.metric(label='Valor Impostos', value=valor)
        with c3:
            st.metric(label='% Margem', value=valor)
        with c4:
            st.metric(label='Valor Frete', value=valor)
        with c5:
            st.metric(label='Qtd Devolução', value=valor)
        with c6:
            st.metric(label='Valor Devolução', value=valor)
        with st.container():
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric(label='Toral Visitas', value=valor)
            with c2:
                st.metric(label='Conversão Vendas', value=valor)
            with c3:
                st.metric(label='Msg Pós Vendas', value=valor)
            with c4:
                st.metric(label='Aguardando Resp.', value=100)


    if st.button("Sair"):
        st.switch_page('pages/Login.py')

if __name__ == '__main__':
    main()