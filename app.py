# -*- coding: utf-8 -*-
import json
import logging
import os
import sys
import warnings
from typing import Dict

import numpy as np
import pandas as pd
import streamlit as st
import streamlit_toggle as tog
import tensorflow as tf
from PIL import Image

from model import EfficientNetB7

# suppress future and deprecation warnings
warnings.simplefilter(action="ignore", category=DeprecationWarning)
warnings.simplefilter(action="ignore", category=FutureWarning)

# create logger instance
log = logging.getLogger(__name__)
# log to stdout
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)


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
    # # make legend more readable
    return legend


# load tourist information
@st.cache_data()
def load_tourist_information(path: str = "resources/tourist_information.json"):
    # load json file from path
    with open(path, "r", encoding="utf-8") as f:
        tourist_information = json.load(f)
    # ensure integer keys
    tourist_information = {int(k): v for k, v in tourist_information.items()}
    return tourist_information


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
    # return label, prediction, and class probabilities
    return label, prediction, class_probabilities


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
    st.title("Willkommen zur Sightseeing Münster App!")
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

    ### predict image, store prediction and class probabilities

    label, prediction, class_probabilities = predict_class_label(imResize, legend, model)

    ### display prediction to user

    st.title("Du stehst wahrscheinlich vor dieser Sehenwürdigkeit:")
    st.header(label)

    ### display class probabilities

    with st.sidebar:
        # define switch
        switch = tog.st_toggle_switch(
            label="Klassen-Wahrscheinlichkeiten anzeigen",
            key="Key1",
            default_value=False,
            label_after="Klassen-Wahrscheinlichkeiten ausblenden",
            inactive_color="#D3D3D3",
            active_color="#11567f",
            track_color="#29B5E8",
        )
        # if switch was turned on
        if switch:
            # show class probabilities
            st.header("Klassen-Wahrscheinlichkeiten")
            st.write(pd.DataFrame(class_probabilities, index=["Wahrscheinlichkeit"], columns=legend.values()).transpose())

    ### display tourist information

    # get the correspondig description of the sight
    sight_description = tourist_information[prediction]
    # write tourist information to oage
    st.subheader("Hier sind einige Informationen zu der Sehenswürdigkeit:")
    st.write(sight_description)
