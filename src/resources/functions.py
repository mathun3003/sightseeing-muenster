# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

import streamlit as st

RESOURCE_DIR = Path("src/resources")
SIGHT_IDS_PATH = os.path.join(os.getcwd(), RESOURCE_DIR, "sight_ids.json")


@st.cache_data()
def load_sight_mapping(path: str = SIGHT_IDS_PATH) -> dict[str, int]:
    """
    Load sight mapping from json file.
    :param path: path to json file
    :return: Dict with
    """
    # load json file from path
    with open(path, "r", encoding="utf-8") as f:
        tourist_information = json.load(f)
    return tourist_information
