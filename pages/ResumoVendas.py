import streamlit as st
import pandas as pd
from dataset import df, dfMetrica, dfMetricaTempoResp, dfVisita, dfPosVenda, dfPergunta, dfTop10
from utils import locale
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
from streamlit_card import card
import yaml
from yaml import SafeLoader
import streamlit_authenticator as stauth
import toml

def dashboard():
    # st.title('Página Inicial')
    #if st.session_state["authentication_status"]:
    #    col1, col2 = st.columns((6,1))
    #    with col1:
    #        st.write(f'Olá *{st.session_state["name"]}*!')
    #    with col2:
    #        teste = authenticator.logout('Logout', 'main')
    #        if teste:
    #            st.switch_page('pages/Login.py')
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
            quantidadePedido = filtered[filtered['id_Periodo'] == filtered['id_Periodo'].max()]['id_Pedido'].count()
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
                st.write("Top 10 - Vendas Recentes")
                st.dataframe(dfTop10.style.set_sticky(axis="index"), hide_index=True,)

        with st.container():
            metricaAtraso = ((dfMetrica['num_NotaAtrasoEnvio'].iloc[0] * 100) - 100) * -1
            metricaReclamacao = ((dfMetrica['num_NotaReclamacao'].iloc[0] * 100) - 100) * -1
            metricaCancelamento = ((dfMetrica['num_NotaCancelamento'].iloc[0] * 100) - 100) * -1
            metricaComercialStr = f"{dfMetricaTempoResp['num_HoraUtil'].iloc[0] / 60:.2f}"
            metricaComercial = dfMetricaTempoResp['num_HoraUtil'].iloc[0] / 60
            metricaForaComercialSTR = f"{dfMetricaTempoResp['num_HoraExtra'].iloc[0] / 60:.2f}"
            metricaForaComercial = dfMetricaTempoResp['num_HoraExtra'].iloc[0] / 60
            metricaFDSSTR = f"{dfMetricaTempoResp['num_HoraFDS'].iloc[0] / 60:.2f}"
            metricaFDS = dfMetricaTempoResp['num_HoraFDS'].iloc[0] / 60

            #fig1 = go.Figure(go.Indicator(
            #    mode="number+gauge+delta",
            #    value=float(metricaAtraso),
            #    # delta={'reference': 50},
            #    domain={'x': [0, 1], 'y': [0, 1]},
            #    gauge={
            #        'threshold': {
            #            'line': {'color': "black", 'width': 2},
            #            'thickness': 0.75,
            #            'value': float(metricaAtraso)},
            #        'shape': "bullet",
            #        'axis': {'range': [None, 100]},
            #        'steps': [
            #            {'range': [0, 20], 'color': "#ff4000"},
            #            {'range': [20, 40], 'color': "#ffbf00"},
            #            {'range': [40, 60], 'color': "#ffff00"},
            #            {'range': [60, 80], 'color': "#bfff00"},
            #            {'range': [80, 100], 'color': "#00ff00"}],
            #        'bar': {'color': "black"}
            #    }))
            #fig1.update_layout(height=30, margin={'t': 0, 'b': 0, 'l': 0})
            #fig2 = go.Figure(go.Indicator(
            #    mode="number+gauge+delta",
            #    value=float(metricaReclamacao),
            #    # delta={'reference': 50},
            #    domain={'x': [0, 1], 'y': [0, 1]},
            #    gauge={
            #        'threshold': {
            #            'line': {'color': "black", 'width': 2},
            #            'thickness': 0.75,
            #            'value': float(metricaReclamacao)},
            #        'shape': "bullet",
            #        'axis': {'range': [None, 100]},
            #        'steps': [
            #            {'range': [0, 20], 'color': "#ff4000"},
            #            {'range': [20, 40], 'color': "#ffbf00"},
            #            {'range': [40, 60], 'color': "#ffff00"},
            #            {'range': [60, 80], 'color': "#bfff00"},
            #            {'range': [80, 100], 'color': "#00ff00"}],
            #        'bar': {'color': "black"}
            #    }))
            #fig2.update_layout(height=30, margin={'t': 0, 'b': 0, 'l': 0})
            #fig3 = go.Figure(go.Indicator(
            #    mode="number+gauge+delta",
            #    value=float(metricaCancelamento),
            #    # delta={'reference': 50},
            #    domain={'x': [0, 1], 'y': [0, 1]},
            #    gauge={
            #        'threshold': {
            #            'line': {'color': "black", 'width': 2},
            #            'thickness': 0.75,
            #            'value': float(metricaCancelamento)},
            #        'shape': "bullet",
            #        'axis': {'range': [None, 100]},
            #        'steps': [
            #            {'range': [0, 20], 'color': "#ff4000"},
            #            {'range': [20, 40], 'color': "#ffbf00"},
            #            {'range': [40, 60], 'color': "#ffff00"},
            #            {'range': [60, 80], 'color': "#bfff00"},
            #            {'range': [80, 100], 'color': "#00ff00"}],
            #        'bar': {'color': "black"}
            #    }
            #))
            #fig3.update_layout(height=30, margin={'t': 0, 'b': 0, 'l': 0})
            #fig4 = go.Figure(go.Indicator(
            #    mode="number+gauge+delta",
            #    value=metricaComercial,
            #    # delta={'reference': 50},
            #    domain={'x': [0, 1], 'y': [0, 1]},
            #    gauge={
            #        'threshold': {
            #            'line': {'color': "black", 'width': 2},
            #            'thickness': 0.75,
            #            'value': metricaComercial},
            #        'shape': "bullet",
            #        'axis': {'range': [None, 100]},
            #        'steps': [
            #            {'range': [0, 20], 'color': "#00ff00"},
            #            {'range': [20, 40], 'color': "#bfff00"},
            #            {'range': [40, 60], 'color': "#ffff00"},
            #            {'range': [60, 80], 'color': "#ffbf00"},
            #            {'range': [80, 100], 'color': "#ff4000"}],
            #        'bar': {'color': "black"}
            #    }
            #))
            #fig4.update_layout(height=30, margin={'t': 0, 'b': 0, 'l': 0})
            #fig5 = go.Figure(go.Indicator(
            #    mode="number+gauge+delta",
            #    value=metricaForaComercial,
            #    # delta={'reference': 50},
            #    domain={'x': [0, 1], 'y': [0, 1]},
            #    gauge={
            #        'threshold': {
            #            'line': {'color': "black", 'width': 2},
            #            'thickness': 0.75,
            #            'value': metricaForaComercial},
            #        'shape': "bullet",
            #        'axis': {'range': [None, 100]},
            #        'steps': [
            #            {'range': [0, 20], 'color': "#00ff00"},
            #            {'range': [20, 40], 'color': "#bfff00"},
            #            {'range': [40, 60], 'color': "#ffff00"},
            #            {'range': [60, 80], 'color': "#ffbf00"},
            #            {'range': [80, 100], 'color': "#ff4000"}],
            #        'bar': {'color': "black"}
            #    }
            #))
            #fig5.update_layout(height=30, margin={'t': 0, 'b': 0, 'l': 0})
            #fig6 = go.Figure(go.Indicator(
            #    mode="number+gauge+delta",
            #    value=metricaFDS,
            #    # delta={'reference': 50},
            #    domain={'x': [0, 1], 'y': [0, 1]},
            #    gauge={
            #        'threshold': {
            #            'line': {'color': "black", 'width': 2},
            #            'thickness': 0.75,
            #            'value': metricaFDS},
            #        'shape': "bullet",
            #        'axis': {'range': [None, 100]},
            #        'steps': [
            #            {'range': [0, 20], 'color': "#00ff00"},
            #            {'range': [20, 40], 'color': "#bfff00"},
            #            {'range': [40, 60], 'color': "#ffff00"},
            #            {'range': [60, 80], 'color': "#ffbf00"},
            #            {'range': [80, 100], 'color': "#ff4000"}],
            #        'bar': {'color': "black"}
            #    }
            #))
            #fig6.update_layout(height=30, margin={'t': 0, 'b': 0, 'l': 0})
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                def determine_color(value):
                    if value >= 80:
                        return "#31b93c"
                    elif value >= 60:
                        return "#baff20"
                    elif value >= 40:
                        return "#fff044"
                    elif value >= 20:
                        return "#ffb657"
                    else:
                        return "#ff605a"

                color_metricaAtraso = determine_color(metricaAtraso)

                # HTML e CSS para a barra de progresso
                progress_metricaAtraso = f"""
                    <div class="outer-wrapper">
                        <div class="column-wrapper">
                            <div class="column" style="width: {metricaAtraso}%; background: {color_metricaAtraso};"></div>
                        </div>
                        <div class="percentage" style="font-size: 11px">Atraso Envio {metricaAtraso}%</div>
                    </div>
                    <style>
                        .outer-wrappers {{
                            display: inline-block;
                            margin: 5px 15px;
                            padding: 25px 15px;
                            background: #eee;
                            min-width: 300px;
                            text-align: center;
                            
                        }}
                        .column-wrapper {{
                            width: 100%;
                            height: 20px;
                            background: #CFD8DC;
                            margin: 0 auto;
                            overflow: hidden;
                            position: relative;
                        }}
                        .column {{
                            height: 20px;
                            position: absolute;
                            left: 0;
                        }}
                        .percentage {{
                            margin-top: 10px;
                            padding: 5px 10px;
                            color: #FFF;
                            background: #262730;
                            position: relative;
                            border-radius: 4px;
                            text-align: center;
                            font-family: sans-serif;
                        }}
                    </style>
                    """

                # Renderizar o HTML no Streamlit
                st.components.v1.html(progress_metricaAtraso, height=80)

            with col2:

                color_metricaReclamacao = determine_color(metricaReclamacao)

                # HTML e CSS para a barra de progresso
                progress_metricaReclamacao = f"""
                                    <div class="outer-wrapper">
                                        <div class="column-wrapper">
                                            <div class="column" style="width: {metricaReclamacao}%; background: {color_metricaReclamacao};"></div>
                                        </div>
                                        <div class="percentage" style="font-size: 11px">Reclamação {metricaReclamacao}%</div>
                                    </div>
                                    <style>
                                        .outer-wrappers {{
                                            display: inline-block;
                                            margin: 5px 15px;
                                            padding: 25px 15px;
                                            background: #eee;
                                            min-width: 300px;
                                            text-align: center;

                                        }}
                                        .column-wrapper {{
                                            width: 100%;
                                            height: 20px;
                                            background: #CFD8DC;
                                            margin: 0 auto;
                                            overflow: hidden;
                                            position: relative;
                                        }}
                                        .column {{
                                            height: 20px;
                                            position: absolute;
                                            left: 0;
                                        }}
                                        .percentage {{
                                            margin-top: 10px;
                                            padding: 5px 10px;
                                            color: #FFF;
                                            background: #262730;
                                            position: relative;
                                            border-radius: 4px;
                                            text-align: center;
                                            font-family: sans-serif;
                                        }}
                                    </style>
                                    """

                # Renderizar o HTML no Streamlit
                st.components.v1.html(progress_metricaReclamacao, height=80)
            with col3:

                color_metricaCancelamento = determine_color(metricaCancelamento)

                # HTML e CSS para a barra de progresso
                progress_metricaCancelamento = f"""
                                    <div class="outer-wrapper">
                                        <div class="column-wrapper">
                                            <div class="column" style="width: {metricaCancelamento}%; background: {color_metricaCancelamento};"></div>
                                        </div>
                                        <div class="percentage" style="font-size: 11px">Cancelamento {metricaCancelamento}%</div>
                                    </div>
                                    <style>
                                        .outer-wrappers {{
                                            display: inline-block;
                                            margin: 5px 15px;
                                            padding: 25px 15px;
                                            background: #eee;
                                            min-width: 300px;
                                            text-align: center;
                                        }}
                                        .column-wrapper {{
                                            width: 100%;
                                            height: 20px;
                                            background: #CFD8DC;
                                            margin: 0 auto;
                                            overflow: hidden;
                                            position: relative;
                                        }}
                                        .column {{
                                            height: 20px;
                                            position: absolute;
                                            left: 0;
                                        }}
                                        .percentage {{
                                            margin-top: 10px;
                                            padding: 5px 10px;
                                            color: #FFF;
                                            background: #262730;
                                            position: relative;
                                            border-radius: 4px;
                                            text-align: center;
                                            font-family: sans-serif;
                                        }}
                                    </style>
                                    """

                # Renderizar o HTML no Streamlit
                st.components.v1.html(progress_metricaCancelamento, height=80)
            with col4:
                def determine_color2(value):
                    if value >= 80:
                        return "#ff605a"
                    elif value >= 60:
                        return "#ffb657"
                    elif value >= 40:
                        return "#fff044"
                    elif value >= 20:
                        return "#baff20"
                    else:
                        return "#31b93c"

                color_metricaComercial = determine_color2(metricaComercial)

                # HTML e CSS para a barra de progresso
                progress_metricaComercial = f"""
                                    <div class="outer-wrapper">
                                        <div class="column-wrapper">
                                            <div class="column" style="width: {metricaComercial}%; background: {color_metricaComercial};"></div>
                                        </div>
                                        <div class="percentage" style="font-size: 11px">Resp. 6h-18h {metricaComercialStr}%</div>
                                    </div>
                                    <style>
                                        .outer-wrappers {{
                                            display: inline-block;
                                            margin: 5px 15px;
                                            padding: 25px 15px;
                                            background: #eee;
                                            min-width: 300px;
                                            text-align: center;

                                        }}
                                        .column-wrapper {{
                                            width: 100%;
                                            height: 20px;
                                            background: #CFD8DC;
                                            margin: 0 auto;
                                            overflow: hidden;
                                            position: relative;
                                        }}
                                        .column {{
                                            height: 20px;
                                            position: absolute;
                                            left: 0;
                                        }}
                                        .percentage {{
                                            margin-top: 10px;
                                            padding: 5px 10px;
                                            color: #FFF;
                                            background: #262730;
                                            position: relative;
                                            border-radius: 4px;
                                            text-align: center;
                                            font-family: sans-serif;
                                        }}
                                    </style>
                                    """

                # Renderizar o HTML no Streamlit
                st.components.v1.html(progress_metricaComercial, height=80)
            with col5:

                color_metricaForaComercial = determine_color2(metricaForaComercial)

                # HTML e CSS para a barra de progresso
                progress_metricaForaComercial = f"""
                                    <div class="outer-wrapper">
                                        <div class="column-wrapper">
                                            <div class="column" style="width: {metricaForaComercial}%; background: {color_metricaForaComercial};"></div>
                                        </div>
                                        <div class="percentage" style="font-size: 11px">Resp. 18h-00h {metricaForaComercialSTR}%</div>
                                    </div>
                                    <style>
                                        .outer-wrappers {{
                                            display: inline-block;
                                            margin: 5px 15px;
                                            padding: 25px 15px;
                                            background: #eee;
                                            min-width: 300px;
                                            text-align: center;

                                        }}
                                        .column-wrapper {{
                                            width: 100%;
                                            height: 20px;
                                            background: #CFD8DC;
                                            margin: 0 auto;
                                            overflow: hidden;
                                            position: relative;
                                        }}
                                        .column {{
                                            height: 20px;
                                            position: absolute;
                                            left: 0;
                                        }}
                                        .percentage {{
                                            margin-top: 10px;
                                            padding: 5px 10px;
                                            color: #FFF;
                                            background: #262730;
                                            position: relative;
                                            border-radius: 4px;
                                            text-align: center;
                                            font-family: sans-serif;
                                        }}
                                    </style>
                                    """

                # Renderizar o HTML no Streamlit
                st.components.v1.html(progress_metricaForaComercial, height=80)
            with col6:

                color_metricaFDS = determine_color2(metricaFDS)

                # HTML e CSS para a barra de progresso
                progress_metricaFDS = f"""
                                    <div class="outer-wrapper">
                                        <div class="column-wrapper">
                                            <div class="column" style="width: {metricaFDS}%; background: {color_metricaFDS};"></div>
                                        </div>
                                        <div class="percentage" style="font-size: 11px">Resp. FDS {metricaFDSSTR}%</div>
                                    </div>
                                    <style>
                                        .outer-wrappers {{
                                            display: inline-block;
                                            margin: 5px 15px;
                                            padding: 25px 15px;
                                            background: #eee;
                                            min-width: 300px;
                                            text-align: center;

                                        }}
                                        .column-wrapper {{
                                            width: 100%;
                                            height: 20px;
                                            background: #CFD8DC;
                                            margin: 0 auto;
                                            overflow: hidden;
                                            position: relative;
                                        }}
                                        .column {{
                                            height: 20px;
                                            position: absolute;
                                            left: 0;
                                        }}
                                        .percentage {{
                                            margin-top: 10px;
                                            padding: 5px 10px;
                                            color: #FFF;
                                            background: #262730;
                                            position: relative;
                                            border-radius: 4px;
                                            text-align: center;
                                            font-family: sans-serif;
                                        }}
                                    </style>
                                    """

                # Renderizar o HTML no Streamlit
                st.components.v1.html(progress_metricaFDS, height=80)
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
                    if filtered['id_Pedido'].count() == 0 or dfVisita['num_TotalVisita'].sum() :
                        cardConversaoVenda = 0
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

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if __name__ == '__main__':
    dashboard()

