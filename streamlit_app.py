import streamlit as st

# --- PAGE SETUP ---
formulario_page = st.Page(
    "view/formulario.py",
    title="Formulario",
    icon=":material/cloud_upload:",
    default=True,
)

pg = st.navigation(
    {
        "formulario": [formulario_page]
    }
)

pg.run()