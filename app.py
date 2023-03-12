# -*- coding: utf-8 -*-
import json
import os
import string
import warnings
from typing import Dict

import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
from PIL import Image

from model import EfficientNetB7

# TODO: show class probabilities per prediction in sidebar


# suppress future and deprecation warnings
warnings.simplefilter(action="ignore", category=DeprecationWarning)
warnings.simplefilter(action="ignore", category=FutureWarning)


# function to load the model
@st.cache_resource()
def load_model(model_weights_path: str = "resources/model_weights.h5") -> tf.keras.Sequential:
    # build model and compile model, load weights
    model = EfficientNetB7().compile_model()
    model.load_weights(model_weights_path)
    return model


# load the label legend
@st.cache_data()
def load_index_to_label_dict(path: str = "resources/labels.json"):
    # load dictionary containing the labels
    with open(path, "r", encoding="utf-8") as f:
        legend = json.load(f)
    # swap keys and values
    legend = {int(v): k for k, v in legend.items()}
    # make legend more readable
    legend = {k: string.capwords(v.replace("_", " ")) for k, v in legend.items()}
    return legend


# load tourist information
@st.cache_data()
def load_tourist_information(path: str = "resources/tourist_information.json"):
    # TODO
    return ""


# load demo_images dir
@st.cache_data()
def list_demo_images(path: str = "resources/demo_images"):
    # get files
    img_files = os.listdir(path)
    # remove file extensions
    images = [img.replace(".jpg", "").strip() for img in img_files]
    return tuple(images)


# function to load demo images
@st.cache_data()
def load_demo_image(path: str = "resources/demo_images/St. Paulus Dom.jpg"):
    return Image.open(path)


# function to predict the class label
@st.cache_data()
def predict_class_label(img: Image.Image, legend: Dict[int, str], _model: tf.keras.Sequential):
    # predict class probabilities
    class_probabilities = _model.predict(img)
    # get highest likelihood
    prediction = np.argmax(class_probabilities[0])
    # get label
    label = legend[prediction]

    ### display class probabilities
    with st.sidebar:
        st.header("Klassen-Wahrscheinlichkeiten")
        st.write(pd.DataFrame(class_probabilities, index=["Wahrscheinlichkeit"], columns=legend.values()).transpose())

    return label


# function to rescale input images and convert them to tensor
def rescale_and_expand_image(image, output_shape: tuple = (224, 224)):
    # resize image
    imResize = image.resize(output_shape, Image.ANTIALIAS)
    # change to RGB if not yet
    if imResize.mode in ["RGBA", "P"]:
        if imResize.getbands() != 3:
            imResize = imResize.convert("RGB")
    # convert to tensor
    imResize = np.expand_dims(imResize, axis=0)
    return imResize


# run app
if __name__ == "__main__":

    ### get model and resources

    model = load_model()
    legend = load_index_to_label_dict()
    tourist_information = load_tourist_information()

    ### Streamlit page

    # set title
    st.title("Willkommen zur Sight Seeking App!")
    st.write("Finde Informationen zu Münsteraner Sehenwürdigkeiten mit nur einem Foto!")
    # set instructions
    instructions = """
    Du kannst entweder dein eigenes Bild hochladen, im Dropdown-Menü ein vorkonfiguriertes Bild auswählen, oder selbst ein Foto aufnehmen.
    Das von dir ausgewählte oder hochgeladene Bild wird in Echtzeit durch das neuronale Netz geleitet und das Ergebnis wird auf dem Bildschirm angezeigt.
    """
    # display instructions
    st.write(instructions)

    ### File uploader, camera input, and sidebar selector

    demo_images = list_demo_images()
    select_option = st.selectbox("Wähle ein Foto aus", demo_images)

    # get image from file uploader
    file_upload = st.file_uploader("... oder lade ein Bild hoch")
    # get image from camera
    camera_photo = st.camera_input("... oder mach ein Foto und lade es hoch.")
    # even load uploaded file or default file
    if file_upload:
        img = Image.open(file_upload)
        # set title
        st.title("Hier ist das Bild, das du hochgeladen hast:")
    elif camera_photo:
        img = Image.open(camera_photo)
        # set title
        st.title("Hier ist das Foto, das du aufgenommen hast:")
    else:
        img = load_demo_image("resources/demo_images/{}.jpg".format(select_option))
        # set title
        st.title("Hier ist das Bild, das du ausgewählt hast:")
    # show image
    st.image(img)

    ### prepare image for model

    # rescale image for model
    imResize = rescale_and_expand_image(img)

    ### predict image

    label = predict_class_label(imResize, legend, model)

    ### display prediction to user

    st.title("Du stehst wahrscheinlich vor dieser Sehenwürdigkeit:")
    st.header(label)

    ### display tourist information

    # get the correspondig description of the sight
    # TODO: Tourist information
    # sight_description = tourist_information[label]
    # write tourist information to oage
    # st.title("Hier sind einige Informationen zu der Sehenswürdigkeit:")
    # st.write(sight_description)
