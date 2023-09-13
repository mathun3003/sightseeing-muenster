# -*- coding: utf-8 -*-
import json
from os import PathLike

import streamlit as st

from src.utils.constants import SIGHT_IDS_PATH


@st.cache_data()
def load_sight_mapping(path: PathLike = SIGHT_IDS_PATH) -> dict[str, int]:
    """
    Load sight mapping from json file.
    :param path: path to json file
    :return: Dict with
    """
    # load json file from path
    with open(path, "r", encoding="utf-8") as f:
        tourist_information = json.load(f)
    return tourist_information
