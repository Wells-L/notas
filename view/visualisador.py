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

st.title("visualizar notas")

df = conn.read(worksheet='Notas')

lista_de_materia = df["matéria"].unique()

materia_selecionada = st.selectbox(
    "escolha sua materia",lista_de_materia
)

st.markdown("# notas em geral")

dados_dumb = {"avaliação":["AT1","AT2","APA","AT1","AT2","APA","AT1","AT2","APA"],
              "trimestre":[1,1,1,2,2,2,3,3,3],
              "nota":[pd.NA,pd.NA,pd.NA,pd.NA,pd.NA,pd.NA,pd.NA,pd.NA,pd.NA]}

df_dumb = pd.DataFrame(dados_dumb)

df_filtrado = df.loc[df["matéria"]== materia_selecionada,["avaliação","trimestre","nota"]]

df_final = pd.concat([df_dumb,df_filtrado])
df_final = df_final.drop_duplicates(subset=["avaliação","trimestre"],keep="last")

df_pivot = df_final.pivot(index="avaliação",columns="trimestre",values="nota")
df_pivot.columns = ["trimestre 1","trimestre 2","trimestre 3"]

st.dataframe(df_pivot)

df_final["prova falta"] = df_final["nota"].isna()

groupby_trimestre_falta = df_final.groupby('trimestre').agg({'nota':"sum",'prova falta': 'sum'}).reset_index()
groupby_trimestre_falta["quanto falta trimestre"] = (18-groupby_trimestre_falta["nota"])/groupby_trimestre_falta["prova falta"]
groupby_trimestre_falta["media trimestre"] = groupby_trimestre_falta["nota"]/3


trimestre_falta = groupby_trimestre_falta[["quanto falta trimestre","media trimestre"]].transpose()
trimestre_falta.columns = ["trimestre 1","trimestre 2","trimestre 3"]
st.dataframe(trimestre_falta)

media_do_ano = df_final["nota"].sum()/9
media_do_ano_str = f'{media_do_ano:.2f}'
if media_do_ano >= 6:
    situacao = "aprovado"

else:
    situacao = "-reprovado"
st.metric(label="Media do ano", value=media_do_ano_str, delta=situacao)
 