
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_excel("Controle de Inspeção Especial - OAEs Ecopistas - Rev03.xlsx")
df.columns = df.columns.str.strip()
df["Ano Intervenção"] = pd.to_datetime(df["Proxima Intervenção"], errors='coerce').dt.year

# Robustez na identificação de colunas
def buscar_coluna(parte_nome):
    for col in df.columns:
        if parte_nome.lower() in col.lower():
            return col
    return None

st.title("Dashboard de Inspeção de OAEs")
st.sidebar.header("Filtros")

rodovia = st.sidebar.multiselect("Rodovia", df.get("RODOVIA", pd.Series()).dropna().unique())
km = st.sidebar.multiselect("KM + M", df.get("KM + M", pd.Series()).dropna().unique())
sentido = st.sidebar.multiselect("Sentido", df.get("SENTIDO", pd.Series()).dropna().unique())
coluna_nota = st.sidebar.selectbox("Tipo de Nota", ["Estrutural", "Funcional", "Durabilidade", "Nota Geral"])

# Filtros por data
ano_ult_col = buscar_coluna("Última Inspeção Especial")
ano_prox_col = buscar_coluna("Próxima Inspeção Especial")

if ano_ult_col:
    anos_ult_ie = sorted(pd.to_datetime(df[ano_ult_col], errors='coerce').dt.year.dropna().unique())
    ano_ult_ie = st.sidebar.multiselect("Última Inspeção Especial (Ano)", anos_ult_ie)
else:
    ano_ult_ie = []

if ano_prox_col:
    anos_prox_ie = sorted(pd.to_datetime(df[ano_prox_col], errors='coerce').dt.year.dropna().unique())
    ano_prox_ie = st.sidebar.multiselect("Próxima Inspeção Especial (Ano)", anos_prox_ie)
else:
    ano_prox_ie = []

anos_intervencao = sorted(df["Ano Intervenção"].dropna().unique())
ano_intervencao = st.sidebar.multiselect("Ano da Próxima Intervenção", anos_intervencao)

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
if ano_ult_ie and ano_ult_col:
    df_filtrado = df_filtrado[pd.to_datetime(df_filtrado[ano_ult_col], errors='coerce').dt.year.isin(ano_ult_ie)]
if ano_prox_ie and ano_prox_col:
    df_filtrado = df_filtrado[pd.to_datetime(df_filtrado[ano_prox_col], errors='coerce').dt.year.isin(ano_prox_ie)]
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
