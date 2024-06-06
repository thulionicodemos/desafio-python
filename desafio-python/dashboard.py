import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações gerais da página
st.set_page_config(
    page_title="Meu dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

# Estilização CSS 
# Crie o seu arquivo .css
with open('style.css', 'r') as fp:
    st.markdown(f"<style>{fp.read()}</style>", unsafe_allow_html=True)

# Carregamento de dados com Pandas
data = pd.read_csv('data_brazil.csv')

# Exibir os nomes das colunas para verificar
st.write("Nomes das colunas no DataFrame:", data.columns)

# Converter a coluna 'Date' para datetime, se existir
if 'Date' in data.columns:
    data['Date'] = pd.to_datetime(data['Date'])
else:
    st.write("A coluna 'Date' não foi encontrada. Verifique os nomes das colunas no CSV.")
    st.stop()

# Adicionar uma coluna para o ano
data['Year'] = data['Date'].dt.year

# Função para criar um gráfico de linhas
def plot1(data, x, y, color):
    fig = px.line(data, x=x, y=y, color=color,
                  title=f'Temperaturas Diárias em {data["Year"].iloc[0]}',
                  labels={y: 'Temperatura Média (°C)', x: 'Data'})
    return fig

# Função para criar um gráfico de barras
def plot2(data, x, y, color):
    fig = px.bar(data, x=x, y=y, color=color,
                 title='Temperatura Média Anual por Cidade',
                 labels={y: 'Temperatura Média (°C)', x: 'Cidade'})
    return fig

# Função para criar um gráfico de dispersão
def plot3(data, x, y, color):
    fig = px.scatter(data, x=x, y=y, color=color,
                     title='Distribuição de Temperaturas ao Longo do Ano',
                     labels={y: 'Temperatura Média (°C)', x: 'Data'})
    return fig

# Configurar o título e a descrição do aplicativo
st.title('Dashboard de Temperatura Diária')
st.markdown("""
    Este dashboard permite visualizar as temperaturas diárias registradas em várias cidades.
    Use a barra lateral para selecionar o ano que deseja visualizar.
""")

# Configurar a barra lateral para selecionar o ano
anos = data['Year'].unique()
ano_selecionado = st.sidebar.selectbox('Selecione o Ano', anos)

# Filtrar os dados pelo ano selecionado
dados_ano_selecionado = data[data['Year'] == ano_selecionado]

# Criar e exibir os gráficos
fig_line = plot1(dados_ano_selecionado, x='Date', y='AvgTemperature', color='City')
fig_bar = plot2(dados_ano_selecionado.groupby('City').mean().reset_index(), x='City', y='AvgTemperature', color='City')
fig_scatter = plot3(dados_ano_selecionado, x='Date', y='AvgTemperature', color='City')

# Exibir os gráficos no Streamlit
st.plotly_chart(fig_line)
st.plotly_chart(fig_bar)
st.plotly_chart(fig_scatter)

# Adicionar uma tabela com os dados filtrados
st.dataframe(dados_ano_selecionado[['Date', 'City', 'AvgTemperature']])