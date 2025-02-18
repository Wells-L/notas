import streamlit as st

# --- PAGE SETUP ---
formulario_page = st.Page(
    "view/formulario.py",
    title="Formulario",
    icon=":material/cloud_upload:",
    default=True,
)

visualisador_page = st.Page(
    "view/visualisador.py",
    title="Visualizador de notas",
    icon=":material/cloud_upload:",
)

pg = st.navigation(
    {
        "formulario": [formulario_page],
        "visualizador":[visualisador_page],
    }
)



pg.run()