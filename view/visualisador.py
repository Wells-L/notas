from streamlit_gsheets import GSheetsConnection
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import gspread
import json
from datetime import datetime
#from google.oauth2.service_account import Credentials

conn = st.connection("gsheets", type=GSheetsConnection)

st.title("visualisar notas")

df = conn.read(worksheet='Notas')

lista_de_materia = df["matéria"].unique()

materia_selecionada = st.selectbox(
    "escolha sua materia",lista_de_materia
)
df_filtrado = df.loc[df["matéria"]== materia_selecionada]
df_pivot = df_filtrado.pivot(index="avaliação",columns="trimestre",values="nota")
st.dataframe(df_pivot)


