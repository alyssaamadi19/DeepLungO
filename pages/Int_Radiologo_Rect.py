import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from streamlit_image_comparison import image_comparison
from streamlit_extras.switch_page_button import switch_page
import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf
import time
import os

# Funciones en archivos .py fuera del folder de 'pages'. Salimos al dir Streamlit
import sys
sys.path.insert(1, 'C:/Users/Usuario/Desktop/PROYECTO_ACSI/PROY_INTEGRADO/Streamlit') 
import CAD_DLOv1 as cad
import database as D


st.markdown("""
    # ➰ Rectificación Diagnóstica
    ### Sírvase a Segmentar la Imagen en relación a su diagnóstico
    ---
    ## SegmenterDLO:
""")

l,lid,df= D.lst_nombres(2)
l.insert(0,'-')
sel = st.selectbox('Encuentra a tu paciente cuyo diagnóstico esté pendiente de rectificación' , l)

if sel is not '-':
    # Recopilamos la info del paciente
    d = df[df['nombre'] == sel].reset_index(drop = True)
    d.pop('key')
    first_col = d.pop('nombre')
    d.insert(0,'nombre', first_col)

    id = lid[l.index(sel)-1]
    st.markdown("""
            # Paciente: {}
            ### ID: {}
                """.format(sel,id))

    with st.expander("Comentarios Previos"):
        st.write(d['comments'].values[0])   
    
    imx = D.get_radiog(id)
    im = Image.fromarray(np.uint8(imx))

    # CREAMOS EL CANVA
    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:", ("freedraw", "rect", "circle", "transform")
    )

    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    if drawing_mode == 'point':
        point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)

    #stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    # bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
    # bg_image = st.sidebar.file_uploader("Background image:", type=["PNG", "jpg"])
    realtime_update = st.sidebar.checkbox("Update in realtime", True)  

    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color='#E03B3B',
        background_color= '#FFFFFF',
        background_image=im, 
        update_streamlit=realtime_update,
        height=600,
        drawing_mode=drawing_mode,
        point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
        key="canvas",
    )

    #Image.open('C:/Users/PIEROL/Downloads/Database_DLO/DS_DLO/Train/P/impos_1036078.png')

    # Establece el diagnostico final
    st.markdown('# Diagnóstico & Comentarios Finales')
    res= st.radio("DIANÓSTICO:", ('POSITIVO','NEGATIVO'))
    txt = st.text_area('Ingrese aquí sus comentarios Doctor', 'Prev:'+ d['comments'].values[0] + '\n')
    
    
    # Botones para aprobar el resultado
    if st.button('APROBAR'):
        st.success('Información del Paciente Actualizada, el Neumólogo ya puede ser los resultados')
        #Juego con la imagen
        fgi = Image.fromarray(np.array(np.uint8(canvas_result.image_data)))
        fgi.save('img.png', 'PNG')
        fg = Image.open('img.png')

        #Superponemos las imagenes
        s = im.size
        bg = im.convert('RGB')
        bg = bg.resize((600,600))
        fg0 = Image.new(mode = 'RGBA', size = (600,600), color = 'green')
        fg0.putalpha(35)

        bg.paste(fg0, (0,0), fg0)
        bg.paste(fg, (0,0), fg)

        bg = bg.resize((s[0],s[1])) #Volvemos al tamaño original

        #st.image(bg)

        os.remove('img.png')
        st.write(bg.size)

        D.aprob_rad('A', id, res, txt, bg)
        time.sleep(3)
        switch_page('int radiologo')
    
    if st.button('CANCELAR OBS/RECT'):
        D.aprob_rad('F', id, res, '', spi)
        time.sleep(3)
        switch_page('int radiologo')
    
    # Resultados en Tiempo Real 
    # if canvas_result.image_data is not None:
    #     st.image(canvas_result.image_data)
    #     x = Image.fromarray(np.array(np.uint8(canvas_result.image_data)))
    #     x.save('img.png', 'PNG')
    #     st.write(x.size)

    
    