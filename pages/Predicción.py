import streamlit as st
from streamlit_image_comparison import image_comparison
import numpy as np
from PIL import Image
import PIL
import gdown


# Funciones en archivos .py fuera del folder de 'pages'. Salimos al dir Streamlit
import sys
import os
path = os.getcwd()
sys.path.insert(1, path)  
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
    # 🧿 Predicción de Radiografía
    ### Nuestra IA utiliza una Red Neuronal Convolucional del tipo Xception, entrenada miles de radiografías provenientes de bases de datos de grado médico.
    ---
    ## Sírvase a encontrar a su paciente:
""")

l,lid,df= D.lst_nombres()
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

    # st.markdown("""
    #         # Paciente: {}
    #         ### ID: {}
    #         ### Edad: {}
    #         ### Tipo Estudio:  {}
    #         ### Médico Neumólogo {}
    #         ### Médico Radiólogo {}
    #             """.format(sel,id,d['edad'].values[0], d['tipo_estudio'].values[0],d['m_neumologo'].values[0],d['m_radiologo'].values[0]))

    st.dataframe(d)
   
   
    # Obtenemos la imagen del Drive
    im = D.get_radiog(id)/255. 
    #st.image(im)
    
    #id= 1jUUB_5C2WHuKD-x_dQgh5-1fD2lPyWoS
    @st.experimental_memo
    def download_data():
        url = "https://drive.google.com/uc?id=1jUUB_5C2WHuKD-x_dQgh5-1fD2lPyWoS";
        output = 'weights.h5';
        gdown.download(url, output);
    download_data()
    
    model_path = 'weights.h5'
    pred, gradcam = cad.DLO_predict(im*255., model_path)
    
    st.markdown("""
        ## Probabilidad de Opacidad Pulmonar:    {} %
    """.format(pred))
    
    im = Image.fromarray(np.uint8(im*255))
    gradcam = Image.fromarray(np.uint8(gradcam*255 + 255))
    gradcam = PIL.ImageOps.invert(gradcam)

    image_comparison(im,gradcam, label1 = 'Radiografía Original', label2 =  'Mapa de Calor de la Opacidad')

    st.markdown('# Sección de Comentarios')
    txt = st.text_area('Ingrese aquí sus comentarios doctor', '''
    ''')

    #st.image(gradcam)
