import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar a estilização do Streamlit
st.set_page_config(page_title='Dashboard COVID-19 Brasil', layout='wide')
st.markdown('<link rel="stylesheet" href="style.css">', unsafe_allow_html=True)

# Título do dashboard
st.title('Dashboard COVID-19 Brasil')

# Carregar os dados
df = pd.read_csv('covid_19_data_brazil.csv')

# Processar dados
df['ObservationDate'] = pd.to_datetime(df['ObservationDate'], format='%m/%d/%Y')
df = df.sort_values('ObservationDate')

# Calcular novos casos e novos óbitos por dia
df['New Cases'] = df.groupby('Province/State')['Confirmed'].diff().fillna(0)
df['New Deaths'] = df.groupby('Province/State')['Deaths'].diff().fillna(0)

# Filtros
st.sidebar.header('Filtros')
state = df['Province/State'].unique().tolist()
state.insert(0, 'Todos')
selected_state = st.sidebar.selectbox('Selecione o Estado', state)

# Filtro de data
start_date = st.sidebar.date_input('Data de Início', df['ObservationDate'].min())
end_date = st.sidebar.date_input('Data Final', df['ObservationDate'].max())

# Aplicar filtros
filtered_df = df
if selected_state != 'Todos':
    filtered_df = filtered_df[filtered_df['Province/State'] == selected_state]
filtered_df = filtered_df[(filtered_df['ObservationDate'] >= pd.to_datetime(start_date)) & (filtered_df['ObservationDate'] <= pd.to_datetime(end_date))]

# Gráfico de casos acumulados
fig_cases = px.line(filtered_df, x='ObservationDate', y='Confirmed', title='Casos Acumulados')
fig_cases.update_xaxes(title='Data')
fig_cases.update_yaxes(title='Casos Acumulados')
st.plotly_chart(fig_cases, use_container_width=True)

# Gráfico de óbitos acumulados
fig_deaths = px.line(filtered_df, x='ObservationDate', y='Deaths', title='Óbitos Acumulados')
fig_deaths.update_xaxes(title='Data')
fig_deaths.update_yaxes(title='Óbitos Acumulados')
st.plotly_chart(fig_deaths, use_container_width=True)

# Gráfico de novos casos por dia
fig_new_cases = px.bar(filtered_df, x='ObservationDate', y='New Cases', title='Novos Casos por Dia')
fig_new_cases.update_xaxes(title='Data')
fig_new_cases.update_yaxes(title='Novos Casos')
st.plotly_chart(fig_new_cases, use_container_width=True)

# Gráfico de novos óbitos por dia
fig_new_deaths = px.bar(filtered_df, x='ObservationDate', y='New Deaths', title='Novos Óbitos por Dia')
fig_new_deaths.update_xaxes(title='Data')
fig_new_deaths.update_yaxes(title='Novos Óbitos')
st.plotly_chart(fig_new_deaths, use_container_width=True)

# Gráfico de recuperações acumuladas
fig_recovered = px.line(filtered_df, x='ObservationDate', y='Recovered', title='Recuperações Acumuladas')
fig_recovered.update_xaxes(title='Data')
fig_recovered.update_yaxes(title='Recuperações Acumuladas')
st.plotly_chart(fig_recovered, use_container_width=True)

# Mapa interativo de casos confirmados no Brasil
brazil_states = {
    'Acre': 'AC', 'Alagoas': 'AL', 'Amapa': 'AP', 'Amazonas': 'AM', 'Bahia': 'BA', 'Ceara': 'CE', 'Distrito Federal': 'DF', 
    'Espirito Santo': 'ES', 'Goias': 'GO', 'Maranhao': 'MA', 'Mato Grosso': 'MT', 'Mato Grosso do Sul': 'MS', 'Minas Gerais': 'MG', 
    'Para': 'PA', 'Paraiba': 'PB', 'Parana': 'PR', 'Pernambuco': 'PE', 'Piaui': 'PI', 'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN', 
    'Rio Grande do Sul': 'RS', 'Rondonia': 'RO', 'Roraima': 'RR', 'Santa Catarina': 'SC', 'Sao Paulo': 'SP', 'Sergipe': 'SE', 'Tocantins': 'TO'
}

# Adicionar coluna de códigos dos estados
df['State Code'] = df['UF'].map(brazil_states)
if df['State Code'].isnull().any():
    st.error("Erro: Alguns estados não foram mapeados corretamente. Verifique os nomes dos estados no CSV.")
    st.stop()

# Filtrar os dados para a data mais recente
latest_date = filtered_df['ObservationDate'].max()
latest_data = df[df['ObservationDate'] == latest_date]

# Verificar se há dados para a data mais recente
if latest_data.empty:
    st.warning("Não há dados disponíveis para a data selecionada.")
else:
    fig_map = px.choropleth(
        latest_data,
        locations="State Code",
        geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
        color="Confirmed",
        hover_name="UF",
        hover_data={"State Code": False, "Confirmed": True},
        title='Casos Confirmados por Estado no Brasil',
        projection="mercator"
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map, use_container_width=True)
