
import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados
df = pd.read_excel("controle OAE - atualizado.xlsx")

# Filtros
st.title("Dashboard de Inspeção de OAEs")
st.sidebar.header("Filtros")

rodovia = st.sidebar.multiselect("Rodovia", df["RODOVIA"].dropna().unique())
km = st.sidebar.multiselect("KM + M", df["KM + M"].dropna().unique())
sentido = st.sidebar.multiselect("Sentido", df["SENTIDO"].dropna().unique())
coluna_nota = st.sidebar.selectbox("Tipo de Nota", ["Estrutural", "Funcional", "Durabilidade", "Nota Geral"])
notas_disponiveis = sorted([n for n in df[coluna_nota].dropna().unique() if isinstance(n, str)])
nota_filtro = st.sidebar.multiselect("Filtrar por Nota", notas_disponiveis)

# Aplicar filtros
df_filtrado = df.copy()
if rodovia:
    df_filtrado = df_filtrado[df_filtrado["RODOVIA"].isin(rodovia)]
if km:
    df_filtrado = df_filtrado[df_filtrado["KM + M"].isin(km)]
if sentido:
    df_filtrado = df_filtrado[df_filtrado["SENTIDO"].isin(sentido)]
if nota_filtro:
    df_filtrado = df_filtrado[df_filtrado[coluna_nota].isin(nota_filtro)]

# Gráfico de pizza
st.subheader(f"Distribuição das notas ({coluna_nota})")
if not df_filtrado.empty:
    fig = px.pie(df_filtrado, names=coluna_nota, title=f"Distribuição de {coluna_nota}", hole=0.4)
    st.plotly_chart(fig)
else:
    st.warning("Nenhum dado disponível para os filtros selecionados.")

# Tabela com os dados
st.subheader("Tabela de OAEs")
st.dataframe(df_filtrado)
