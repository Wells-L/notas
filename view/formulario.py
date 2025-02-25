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

st.title("Formulario de notas")

with st.form("notas_form"):
    

    col1,col2 = st.columns(2)

    with col1 :
        avaliacao = st.selectbox(
            "escolha sua avaliacao",["AT1","AT2","APA"]
        )
        st.write(f"voce selecionou: {avaliacao}")

        trimestre = st.selectbox(
            "escolha seu trimestre",["1","2","3"]
        )
        st.write(f"voce selecionou o trimestre: {trimestre}")

    with col2 :

        materia = st.selectbox(
            "escolha sua materia",["Matematica","Portugues","ciencias"]
        )
        st.write(f"voce selecionou: {materia}")

        nota = st.number_input("Sua nota:", step = 0.1, value=6.0)



    if nota < 6:
        st.write("voce foi muito mal, tem que melhorar")



    submitted = st.form_submit_button("Submit")

if submitted :

    if 'notas_db' not in st.session_state:

 
        df = conn.read(worksheet='Notas')
        st.session_state["notas_db"] = df
    else:
        df = st.session_state["notas_db"]
   
    now = datetime.now()

    
    novos_dados = pd.DataFrame({'matéria':[materia], 'avaliação':[avaliacao], 'nota':[nota], 'trimestre':[trimestre], 'última atualização':[now]})


    resultado = pd.concat([df, novos_dados], ignore_index=True)
    resultado = resultado.drop_duplicates(subset=["matéria","avaliação","trimestre"],keep="last")
    
  
    df = conn.update(data=resultado,worksheet='Notas')
    st.session_state["notas_db"] = df
    st.success("dados foram atualizados com sucesso")
    

#https://github.com/streamlit/gsheets-connection/blob/main/examples/pages/Service_Account_Example.py
#licao: arrumar streamlit e colocar dados no banco
