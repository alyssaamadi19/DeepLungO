import streamlit as st
import cv2
import base64


st.set_page_config(layout='wide', initial_sidebar_state='expanded', page_title = "DeepLungOp",)


@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
img = get_img_as_base64("doctor.png")

page_bg_img = """
<style>
[data-testid = "stAppViewContainer"]{{
background-image: url("data:image/png;base64,{img}");
background-size: cover;
}}

[data-testid="stSidebar"] > div:first-child{{
background-image: url("data:image/png;base64,{img}");
background-position: center;
}}
</style>
"""




st.markdown(page_bg_img, unsafe_allow_html = True)

st.title("Deep Learning Opacity Web Service")
st.sidebar.success("Select a page above.")

st.markdown("""
    ## ¿Qué es DLO?
    Somos una plataforma Web que predice la probabiliad de Opacidad Pulmonar en una Radiografía de Pecho, apoyando al diagnóstico de los médicos radiólogos
""")


#Colummns
col1, col2, col3 = st.columns(3)
with col1: 
    st.subheader(" ")
with col2: 
    st.subheader(" Objetivos ")

with col3: 
    st.subheader(" ")


col1, col2, col3 = st.columns(3)
with col1: 
    st.subheader(" 1.")
    st.markdown("Reconocer la opacidad en imágenes de radiografía pulmonar a través de algoritmos de inteligencia artificial.")
with col2: 
    st.subheader(" 2.")
    st.markdown("- Implementar una plataforma web enlazada a una base de datos para la visualización de resultados.")

with col3: 
    st.subheader(" 3. ")
    st.markdown("- Conectar el sistema del centro de salud a la plataforma web desarrollada.")


st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    list-style-position: inside;
}
</style>
''', unsafe_allow_html=True)



