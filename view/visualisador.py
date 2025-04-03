from streamlit_gsheets import GSheetsConnection
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import gspread
import json
from datetime import datetime
#from google.oauth2.service_account import Credentials


# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
# define um titulo
st.title("visualizar notas")
# Le os dados da planilha do Google Sheets na aba Nota
df = conn.read(worksheet='Notas')
# deixa as matérias únicas
lista_de_materia = df["matéria"].unique()
# Cria um selectbox para escolher a matéria
materia_selecionada = st.selectbox(
    "escolha sua materia",lista_de_materia
)
# adiciona um titulo para o dataframe
st.markdown("### notas em geral")
# Cria um DataFrame modelo para que todas as avaliações apareçam
# Caso não tenha dados na planilha, este modelo evita erros
# hardestcode
dados_dumb = {"avaliação":["AT1","AT2","APA","AT1","AT2","APA","AT1","AT2","APA"],
                "trimestre":[1,1,1,2,2,2,3,3,3],
                "nota":[pd.NA,pd.NA,pd.NA,pd.NA,pd.NA,pd.NA,pd.NA,pd.NA,pd.NA]}

df_dumb = pd.DataFrame(dados_dumb)

# Filtra os dados da matéria escolhida
df_filtrado = df.loc[df["matéria"]== materia_selecionada,["avaliação","trimestre","nota"]]
# Combina os dados da planilha com o DataFrame modelo e remove duplicatas
df_final = pd.concat([df_dumb,df_filtrado])
df_final = df_final.drop_duplicates(subset=["avaliação","trimestre"],keep="last")
# converte para uma tabela pivot para melorar a visualização
df_pivot = df_final.pivot(index="avaliação",columns="trimestre",values="nota")
df_pivot.columns = ["trimestre 1","trimestre 2","trimestre 3"]

# printa o dataframe notas em geral
st.dataframe(df_pivot)
st.write("d")
# identifica as provas que faltam
df_final["prova falta"] = df_final["nota"].isna()
# calcula os dados necessarios
groupby_trimestre_falta = df_final.groupby('trimestre').agg({'nota':"sum",'prova falta': 'sum'}).reset_index()
groupby_trimestre_falta["nota"] = groupby_trimestre_falta["nota"].fillna(0)
groupby_trimestre_falta["quanto falta trimestre"] = (18-groupby_trimestre_falta["nota"])/groupby_trimestre_falta["prova falta"]
groupby_trimestre_falta["media trimestre"] = groupby_trimestre_falta["nota"]/3 
groupby_trimestre_falta["media trimestre"] =  groupby_trimestre_falta["media trimestre"].round(1)
    
# calcula quanto falta para chegar em 6
#groupby_trimestre_falta["quanto falta por prova"] = (54-groupby_trimestre_falta.agg({'nota':"sum",'prova falta': 'sum'}).reset_index())
# deixa a tabela com uma melhor visualisacao 
trimestre_falta = groupby_trimestre_falta[["quanto falta trimestre","media trimestre"]].transpose()
trimestre_falta.columns = ["trimestre 1","trimestre 2","trimestre 3"]
# adiciona um subtitulo
st.markdown("### informações do trimestre")
#mostra a tabela com as informacoes do trimestre
st.dataframe(trimestre_falta)
#dividi em 3 colunas para melhor visualicasao 
col1,col2,col3, = st.columns(3)

with col3 :
# calcula a media do ano
    media_do_ano = df_final["nota"].sum()/9
    media_do_ano_str = f'{media_do_ano:.2f}'
        # mostra a situacao
    if media_do_ano >= 6:
            situacao = "aprovado"

    else:
        situacao = "-reprovado"
        #exibe a st.metric com informacoes 
        st.metric(label=f"Media anual {materia_selecionada}", value=media_do_ano_str, delta=situacao, border=True)

#resolver quanto falta em cada prova 
