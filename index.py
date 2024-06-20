import streamlit as st
import toml

st.set_page_config(page_title='Bem-Vindo', page_icon='☀', layout="centered", initial_sidebar_state="collapsed", menu_items=None)

with open('config.toml') as thm:
    theme = toml.load(thm)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""<div markdown="1" style='text-align: center;'>

## Bem-Vindo ao Portal de Dashboards

Seja bem-vindo ao nosso portal de dashboards, onde você terá acesso a informações e análises detalhadas para tomar decisões estratégicas de forma rápida e eficiente.

## O que você encontrará aqui:

**Dashboards Interativos:** Explore nossos dashboards interativos que oferecem insights em tempo real sobre os principais indicadores de negócio.

**Visualizações Personalizadas:** Personalize suas visualizações de dados de acordo com suas necessidades específicas usando filtros e opções de personalização avançadas.

**Análises Profundas:** Aprofunde-se nos dados com análises detalhadas, gráficos intuitivos e relatórios personalizados que ajudam na compreensão do desempenho da sua empresa.

## Como usar:

**Explorar Dashboards:** Clique nos diferentes painéis de dashboards para visualizar métricas importantes de vendas, marketing, financeiro e mais.

**Filtros Avançados:** Utilize os filtros na lateral para segmentar os dados por período, região, produto, entre outros critérios, e obtenha análises mais precisas.

**Exportar Dados:** Exporte os dados e gráficos para formatos como PDF ou Excel para compartilhar com colegas e stakeholders.

## Comece agora:

Não perca tempo e comece a explorar as possibilidades que nosso portal de dashboards oferece para impulsionar o crescimento e a eficiência da sua empresa.

Estamos aqui para ajudá-lo a transformar dados em decisões inteligentes. Aproveite sua jornada de análise de dados!

</div>""", unsafe_allow_html=True)


st.markdown(
    """
<style>
button {
    height: auto;
    padding-top: 10px !important;
    padding-bottom: 10px !important;
    width: 100px;q
    align: center;
}
</style>
""",
    unsafe_allow_html=True,
)

col1,col2,col3 = st.columns((3,1,3))
with col1:
    pass
with col2:
    center_button = st.page_link('./pages/Login.py',label='Fazer Login!')
with col3:
    pass
