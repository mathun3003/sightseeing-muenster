from io import BytesIO
from PIL import Image
import os
import streamlit as st


prediction = "St. Paulus Dom"
img = None

def rescale_image(img, output_shape: tuple=(224,224)):
    imResize = img.resize(output_shape, Image.ANTIALIAS)
    if imResize.mode in ["RGBA", "P"]:
        if imResize.getbands() != 3:
            imResize = imResize.convert("RGB")
    return imResize
    

def load_model():
    # TODO
    pass


def predict_image():
    # TODO
    pass


if __name__ == "__main__":
    st.title("Sight Seeking App - Finde Informationen zu Münsteraner Sehenwürdigkeiten mit nur einem Foto!")
    instructions = """
    
    """
    st.write(instructions)
    
    file_upload = st.file_uploader("Lade ein Bild hoch")

    if file_upload:
        img = Image.open(file_upload)
    else:
        img = Image.open("demo_images/20230208_162937.jpg")
    # rescale image
    imResize = rescale_image(img)
    
    # show image
    st.title("Hier ist das Bild, das du hochgeladen hast.")
    st.image(imResize)
    
    st.title("Du stehst wahrscheinlich vor/bei dem/den {}".format(prediction))
    
    st.title("Hier sind einige Informationen zu der Sehenswürdigkeit: ")
    