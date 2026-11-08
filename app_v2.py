import streamlit as st
import os

from components.navbar import show_navbar
from components.hero import show_hero

st.set_page_config(
    page_title="Emotion Detection AI",
    page_icon="🧠",
    layout="wide"
)
st.write(os.getcwd())
with open("styles/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

show_navbar()

#show_hero()
st.markdown(
    """
    <h1 style='color:red;'>Hello World</h1>
    """,
    unsafe_allow_html=True
)