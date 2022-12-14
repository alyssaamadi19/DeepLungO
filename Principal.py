import streamlit as st
import cv2
import base64


st.set_page_config(layout='wide', initial_sidebar_state='expanded', page_title = "DeepLungOp",)



st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#2e7bcf);
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)




st.title("Deep Learning Opacity Web Service")
st.sidebar.success("Select a page above.")

st.markdown("""
    ## ¿Qué es DLO?
    Somos una plataforma Web que predice la probabiliad de Opacidad Pulmonar en una Radiografía de Pecho, apoyando al diagnóstico de los médicos radiólogos
""")
st.markdown("")
st.markdown("")

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
    st.markdown("Implementar una plataforma web enlazada a una base de datos para la visualización de resultados.")

with col3: 
    st.subheader(" 3. ")
    st.markdown("Conectar el sistema del centro de salud a la plataforma web desarrollada.")


st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    list-style-position: inside;
}
</style>
''', unsafe_allow_html=True)

st.markdown("")

#Colummns
col1, col2, col3 = st.columns(3)
with col1: 
    st.subheader(" ")
with col2: 
    st.subheader(" Sobre nosotros ")
with col3: 
    st.subheader(" ")
    
st.markdown("Somos alumnos de Ingeniería Biomédica de la Universidad Peruana Cayetano Heredia y la Pontifica Universidad Católica del Perú, interesados en la rama de Señales e Imágenes Médicas.")



#Colummns
col1, col2, col3 = st.columns(3)
with col1: 
    st.image("pierol.jpeg")
    st.subheader("Pierol Salvador Quispe Sánchez")
    st.markdown("Estudiante de Ing Biomedica de de 9no ciclo apasionado por la investigación y desarrollo de nuevas tecnologías que mejores la salud. Tengo interés particular por el área del el Diagnóstico de Imágenes o señales por IA, Ing. Clínica e Ingeniería de Tejidos.")
with col2: 
    st.image("victor.jpeg")
    st.subheader("Victor Giancarlo Sosa Rocha")
    st.markdown("Apasionado en las ramas de Ing. Clínica y Señales e Imágenes. Experiencia en desarrollo de un wearable prototipo para obtención de señales multiparamétricas e interés en procesamiento de señales de voz para personas que sufrieron laringectomía.")
with col3: 
    st.image("alyssa.jfif")
    st.subheader("Alyssa Nicole Maguiña Díaz")
    st.markdown("Estudia de Ingeniería Biomédica integrante de Laboratorio de Biomecánica y Robótica Aplicada con interés en la neurociencia relacionada con el aprendizaje motriz y procesamiento de señales de EEG e imágenes motoras para BCI. ")
    
col1, col2 = st.columns(2)
with col1: 
    st.image("david.png")
    st.subheader("David Villaseca Pacheco")
    st.markdown("Estudiante de ingeniería biomédica con enfoque al área de señales e imágenes e ingeniería clínica. Experiencia en la detección de patologías usando métodos de deep learning y machine learning.")
with col2: 
    st.image("ximena.jpeg")
    st.subheader("Ximena Jamilet Montoya Calderón")
    st.markdown("Estudiante de 8vo ciclo de la carrera de Ing. Biomédica, integrante del Laboratorio de Imágenes Médicas de la PUCP con interés en desarrollarse en el área de Imágenes y Señales Biomédicas. Experiencia trabajando con ultrasonido pulmonar.")

    
    
    
    
