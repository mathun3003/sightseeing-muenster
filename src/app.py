# -*- coding: utf-8 -*-
# pylint: disable=import-error
from typing import get_args

import streamlit as st
from PIL import Image

from core.models import TouristInformationResponse
from ml_models.efficientnetv2s import EfficientNetV2S, transform
from src.core.constants import LANGUAGES
from src.core.data_portal import DataPortalMS
from utils.functions import load_sight_mapping
from utils.translation import translate


class SightseeingApp:
    """
    Class to represent the Sightseeing App
    """

    def __init__(self, language: str) -> None:
        """
        Initializes the Sightseeing Münster App
        :param language: Language in which the app will be displayed.
        :return: None
        """
        self.lang = language

    def header(self) -> None:
        """
        Function to display the header of the app
        :return: None
        """
        # set title
        st.title(translate("Willkommen zur Sightseeing Münster App!", self.lang))
        st.write(translate("Finde Informationen zu Münsteraner Sehenwürdigkeiten mit nur einem Foto!", self.lang))
        # display instructions
        st.write(
            translate(
                """Du kannst entweder ein vorhandenes Bild hochladen, oder selbst ein Foto mit der Kamera
                aufnehmen. Ein neuronales Netz erkennt das von dir hochgeladene Foto und gibt dir passende
                Informationen zu der Sehenswürdigkeit auf dem Foto.""",
                self.lang,
            )
        )

    # pylint: disable=inconsistent-return-statements
    def image_upload(self) -> Image:
        """
        Function to load an image into the app
        :return: Pillow Image
        """
        file_upload, camera_photo = None, None
        upload_options = [translate("Bild hochladen", self.lang), translate("Foto aufnehmen", self.lang)]
        option = st.selectbox(label=translate("Wie möchtest du ein Foto hochladen?", self.lang), options=upload_options)
        # if file upload was selected
        if option == upload_options[0]:
            # get image from file uploader
            file_upload = st.file_uploader(translate("Lade ein Bild hoch", self.lang))
            if not file_upload:
                st.stop()
            img = Image.open(file_upload)
        # if camera was selected
        elif option == upload_options[1]:
            # get image from camera
            camera_photo = st.camera_input(translate("Nehme ein Foto mit deiner Kamera auf.", self.lang))
            if not camera_photo:
                st.stop()
            img = Image.open(camera_photo)
        else:
            st.stop()
        st.divider()
        # even load uploaded file or default file
        if file_upload:
            # set title
            st.title(translate("Hier ist das Bild, das du hochgeladen hast:", self.lang))
        elif camera_photo:
            # set title
            st.title(translate("Hier ist das Foto, das du aufgenommen hast:", self.lang))
        else:
            st.stop()
        if file_upload or camera_photo:
            # show image
            st.image(img)
            return img

    def sight_information(self, tourist_information: TouristInformationResponse) -> None:
        """
        Function to display the tourist information
        :param tourist_information: tourist information to display
        :return: None
        """
        # display prediction to user
        st.markdown(f"### {translate('Du stehst wahrscheinlich vor dem:', self.lang)}")
        st.markdown(f"#### {tourist_information.name}")
        st.divider()
        # write tourist information to page
        st.markdown(f"### {translate('Hier sind einige Informationen zu der Sehenswürdigkeit:', self.lang)}")
        st.markdown(f"#### {translate('Beschreibung', self.lang)}:")
        st.write(tourist_information.description)
        st.markdown(f"#### {translate('Adresse', self.lang)}:")
        st.write(
            f"""
        {tourist_information.address.street} {tourist_information.address.house_number},
        {tourist_information.address.postal_code} Münster"""
        )
        st.markdown(f"#### {translate('Kontakt', self.lang)}:")
        st.write(
            f"""
                {translate('Telefonnummer', self.lang)}: {tourist_information.contact_details.phone}\n
                {translate('E - Mail', self.lang)}: {tourist_information.contact_details.email}\n
                {translate('Website', self.lang)}: {tourist_information.contact_details.website}"""
        )
        st.markdown(f"#### {translate('Weitere Informationen', self.lang)}:")
        if tourist_information.additional_information:
            for info in tourist_information.additional_information:
                with st.expander(info.headline):
                    st.write(info.text)


def main() -> None:
    """Main Function to start the streamlit app."""
    # set language
    lang = st.sidebar.selectbox("Language", map(str.upper, get_args(LANGUAGES))).lower()  # type: ignore

    # load model and app resources
    model = EfficientNetV2S()
    sight_ids = load_sight_mapping()
    dataportal = DataPortalMS(language=lang)

    # create app
    app = SightseeingApp(language=lang)
    app.header()
    image = app.image_upload()
    # transform image
    transformed_image = transform(image)
    with st.spinner(translate("Erkenne Sehenswüridkeit", lang)):
        # predict label
        label = model.predict_class_label(transformed_image)
    with st.spinner(translate("Lade Informationen", lang)):
        # get tourist information
        tourist_information = dataportal.get_tourist_information(sight_ids[label])
        # display prediction to user
        app.sight_information(tourist_information)


if __name__ == "__main__":
    main()
