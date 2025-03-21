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

dados_dumb = {"avaliação":["AT1","AT2","APA","AT1","AT2","APA","AT1","AT2","APA"],
              "trimestre":[1,1,1,2,2,2,3,3,3],
              "nota":[pd.NA,pd.NA,pd.NA,pd.NA,pd.NA,pd.NA,pd.NA,pd.NA,pd.NA]}

df_dumb = pd.DataFrame(dados_dumb)

df_filtrado = df.loc[df["matéria"]== materia_selecionada,["avaliação","trimestre","nota"]]

df_final = pd.concat([df_dumb,df_filtrado])
df_final = df_final.drop_duplicates(subset=["avaliação","trimestre"],keep="last")

df_pivot = df_final.pivot(index="avaliação",columns="trimestre",values="nota")

st.dataframe(df_pivot)

df_final["prova falta"] = df_final["nota"].isna()

groupby_trimestre = df_final.fillna(0).groupby("trimestre")["nota"].mean()

groupby_trimestre_falta = df_final.groupby('trimestre').agg({'nota':"sum",'prova falta': 'sum'}).reset_index()
groupby_trimestre_falta["quanto falta trimestre"] = (18-groupby_trimestre_falta["nota"])/groupby_trimestre_falta["prova falta"]
st.dataframe(groupby_trimestre_falta)

st.dataframe(groupby_trimestre)

