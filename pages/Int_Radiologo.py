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
    # 🧿 Apoyo Diagnóstico - Radiología
    ### Nuestra IA utiliza una Red Neuronal Convolucional del tipo Xception, entrenada miles de radiografías provenientes de bases de datos de grado médico.
    ---
    ## Sírvase a encontrar a su paciente:
""")

l,lid,df= D.lst_nombres(1)
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
   
    # Obtenemos la imagen del Drive
    im = D.get_radiog(id)/255.

    
    @st.experimental_memo
    def download_data():
        url = "https://drive.google.com/uc?id=1PLgNw1tK9MobVEa8nTNZ9-RnWpW3Y1vo";
        output = 'weightsXception.h5';
        gdown.download(url, output);
    download_data()
    
    model_path = 'weightsXception.h5'
    pred, gradcam, spi = cad.DLO_predict(im*255., model_path)
    
    st.markdown("""
        ## Probabilidad de Opacidad Pulmonar:    {} %
    """.format(pred))

    if pred >= 50:
        res = 'POSITIVO'
        new_title = '<p style="font-family:monospace; color:#E74C3C; font-size: 30px;"> Resultado: POSITIVO </p>'
    else:
        res = 'NEGATIVO'
        new_title = '<p style="font-family:monospace; color:#27AE60; font-size: 30px;"> Resultado: NEGATIVO </p>'

    # Colores HTML: https://htmlcolorcodes.com/es/

    st.markdown(new_title, unsafe_allow_html=True)
    
    im = Image.fromarray(np.uint8(im*255))

    image_comparison(im,spi, label1 = 'Radiografía Original', label2 =  'Mapa de Calor de la Opacidad')

    st.markdown('# Sección de Comentarios')
    txt = st.text_area('Ingrese aquí sus comentarios doctor', ' ')

    #st.image(gradcam)

    if st.button('APROBAR'):
        st.success('Información del Paciente Actualizada, el Neumólogo ya puede ser los resultados')
        D.aprob_rad('A', id, res, txt, spi)
        switch_page('int radiologo')
    
    if st.button('OBSERVAR/RECTIFICAR'):
        st.info('Se procederá a habilitar el SEGMENTADOR DLO para que pueda CORREGIR el Diagnóstico')
        time.sleep(2)
        D.aprob_rad('R', id, '', txt)
        switch_page('int radiologo rect')
