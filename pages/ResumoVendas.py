import streamlit as st
import pandas as pd
from dataset import df, dfMetrica, dfMetricaTempoResp, dfVisita, dfPosVenda, dfPergunta
from utils import locale
import plotly.express as px
import plotly.graph_objects as go
from streamlit_card import card
import yaml
from yaml import SafeLoader
import streamlit_authenticator as stauth
import toml

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

def dashboard():
    # st.title('Página Inicial')
    if st.session_state["authentication_status"]:
        col1, col2 = st.columns((6,1))
        with col1:
            st.write(f'Olá *{st.session_state["name"]}*!')
        with col2:
            teste = authenticator.logout('Logout', 'main')
            if teste:
                st.switch_page('pages/Login.py')
    aba1, aba2 = st.tabs(['Resumo', 'Detalhado'])

    #marcas = st.multiselect(
    #    'Marcas'
    #    ,df['nom_Marca'].unique()
    #    ,df['nom_Marca'].unique()
    #)
#
    #query = '''`nom_Marca` in @marcas'''
#
    #filtered = df.query(query)

    filtered = df
    with aba1:
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
            valorPedidoDia = 'R$ ' + locale.format_string('%.2f', filtered[
                filtered['dat_Criacao'] == filtered['dat_Criacao'].max()]['vlr_TotalPago'].sum(), grouping=True)
            valorTicketMedio = 'R$ ' + locale.format_string('%.2f', filtered[
                filtered['dat_Criacao'] > filtered['dat_Criacao'].max() - pd.Timedelta(days=30)][
                'vlr_TotalPago'].mean(), grouping=True)

            #
            col_Card1.metric(label='Valor Pedidos', value=valorPedido)
            col_Card2.metric(label='Valor Pedidos Dia', value=valorPedidoDia)
            col_Card3.metric(label='Ticket Médio', value=valorTicketMedio)

        with st.container():
            c1, c2 = st.columns((1, 3))
            # Card1, Card2, Card3 = st.columns(3)
            quantidadePedido = '{:,}'.format(filtered['id_Pedido'].count())
            quantidadeAguardandoEnvio = '{:,}'.format(
                filtered[filtered['nom_StatusEnvio'] == 'READY_TO_SHIP']['id_Pedido'].count())
            quantidadeAtrasados = '{:,}'.format(
                filtered[(filtered['num_DiasAtraso'] > 0) & (filtered['dat_PrevisaoEnvio'] == 'READY_TO_SHIP')][
                    'id_Pedido'].count())

            with c1:
                st.metric(label='Pedidos do Dia', value=quantidadePedido)
                st.metric(label='Aguard. Envio', value=quantidadeAguardandoEnvio)
                st.metric(label='Atrasados', value=quantidadeAtrasados)

            with c2:
                st.dataframe(filtered, hide_index=True)

        with st.container():
            metricaAtraso = ((dfMetrica['num_NotaAtrasoEnvio'].iloc[0] * 100) - 100) * -1
            metricaReclamacao = ((dfMetrica['num_NotaReclamacao'] * 100) - 100) * -1
            metricaCancelamento = ((dfMetrica['num_NotaCancelamento'] * 100) - 100) * -1
            metricaComercial = dfMetricaTempoResp['num_HoraUtil'].iloc[0] / 60
            metricaForaComercial = dfMetricaTempoResp['num_HoraExtra'].iloc[0] / 60
            metricaFDS = dfMetricaTempoResp['num_HoraFDS'].iloc[0] / 60
            fig1 = go.Figure(go.Indicator(
                mode="number+gauge+delta",
                value=float(metricaAtraso),
                # delta={'reference': 50},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'threshold': {
                        'line': {'color': "black", 'width': 2},
                        'thickness': 0.75,
                        'value': float(metricaAtraso)},
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
                value=float(metricaReclamacao),
                # delta={'reference': 50},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'threshold': {
                        'line': {'color': "black", 'width': 2},
                        'thickness': 0.75,
                        'value': float(metricaReclamacao)},
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
                value=float(metricaCancelamento),
                # delta={'reference': 50},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'threshold': {
                        'line': {'color': "black", 'width': 2},
                        'thickness': 0.75,
                        'value': float(metricaCancelamento)},
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
            fig4 = go.Figure(go.Indicator(
                mode="number+gauge+delta",
                value=metricaComercial,
                # delta={'reference': 50},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'threshold': {
                        'line': {'color': "black", 'width': 2},
                        'thickness': 0.75,
                        'value': metricaComercial},
                    'shape': "bullet",
                    'axis': {'range': [None, 100]},
                    'steps': [
                        {'range': [0, 20], 'color': "#00ff00"},
                        {'range': [20, 40], 'color': "#bfff00"},
                        {'range': [40, 60], 'color': "#ffff00"},
                        {'range': [60, 80], 'color': "#ffbf00"},
                        {'range': [80, 100], 'color': "#ff4000"}],
                    'bar': {'color': "black"}
                }
            ))
            fig4.update_layout(height=30, margin={'t': 0, 'b': 0, 'l': 0})
            fig5 = go.Figure(go.Indicator(
                mode="number+gauge+delta",
                value=metricaForaComercial,
                # delta={'reference': 50},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'threshold': {
                        'line': {'color': "black", 'width': 2},
                        'thickness': 0.75,
                        'value': metricaForaComercial},
                    'shape': "bullet",
                    'axis': {'range': [None, 100]},
                    'steps': [
                        {'range': [0, 20], 'color': "#00ff00"},
                        {'range': [20, 40], 'color': "#bfff00"},
                        {'range': [40, 60], 'color': "#ffff00"},
                        {'range': [60, 80], 'color': "#ffbf00"},
                        {'range': [80, 100], 'color': "#ff4000"}],
                    'bar': {'color': "black"}
                }
            ))
            fig5.update_layout(height=30, margin={'t': 0, 'b': 0, 'l': 0})
            fig6 = go.Figure(go.Indicator(
                mode="number+gauge+delta",
                value=metricaFDS,
                # delta={'reference': 50},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'threshold': {
                        'line': {'color': "black", 'width': 2},
                        'thickness': 0.75,
                        'value': metricaFDS},
                    'shape': "bullet",
                    'axis': {'range': [None, 100]},
                    'steps': [
                        {'range': [0, 20], 'color': "#00ff00"},
                        {'range': [20, 40], 'color': "#bfff00"},
                        {'range': [40, 60], 'color': "#ffff00"},
                        {'range': [60, 80], 'color': "#ffbf00"},
                        {'range': [80, 100], 'color': "#ff4000"}],
                    'bar': {'color': "black"}
                }
            ))
            fig6.update_layout(height=30, margin={'t': 0, 'b': 0, 'l': 0})
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
                st.plotly_chart(fig4, use_container_width=True)
            with col5:
                st.markdown('Comercial(18 às 00h)')
                st.plotly_chart(fig5, use_container_width=True)
            with col6:
                st.markdown('Sábado e Domingo')
                st.plotly_chart(fig6, use_container_width=True)
        with st.container():
            c1, c2, c3, c4, c5, c6 = st.columns(6)
            with c1:
                cardValorComissao = 'R$ ' + locale.format_string('%.2f', filtered['vlr_Comissao'].sum(), grouping=True)
                st.metric(label='Valor Comissão', value=cardValorComissao)
            with c2:
                cardValorImpostos = 'R$ ' + locale.format_string('%.2f', 0,
                                                                 grouping=True)  # filtered['vlr_Comissao'].sum()
                st.metric(label='Valor Impostos', value=cardValorImpostos)
            with c3:
                cardPercentualaMargem = filtered['perc_MargemVenda'].mean()
                cardPercentualaMargem = '{:.2%}'.format(cardPercentualaMargem * 100)
                st.metric(label='% Margem', value=cardPercentualaMargem)
            with c4:
                cardValorFrete = 'R$ ' + locale.format_string('%.2f', filtered['vlr_FreteFinal'].sum(), grouping=True)
                st.metric(label='Valor Frete', value=cardValorFrete)
            with c5:
                cardQuantidadeDevolucao = '{:,}'.format(filtered['id_Mediacao'].nunique())
                st.metric(label='Qtd Devolução', value=cardQuantidadeDevolucao)
            with c6:
                carValorDevolucao = 'R$ ' + locale.format_string('%.2f', filtered['vlr_Devolucao'].sum(), grouping=True)
                st.metric(label='Valor Devolução', value=carValorDevolucao)
            with st.container():
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    cardTotalVisita = '{:,}'.format(dfVisita['num_TotalVisita'].sum())
                    st.metric(label='Total Visitas', value=cardTotalVisita)
                with c2:
                    cardConversaoVenda = '{:.2%}'.format(
                        filtered['id_Pedido'].count() / dfVisita['num_TotalVisita'].sum())
                    st.metric(label='Conversão Vendas', value=cardConversaoVenda)
                with c3:
                    try:
                        cardPosVenda = '{:,}'.format(dfPosVenda['qtd_MSG'].sum())
                    except:
                        cardPosVenda = 0
                    st.metric(label='Msg Pós Vendas', value=cardPosVenda)
                with c4:
                    cardAguardandoResp = '{:,}'.format(
                        dfPergunta[dfPergunta['nom_Status'] == 'UNANSWERED']['id_Vendedor'].count())
                    st.metric(label='Aguardando Resp.', value=cardAguardandoResp)

    with aba2:
        st.dataframe(filtered)


if __name__ == '__main__':
    dashboard()