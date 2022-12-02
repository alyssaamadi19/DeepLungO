import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import time

# Funciones en archivos .py fuera del folder de pages. Tendras que cambiarlo para tu compu
import sys
sys.path.insert(1, 'C:/Users/Usuario/Desktop/PROYECTO_ACSI/PROY_INTEGRADO/Streamlit') 
import CAD_DLOv1 as cad
import database as D

import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('login2.png')    



st.markdown("""
    # 👥 Ingrese sus credenciales
""")

us = st.text_input("Usuario")
pw = st.text_input("Contraseña",type="password")


if st.button("Ingresar"):
    if us is not '':
        if pw is not '':
            pw_real, name, doc, id = D.get_pw(us)
            if pw_real is not -1:
                if pw == pw_real:
                    msj = 'Bienvenido Doctor ' + name
                    st.success(msj)
                    time.sleep(2)
                    
                    if doc == 'RADIOLOGO':
                        switch_page('Int_Radiologo')
                    else:
                        switch_page('Int_Neumologo')

                else:
                    st.error('Contraseña Incorrecta, vuelva a intentar')  
            else: 
                st.error('Usuario Incorrecto, vuelva a intentar')
        else:
            st.error('Ingrese su contraseña, por favor')
    else:
        st.error('Ingrese su usuario, por favor')




# 2 metodo en:
# https://towardsdatascience.com/how-to-add-a-user-authentication-service-in-streamlit-a8b93bf02031
