# -*- coding: utf-8 -*-
from typing import get_args

import streamlit as st
from translate import Translator

from core.constants import LANGUAGES  # pylint: disable=import-error


@st.cache_data()
def translate(text: str, target_language: str) -> str:
    """
    Translate text to target language.
    :param text: text to translate
    :param target_language:
    :return: translated text or input text if target language is 'de'
    """
    # check if target language is supported
    if target_language not in get_args(LANGUAGES):
        raise ValueError(f"Language {target_language} is not supported.")
    # translate text
    if target_language != "de":
        translator = Translator(to_lang=target_language, from_lang="de")
        translation = translator.translate(text)
        return translation
    return text
