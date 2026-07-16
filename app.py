import streamlit as st
import plotly.express as px
from src.processamento import processar_base_precificacao, salvar_processado

# Configuração da página
st.set_page_config(layout="wide", page_title="Dashboard Precificação")

st.title(" Dashboard de Inteligência de Mercado")
st.markdown("---")

# Carregamento dos dados com cache para performance
@st.cache_data
def carregar_dados_dashboard():
    return processar_base_precificacao(
        'data/raw/COTAÇÕES - CASE.xlsx', 
        'data/raw/SalesForce - CASE.xlsx'
    )

try:
    df = carregar_dados_dashboard()
    salvar_processado(df)
    

    # Layout do Dashboard
    col1, col2 = st.columns(2)

    # Top 10 Clientes (Descontos)
    with col1:
        st.subheader("Top 10 Clientes: Maior Concessão de Desconto")
        top_10 = df.groupby('Código_do_Cliente')['Var_Preço_Proposto'].sum().nlargest(10).reset_index()
        fig1 = px.bar(
            top_10, 
            x='Var_Preço_Proposto', 
            y='Código_do_Cliente', 
            orientation='h',
            text_auto='.2s',
            color_discrete_sequence=['#1f77b4']
        )
        fig1.update_layout(template="plotly_white", xaxis_title="Desconto Total (R$)", yaxis_title="ID do Cliente")
        st.plotly_chart(fig1, width='stretch')

    #  Top 10 por Região e Gestão
    with col2:
        st.subheader("Volume de Descontos por Região e Gestão")
        df_regiao = df.groupby(['Região', 'Gestão_de_Vendas'])['Var_Preço_Proposto'].sum().nlargest(10).reset_index()
        fig2 = px.bar(
            df_regiao, 
            x='Região', 
            y='Var_Preço_Proposto', 
            color='Gestão_de_Vendas',
            barmode='group',
            template="plotly_white"
        )
        st.plotly_chart(fig2, width='stretch')

    #  Análise de Fretes
    st.markdown("---")
    st.subheader("Análise de Fretes Zerados (CIF)")
    df_frete = df[(df['Frete_Comercial'] == 0) & (df['Incoterm'] == 'CIF')]
    
    if not df_frete.empty:
        fig3 = px.pie(
            df_frete, 
            names='Cód_Expedição', 
            hole=0.4, 
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig3.update_traces(textinfo='percent+label')
        st.plotly_chart(fig3, width='stretch')
    else:
        st.info("Nenhum registro de frete CIF com valor zerado encontrado.")

except Exception as e:
    st.error(f"Erro ao carregar o dashboard: {e}")
    st.write("Verifique se os arquivos de dados estão na pasta `data/raw/` com os nomes corretos.")