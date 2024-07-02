import streamlit as st
import pandas as pd
from dataset import df, dfDetalhado, dfMetrica, dfMetricaTempoResp, dfVisita, dfPosVenda, dfPergunta, dfTop10, get_api_data
# from utils import locale
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh
from streamlit_card import card
import yaml
from yaml import SafeLoader
import streamlit_authenticator as stauth
import toml




def dashboard():
    # st.title('Página Inicial')
    # if st.session_state["authentication_status"]:
    #    col1, col2 = st.columns((6,1))
    #    with col1:
    #        st.write(f'Olá *{st.session_state["name"]}*!')
    #    with col2:
    #        teste = authenticator.logout('Logout', 'main')
    #        if teste:
    #            st.switch_page('pages/Login.py')
    aba1, aba2, aba3 = st.tabs(['Resumo', 'Detalhado','Estoque'])

    # marcas = st.multiselect(
    #    'Marcas'
    #    ,df['nom_Marca'].unique()
    #    ,df['nom_Marca'].unique()
    # )
    #
    # query = '''`nom_Marca` in @marcas'''
    #
    # filtered = df.query(query)

    filtered = df
    with aba1:
        st_autorefresh(interval=600000, limit=None, key="fizzbuzzcounter")
        st.markdown('''
                ## Resumo de Vendas Ecommerce
                Dados dos últimos 30 dias.
                ''')

        # st.title('Vendas Ecommerce')
        # st.subheader('Dados dos últimos 30 dias')

        # Cards
        col_Card1, col_Card2, col_Card3 = st.columns(3)
        with st.container():
            valorPedido = f"R$ {filtered['vlr_TotalPago'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X',
                                                                                                                   '.')
            valorPedidoDia = f"R$ {filtered[filtered['dat_Criacao'] == filtered['dat_Criacao'].max()]['vlr_TotalPago'].sum():,.2f}".replace(
                ',', 'X').replace('.', ',').replace('X', '.')
            valorTicketMedio = f"R$ {filtered[filtered['dat_Criacao'] > filtered['dat_Criacao'].max() - pd.Timedelta(days=30)]['vlr_TotalPago'].mean():,.2f}".replace(
                ',', 'X').replace('.', ',').replace('X', '.')

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
                st.dataframe(dfTop10.style.set_sticky(axis="index"), hide_index=True, )

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
                cardValorComissao = f"R$ {filtered['vlr_Comissao'].sum():,.2f}".replace(',', 'X').replace('.',
                                                                                                          ',').replace(
                    'X', '.')
                st.metric(label='Valor Comissão', value=cardValorComissao)
            with c2:
                cardValorImpostos = f"R$ {filtered['vlr_Impostos'].sum():,.2f}".replace(',', 'X').replace('.',
                                                                                                          ',').replace(
                    'X', '.')  # filtered['vlr_Comissao'].sum()
                st.metric(label='Valor Impostos', value=cardValorImpostos)
            with c3:
                cardPercentualaMargem = filtered['perc_MargemVenda'].mean()
                cardPercentualaMargem = '{:.2%}'.format(cardPercentualaMargem * 100)
                st.metric(label='% Margem', value=cardPercentualaMargem)
            with c4:
                cardValorFrete = f"R$ {filtered['vlr_FreteFinal'].sum():,.2f}".replace(',', 'X').replace('.',
                                                                                                         ',').replace(
                    'X', '.')
                st.metric(label='Valor Frete', value=cardValorFrete)
            with c5:
                cardQuantidadeDevolucao = '{:,}'.format(filtered['id_Mediacao'].nunique())
                st.metric(label='Qtd Devolução', value=cardQuantidadeDevolucao.replace(',', '.'))
            with c6:
                carValorDevolucao = f"R$ {filtered['vlr_Devolucao'].sum():,.2f}".replace(',', 'X').replace('.',
                                                                                                           ',').replace(
                    'X', '.')
                st.metric(label='Valor Devolução', value=carValorDevolucao)

            with st.container():
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    cardTotalVisita = '{:,}'.format(dfVisita['num_TotalVisita'].sum())
                    st.metric(label='Total Visitas', value=cardTotalVisita.replace(',', '.'))
                with c2:
                    cardConversaoVenda = '{:.2%}'.format(
                        filtered['id_Pedido'].count() / dfVisita['num_TotalVisita'].sum())
                    if filtered['id_Pedido'].count() == 0 or dfVisita['num_TotalVisita'].sum():
                        cardConversaoVenda = 0
                    st.metric(label='Conversão Vendas', value=cardConversaoVenda)
                with c3:
                    try:
                        cardPosVenda = '{:,}'.format(dfPosVenda['qtd_MSG'].sum())
                    except:
                        cardPosVenda = 0
                    st.metric(label='Msg Pós Vendas', value=cardPosVenda.replace(',', '.'))
                with c4:
                    cardAguardandoResp = f"{dfPergunta[dfPergunta['nom_Status'] == 'UNANSWERED']['id_Vendedor'].count():,}".replace(
                        ',', '.')
                    st.metric(label='Aguardando Resp.', value=cardAguardandoResp)

    with aba2:
        st.markdown('''
                                ## Detalhado de Vendas Ecommerce
                                ''')
        filtro1, filtro2, filtro3 = st.columns(3)
        with filtro1:
            with st.expander('Data de Venda'):
                data_venda = st.date_input(
                    'Selecione a Data'
                    , (dfDetalhado['Data'].min()
                       , dfDetalhado['Data'].max())
                )

        with filtro2:
            with st.expander('Pedido'):
                # pedido = st.container(height=300).multiselect(
                #    'Selecione o Número do Pedido'
                #    ,dfDetalhado['Pedido'].unique()
                #    ,dfDetalhado['Pedido'].unique()
                # )

                all_options = dfDetalhado['Pedido'].tolist()

                selected_all = st.container(height=200).multiselect(
                    'Selecione o Pedido'
                    , all_options
                    , all_options
                    , key="selected_all"
                    , placeholder='Selecione o Pedido'
                )

                def _select_all():
                    st.session_state.selected_all = all_options

                st.button("Todos Pedidos", on_click=_select_all)

                selected_all

        with filtro3:
            with st.expander('Tipo Venda'):
                tipovenda = st.multiselect(
                    'Selecione o Tipo de Venda'
                    , dfDetalhado['Tipo Venda'].unique()
                    , dfDetalhado['Tipo Venda'].unique()
                )

        query = '''
                    `Data` >= @data_venda[0] and `Data` <= @data_venda[1] \
                    and `Pedido` in @selected_all \
                    and `Tipo Venda` in @tipovenda \
                '''

        filtro_dados = dfDetalhado.query(query)

        st.dataframe(filtro_dados, hide_index=True)

        card1, card2, card3, card4, card5, card6 = st.columns(6)
        with card1:
            v_TotalPedido = '{:,}'.format(filtro_dados['Pedido'].nunique())
            st.metric(label='Total Pedidos', value=v_TotalPedido.replace(',', '.'))
        with card2:
            v_ValorPedido = f"R$ {filtro_dados['Venda'].sum():,.2f}"
            st.metric(label='Valor Pedidos', value=v_ValorPedido.replace(',', 'X').replace('.', ',').replace('X', '.'))
        with card3:
            v_TicketMedio = f"R$ {filtro_dados['Venda'].mean():,.2f}"
            st.metric(label='Tiket Médio', value=v_TicketMedio.replace(',', 'X').replace('.', ',').replace('X', '.'))
        with card4:
            v_ComissaoML = f"R$ {filtro_dados['Comissão'].sum():,.2f}"
            st.metric(label='Comissão ML', value=v_ComissaoML.replace(',', 'X').replace('.', ',').replace('X', '.'))
        with card5:
            v_Impostos = f"R$ {filtro_dados['Impostos'].sum():,.2f}"
            st.metric(label='Valor Impostos', value=v_Impostos.replace(',', 'X').replace('.', ',').replace('X', '.'))
        with card6:
            v_Frete = f"R$ {filtro_dados['Frete'].sum():,.2f}"
            st.metric(label='Valor Frete', value=v_Frete.replace(',', 'X').replace('.', ',').replace('X', '.'))


    with aba3:
        st.header('Estoque de Peças')
        dfEstoque = get_api_data()

        filtro1, filtro2, filtro3 = st.columns(3)
        filtro4, filtro5, filtro6 = st.columns(3)
        with filtro1:
            with st.expander('Status'):
                e_status = st.multiselect(
                    'Selecione o Status'
                    , dfEstoque['Status'].unique()
                    , dfEstoque['Status'].unique()
                    , key='e_status'
                )

        with filtro2:
            with st.expander('Matriz'):
                all_options_matriz = dfEstoque['Cod. Matriz'].tolist()

                e_matriz_selected_all = st.container(height=200).multiselect(
                    'Selecione a Matriz'
                    , all_options_matriz
                    , all_options_matriz
                    , key="e_matriz_selected_all"
                    , placeholder='Selecione a Matriz'
                )

                def _select_all_matriz():
                    st.session_state.matriz_selected_all = all_options_matriz

                st.button("Todas Matrizes", on_click=_select_all_matriz)

                e_matriz_selected_all

        with filtro3:
            with st.expander('Empresa'):
                all_options_empresa = dfEstoque['Cod. Empresa'].tolist()

                e_empresa_selected_all = st.container(height=200).multiselect(
                    'Selecione a Empresa'
                    , all_options_empresa
                    , all_options_empresa
                    , key="e_empresa_selected_all"
                    , placeholder='Selecione a Empresa'
                )

                def _select_all_empresa():
                    st.session_state.e_empresa_selected_all = all_options_empresa

                st.button("Todas Empresas", on_click=_select_all_empresa)

                e_empresa_selected_all

        with filtro4:
            with st.expander('Marca'):
                all_options_marca = dfEstoque['Fornecedor'].tolist()

                e_marca_selected_all = st.container(height=200).multiselect(
                    'Selecione a Marca'
                    , all_options_marca
                    , all_options_marca
                    , key="e_marca_selected_all"
                    , placeholder='Selecione a Marca'
                )

                def _select_all_marca():
                    st.session_state.e_marca_selected_all = all_options_marca

                st.button("Todas Marcas", on_click=_select_all_marca)

                e_marca_selected_all

        with filtro5:
            with st.expander('SKU'):
                all_options_sku = dfEstoque['SKU'].tolist()

                e_sku_selected_all = st.container(height=200).multiselect(
                    'Selecione o SKU'
                    , all_options_sku
                    , all_options_sku
                    , key="e_sku_selected_all"
                    , placeholder='Selecione o SKU'
                )

                def _select_all_sku():
                    st.session_state.e_sku_selected_all = all_options_sku

                st.button("Todos SKUs", on_click=_select_all_sku)

                e_sku_selected_all

        with filtro6:
            ""
        query = '''
            `Status` in @e_status  \
            and `SKU` in @e_sku_selected_all \
            and `Cod. Matriz` in @e_matriz_selected_all \
            and `Fornecedor` in @e_marca_selected_all \
            and `Cod. Empresa` in @e_empresa_selected_all \
            '''

        filtro_estoque = dfEstoque.query(query)

        st.dataframe(filtro_estoque, hide_index=True)
        st.markdown(f'''
                    🟢 {filtro_estoque[filtro_estoque['Status'] == '🟢']['Status'].count()} Items \n
                    🟡 {filtro_estoque[filtro_estoque['Status'] == '🟡']['Status'].count()} Items \n
                    🟠 {filtro_estoque[filtro_estoque['Status'] == '🟠']['Status'].count()} Items \n
                    🔴 {filtro_estoque[filtro_estoque['Status'] == '🔴']['Status'].count()} Items \n
                    ''')


    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#if __name__ == '__main__':
#    dashboard()

