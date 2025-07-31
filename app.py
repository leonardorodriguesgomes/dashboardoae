
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_excel("Controle de Inspeção Especial - OAEs Ecopistas - Rev03.xlsx")
df.columns = df.columns.str.strip()
df["Ano Intervenção"] = pd.to_datetime(df["Proxima Intervenção"], errors='coerce').dt.year

st.title("Dashboard de Inspeção de OAEs")
st.sidebar.header("Filtros")

rodovia = st.sidebar.multiselect("Rodovia", df["RODOVIA"].dropna().unique())
km = st.sidebar.multiselect("KM + M", df["KM + M"].dropna().unique())
sentido = st.sidebar.multiselect("Sentido", df["SENTIDO"].dropna().unique())
coluna_nota = st.sidebar.selectbox("Tipo de Nota", ["Estrutural", "Funcional", "Durabilidade", "Nota Geral"])

try:
    anos_ult_ie = sorted(df["Ultima Inspeção Especial"].dropna().unique())
    ano_ult_ie = st.sidebar.multiselect("Última Inspeção Especial (Ano)", anos_ult_ie)
except KeyError:
    ano_ult_ie = []

try:
    anos_prox_ie = sorted(df["Proxima Inspeção Especial"].dropna().unique())
    ano_prox_ie = st.sidebar.multiselect("Próxima Inspeção Especial (Ano)", anos_prox_ie)
except KeyError:
    ano_prox_ie = []

try:
    anos_intervencao = sorted(df["Ano Intervenção"].dropna().unique())
    ano_intervencao = st.sidebar.multiselect("Ano da Próxima Intervenção", anos_intervencao)
except KeyError:
    ano_intervencao = []

notas_disponiveis = sorted([n for n in df[coluna_nota].dropna().unique() if isinstance(n, str)])
nota_filtro = st.sidebar.multiselect("Filtrar por Nota", notas_disponiveis)

df_filtrado = df.copy()
if rodovia:
    df_filtrado = df_filtrado[df_filtrado["RODOVIA"].isin(rodovia)]
if km:
    df_filtrado = df_filtrado[df_filtrado["KM + M"].isin(km)]
if sentido:
    df_filtrado = df_filtrado[df_filtrado["SENTIDO"].isin(sentido)]
if nota_filtro:
    df_filtrado = df_filtrado[df_filtrado[coluna_nota].isin(nota_filtro)]
if ano_ult_ie:
    df_filtrado = df_filtrado[df_filtrado["Ultima Inspeção Especial"].isin(ano_ult_ie)]
if ano_prox_ie:
    df_filtrado = df_filtrado[df_filtrado["Proxima Inspeção Especial"].isin(ano_prox_ie)]
if ano_intervencao:
    df_filtrado = df_filtrado[df_filtrado["Ano Intervenção"].isin(ano_intervencao)]

st.subheader(f"Distribuição das notas ({coluna_nota})")
if not df_filtrado.empty:
    fig = px.pie(df_filtrado, names=coluna_nota, title=f"Distribuição de {coluna_nota}", hole=0.4)
    st.plotly_chart(fig)
else:
    st.warning("Nenhum dado disponível para os filtros selecionados.")

st.subheader("Tabela de OAEs")
st.dataframe(df_filtrado)
