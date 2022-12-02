import streamlit as st
from streamlit_image_comparison import image_comparison
from streamlit_extras.switch_page_button import switch_page
import numpy as np
from PIL import Image, ImageOps
import time
import gdown


page_bg = """
<style>
[data-testid = "stAppViewContainer"]
background-image: url("https://images.wallpapersden.com/image/download/abstract-wave-hd-blue_bWZnbm6UmZqaraWkpJRoaWprrWdnaGk.jpg");
background-size: cover;
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html = True)


# Funciones en archivos .py fuera del folder de 'pages'. Salimos al dir Streamlit
import sys
sys.path.insert(1, 'C:/Users/Usuario/Desktop/PROYECTO_ACSI/PROY_INTEGRADO/Streamlit') 
#path = os.getcwd()
#sys.path.insert(1, path)  
import CAD_DLOv1 as cad
import database as D


st.markdown("""
    # 🧿 Dashboard  - Radiología
    ### ¿Cuántos pacientes tienes?""")

################################

        

lst_names, lst_id, df, df2= D.lst_radiologos()
lst_names.insert(0,'-')
sel = st.selectbox("Ingresa tu key",l)
display(df)
display(df2)

if us=="RadioAC_002":
    id_rad = df2[df2['id_neu']== "RadioAC_002"]    
if us=="RadioJP_001":
    id_rad='0'
    
if us=="RadioJP_003":
    id_rad='1'

#######################################
    



