# -*- coding: utf-8 -*-
import json
import string
from typing import Dict

import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

from models.efficientnet import EfficientNetB7

# TODO: implement photo upload: https://docs.streamlit.io/library/api-reference/widgets/st.camera_input
# TODO: add docstrings


# function to load the model
@st.cache()
def load_model(model_weights_path: str = "models/model_weights.h5") -> tf.keras.Sequential:
    # build model and compile model, load weights
    model = EfficientNetB7().compile_model().load_weights(model_weights_path)
    return model


# load the label legend
@st.cache()
def load_index_to_label_dict(path: str = "resources/labels.json"):
    # load dictionary containing the labels
    with open(path, "r", encoding="utf-8") as f:
        legend = json.load(f)
    # swap keys and values
    legend = {v: k for k, v in legend.items()}
    # make legend more readable
    legend = {k: string.capwords(v.replace("_", " ")) for k, v in legend.items()}
    return legend


# load tourist information
@st.cache()
def load_tourist_information(path: str = "resources/tourist_information.json"):
    # TODO
    return ""


# function to load demo images
@st.cache()
def load_demo_image(path: str = "resources/demo_images/St. Paulus Dom.jpg"):
    return Image.open(path)


# function to predict the class label
@st.cache()
def predict_class_label(img: Image.Image, legend: Dict[int, str], model: tf.keras.Sequential):
    # predict class probabilities
    class_probabilities = model.predict(img)
    # get highest likelihood
    prediction = np.argmax(class_probabilities[0])
    # get label
    label = legend[prediction]
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
    Du kannst entweder dein eigenes Bild hochladen oder in der Seitenleiste ein vorkonfiguriertes Bild auswählen.
    Das von dir ausgewählte oder hochgeladene Bild wird in Echtzeit durch das neuronale Netz geleitet und das Ergebnis wird auf dem Bildschirm angezeigt.
    """
    # display instructions
    st.write(instructions)

    ### File uploader and sidebar selector

    # get image from file uploader
    file_upload = st.file_uploader("Lade ein Bild hoch")
    # even load uploaded file or default file
    if file_upload:
        img = Image.open(file_upload)
        # set title
        st.title("Hier ist das Bild, das du hochgeladen hast:")
    else:
        img = load_demo_image()
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

    st.title("Du stehst wahrscheinlich vor dieser Sehenwürdigkeit:\n {}".format(label))

    ### display tourist information

    # get the correspondig description of the sight
    sight_description = tourist_information[label]
    # write tourist information to oage
    st.title("Hier sind einige Informationen zu der Sehenswürdigkeit:")
    st.write(sight_description)
