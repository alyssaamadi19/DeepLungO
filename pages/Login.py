import streamlit as st

# Funciones en archivos .py fuera del folder de pages. Tendras que cambiarlo para tu compu
import sys
sys.path.insert(1, 'C:/Users/PIEROL/Desktop/DeepLearningOp/Streamlit') 
import CAD_DLOv1 as cad
import database as D


page_bg = """
<style>
[data-testid = "stAppViewContainer"]{
background-image: url("https://img.freepik.com/free-photo/abstract-orange-paint-background-acrylic-texture-with-marble-pattern_1258-90489.jpg?w=2000");
background-size: cover;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html = True)

st.markdown("""
    # 👥 Ingrese sus credenciales
""")

us = st.text_input("Usuario")
pw = st.text_input("Contraseña",type="password")


if st.button("Ingresar"):
    if us is not '':
        if pw is not '':
            pw_real, name = D.get_pw(us)
            if pw_real is not -1:
                if pw == pw_real:
                    msj = 'Bienvenido Doctor ' + name
                    st.success(msj)
                else:
                    st.error('Contraseña Incorrecta, vuelva a intentar')  
            else: 
                st.error('Usuario Incorrecto, vuelva a intentar')
        else:
            st.error('Ingrese su contraseña, por favor')
    else:
        st.error('Ingrese su usuario, por favor')
