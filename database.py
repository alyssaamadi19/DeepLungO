from deta import Deta  # pip install deta
from skimage.io import imread,imshow,imsave
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import tensorflow as tf


# Initialize with a project key
DETA_KEY = 'e0ahdez9_GP8i1VXapCTobFWSmC87q1GG2Ar13Rtj' ##"e0aeitf6_7Ez5rjjPeN12TfdyAbN34KdzT7Jse29P"
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("METADATA_PRINCIPAL") ##
dv = deta.Drive('PACS_DICOM2PNG') ##
dbc = deta.Base('Cred')
dvg = deta.Drive('GradCam')

# FUNCIONES DE LA BASE DE DATOS
def insert_met(id, name, age, te, r, id_neu, id_rad):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"key": id, "nombre": name, "edad": age, 'tipo_estudio' : te, 'razon': r, 'id_neu': id_neu, 'id_rad': id_rad})
def get_met(period):
    """If not found, the function will return None"""
    return db.get(period)
# FUNCIONES DEL DRIVE
def upload(imname, file):
    # Subimos una Imagen
    return dv.put(name = imname, path =file)
def get_image(name):
    # Obtenemos una Imagen cuando la pedimos por el nombre
    return dv.get(name)
def list_images():
    # Lista de las Imágenes que guarda
    return dv.list()

# FUNCIONES PARA INTEGRACIÓN
def lst_nombres(pdoc): # Lista de Nombres
    res = db.fetch()
    df = pd.DataFrame(res.items)

    if pdoc == 0: # Int Neumologo
        df = df[df['aprob'] == 'T']
    if pdoc == 1: # Int Radiologo
        df = df[df['aprob'] == 'F']
    if pdoc == 2: # Int Radiologo Rect
        df = df[df['aprob'] == 'W']
    #display(df)

    lst_names = list(df['id_rad'])
    lst_id = list(df['key'])
    return lst_names, lst_id, df

def lst_radiologos(): # Lista de Nombres
    res = dbc.fetch()
    df = pd.DataFrame(res.items)
    res2 = db.fetch()
    df2 = pd.DataFrame(res.items)
    
    lst_names = list(df['nombre'])
    lst_id = list(df['key']) 
   
    
    return lst_names, lst_id, df, df2
    

def get_radiog(id): # Obtenemos la Imagen
    iml = get_image(id)
    content = iml.read().decode("utf-8") 
    iml.close()

    glst = []
    content = content.replace('\r', '')
    imlst = content.split('\n')
    imlst = imlst[:len(imlst)-1]

    for lst in imlst:
        l = lst.split(' ')
        l = list(map(float, l))
        glst.append(l)

    im = np.array(glst)
    return im

def get_pw(us): # Extraemos contraseña
    res = dbc.fetch()
    df = pd.DataFrame(res.items)

    try:
        df_us = df[df['usuario'] == us] 
        pw = df_us['contra'].values[0]
        name = df_us['nombre'].values[0]
        doc = df_us['especialidad'].values[0]
        id = df_us['key'].values[0]
    except:
        pw = -1
        name = -1
        doc = -1
        id = -1
    return pw, name, doc,id

def upload_gradcamtxt(id, gradcam): # Subimos el gradcam de una imagen
    data = tf.keras.preprocessing.image.img_to_array(gradcam)
    data = np.transpose(data, (2,0,1))
    with open('test.txt', 'w') as outfile:
        # I'm writing a header here just for the sake of readability
        # Any line starting with "#" will be ignored by numpy.loadtxt
        outfile.write('# {0}\n'.format(data.shape))
        
        # Iterating through a ndimensional array produces slices along
        # the last axis. This is equivalent to data[i,:,:] in this case
        for data_slice in data:

            # The formatting string indicates that I'm writing out
            # the values in left-justified columns 7 characters in width
            # with 2 decimal places.  
            np.savetxt(outfile, data_slice, fmt='%.2f')

            # Writing out a break to indicate different slices...
            outfile.write('# New slice\n')
    f = open('test.txt', 'r')
    dvg.put(id, f)
    os.remove('test.txt')

def get_gradcam(id): # Recuperar GradCam
    file = dvg.get(id)
    content = file.read().decode("utf-8") 
    file.close()

    imlst = content.split('\n')
    imlst.pop()
    s = imlst.pop(0)

    i1 = imlst.index('# New slice')
    l1 = imlst[:i1]
    i2 = imlst[i1+1:].index('# New slice')
    l2 = imlst[i1+1:i1+i2+1]
    l3 = imlst[i1+i2+2:]
    l3.pop()

    for ll in [l1,l2,l3]:
        clst = []
        for li in ll:
            lst_i =  li.split(' ')
            lst_i = list(map(float,lst_i))
            clst.append(lst_i)  
        # x = np.array(clst)
        # print(x.shape)
        if ll is l1:
            gc = np.array(clst)
        else:
            gc = np.dstack([gc, np.array(clst)])
    return gc


def aprob_rad(but, id, diag, com, gradcam =''): # Aprobación del Radiologo
    # Actualizamos la base de datos de pacientes para que los neumologos tengan acceso
    if but == 'A':
        up = {
            'aprob': 'T',
            'diag': diag,
            'comments': com
            }
            # Actualizamos el Drive de Gradcam+Imagen
        upload_gradcamtxt(id,gradcam)
    else:
        up = {
            'aprob': 'W',
            'comments': com}
    db.update(up,id)
