import streamlit as st
from streamlit_image_comparison import image_comparison
import numpy as np
from PIL import Image
import gdown

# Funciones en archivos .py fuera del folder de 'pages'. Salimos al dir Streamlit
import sys
sys.path.insert(1, 'C:/Users/Usuario/Desktop/PROYECTO_ACSI/PROY_INTEGRADO/Streamlit')  
#path = os.getcwd()
#sys.path.insert(1, path)  
import CAD_DLOv1 as cad
import database as D


st.markdown("""
    # 👨‍⚕️ Resultados - Neumólogía
    ### Los resultados son aprobados por el Médico Radiólogo correspondiente, en apoyo con nuestra IA.
    ---
    ## Sírvase a encontrar a su paciente:
""")

l,lid,df= D.lst_nombres(0)
l.insert(0,'-')
sel = st.selectbox('Encuentra a tu paciente en la base de datos del PACS y obten la probabilidad de diagnóstico de Opacidad Pulmonar' , l)

if sel is not '-':
    # Extraemos index
    d = df[df['nombre'] == sel].reset_index(drop = True)
    d.pop('key')
    first_col = d.pop('nombre')
    d.insert(0,'nombre', first_col)

    id = lid[l.index(sel)-1]

    st.markdown("""
            # Paciente: {}
            ### ID: {}
                """.format(sel,id))

    st.dataframe(d)
    res = d['diag'].values[0]
   
    # Obtenemos la imagen del Drive
    im = D.get_radiog(id)/255.

    if res == 'POSITIVO':
        new_title = '<p style="font-family:monospace; color:#E74C3C; font-size: 30px;"> Resultado: POSITIVO </p>'
    else:
        new_title = '<p style="font-family:monospace; color:#27AE60; font-size: 30px;"> Resultado: NEGATIVO </p>'

    # Colores HTML: https://htmlcolorcodes.com/es/

    st.markdown(new_title, unsafe_allow_html=True)

    with st.expander("Comentarios del Médico Radiólgo"):
        st.write(d['comments'].values[0])
    
    im = Image.fromarray(np.uint8(im*255))

    spi = Image.fromarray(np.uint8(D.get_gradcam(id)))

    image_comparison(im,spi, label1 = 'Radiografía Original', label2 =  'Mapa de Calor de la Opacidad')
