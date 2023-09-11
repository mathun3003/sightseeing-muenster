# -*- coding: utf-8 -*-
from typing import get_args

import streamlit as st
from PIL import Image

from sight_seeing_ms.data.get_info import DataPortalMS
from sight_seeing_ms.data.response_models import TouristInformationResponse
from sight_seeing_ms.models.efficientnetv2s import EfficientNetV2S, transform
from sight_seeing_ms.utils.caching_functions import load_sight_mapping
from sight_seeing_ms.utils.constants import LANGUAGES
from sight_seeing_ms.utils.translation import translate


class SightseeingApp:
    """
    Class to represent the Sightseeing App
    """

    @staticmethod
    def header(lang: str) -> None:
        """
        Function to display the header of the app
        :param lang: language the app is displayed in
        :return: None
        """
        # set title
        st.title(translate("Willkommen zur Sightseeing Münster App!", lang))
        st.write(translate("Finde Informationen zu Münsteraner Sehenwürdigkeiten mit nur einem Foto!", lang))
        # display instructions
        st.write(
            translate(
                """Du kannst entweder dein eigenes Bild hochladen, oder selbst ein Foto aufnehmen. Das von
        dir hochgeladene Bild wird in Echtzeit durch das neuronale Netz geleitet und das Ergebnis wird auf dem
        Bildschirm angezeigt.""",
                lang,
            )
        )

    # pylint: disable=inconsistent-return-statements
    @staticmethod
    def image_upload(lang: str) -> Image:
        """
        Function to load an image into the app
        :param lang: language the app is displayed in
        :return: Pillow Image
        """
        # get image from file uploader
        file_upload = st.file_uploader(translate("Lade ein Bild hoch", lang))
        # get image from camera
        camera_photo = st.camera_input(translate("... oder mache ein Foto und lade es hoch.", lang))
        st.divider()
        # even load uploaded file or default file
        if file_upload:
            img = Image.open(file_upload)
            # set title
            st.title(translate("Hier ist das Bild, das du hochgeladen hast:", lang))
        elif camera_photo:
            img = Image.open(camera_photo)
            # set title
            st.title(translate("Hier ist das Foto, das du aufgenommen hast:", lang))
        else:
            st.stop()
        if file_upload or camera_photo:
            # show image
            st.image(img)
            return img

    @staticmethod
    def sight_information(lang: str, tourist_information: TouristInformationResponse) -> None:
        """
        Function to display the tourist information
        :param lang: language the information should be displayed
        :param tourist_information: tourist information to display
        :return: None
        """
        # display prediction to user
        st.markdown(f"### {translate('Du stehst wahrscheinlich vor dem:', lang)}")
        st.markdown(f"#### {tourist_information.name}")
        st.divider()
        # write tourist information to page
        st.markdown(f"### {translate('Hier sind einige Informationen zu der Sehenswürdigkeit:', lang)}")
        st.markdown(f"#### {translate('Beschreibung', lang)}:")
        st.write(tourist_information.description)
        st.markdown(f"#### {translate('Adresse', lang)}:")
        st.write(
            f"""
        {tourist_information.address.street} {tourist_information.address.house_number},
        {tourist_information.address.postal_code} Münster"""
        )
        st.markdown(f"#### {translate('Kontakt', lang)}:")
        st.write(
            f"""
                {translate('Telefonnummer', lang)}: {tourist_information.contact_details.phone}\n
                {translate('E - Mail', lang)}: {tourist_information.contact_details.email}\n
                {translate('Website', lang)}: {tourist_information.contact_details.website}"""
        )
        st.markdown(f"#### {translate('Weitere Informationen', lang)}:")
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
    app = SightseeingApp()
    app.header(lang)
    image = app.image_upload(lang)
    # transform image
    transformed_image = transform(image)
    # predict label
    label = model.predict_class_label(transformed_image)
    # get tourist information
    tourist_information = dataportal.get_tourist_information(sight_ids[label])
    # display prediction to user
    app.sight_information(lang, tourist_information)


if __name__ == "__main__":
    main()
