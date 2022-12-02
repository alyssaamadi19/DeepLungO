import streamlit as st
import cv2
import base64

@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
img = get_img_as_base64("doctor.png")

page_bg_img = f"""
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



st.set_page_config(
    page_title = "Multipage App",
)


st.markdown(page_bg_img, unsafe_allow_html = True)

st.title('Deep Learning Opacity Web Service')
st.sidebar.success("Select a page above.")

st.markdown("""
    ## ¿Qué es DLO?
    Somos una plataforma Web que predice la probabiliad de Opacidad Pulmonar en una Radiografía de Pecho, apoyando al diagnóstico de los médicos radiólogos
""")


#st.image(imread('./imgs/cadex.jpg'), channels = 'RGB')
