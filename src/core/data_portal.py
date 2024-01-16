# -*- coding: utf-8 -*-
# pylint: disable=import-error
import os
from typing import Optional

import requests
from data.response_models import (
    SightAddress,
    SightContactDetails,
    SightText,
    TouristInformationResponse,
)

from utils.constants import (
    SIGHT_ADDRESS,
    SIGHT_ADDRESS_HOUSE_NUMBER,
    SIGHT_ADDRESS_POSTAL_CODE,
    SIGHT_ADDRESS_STREET,
    SIGHT_CONTACT_DETAILS,
    SIGHT_CONTACT_DETAILS_EMAIL,
    SIGHT_CONTACT_DETAILS_PHONE,
    SIGHT_CONTACT_DETAILS_WEBSITE,
    SIGHT_DESCRIPTION,
    SIGHT_NAME,
)
from utils.logger import CustomLogger

logger = CustomLogger().get_logger()


# pylint: disable=too-few-public-methods
class DataPortalMS:
    """
    Class to fetch data from the Data Portal Münsterland.
    """

    def __init__(self, language: str) -> None:
        """
        Initialize the Data Portal Münsterland
        :param language:
        """
        self.language = language
        self._username = os.getenv("API_USERNAME")
        self._token = os.getenv("API_TOKEN")
        self.header = {"Content-Type": "application/json", "Authorization": f"Basic {self._token}"}

    def get_tourist_information(self, sight_id: int) -> TouristInformationResponse:
        """
        Get tourist information for a sight.
        :param sight_id: ID of the sight
        :return: Tourist information
        """
        url = f"https://www.datenportal-muensterland.de/api/v1/pois/{sight_id}"
        response = self._fetch(url, params={"append": "all_translations_grouped"} if self.language != "de" else None)
        # get core from response
        tourist_information = response["data"]
        # get sight address
        sight_address = SightAddress(
            street=tourist_information[SIGHT_ADDRESS][SIGHT_ADDRESS_STREET],
            house_number=tourist_information[SIGHT_ADDRESS][SIGHT_ADDRESS_HOUSE_NUMBER],
            postal_code=tourist_information[SIGHT_ADDRESS][SIGHT_ADDRESS_POSTAL_CODE],
        )
        # get contact details
        sight_contact_details = SightContactDetails(
            phone=tourist_information[SIGHT_CONTACT_DETAILS][SIGHT_CONTACT_DETAILS_PHONE],
            email=tourist_information[SIGHT_CONTACT_DETAILS][SIGHT_CONTACT_DETAILS_EMAIL],
            website=tourist_information[SIGHT_CONTACT_DETAILS][SIGHT_CONTACT_DETAILS_WEBSITE],
        )
        # get correct translation for name and description
        if self.language != "de":
            name = tourist_information["all_translations_grouped"][self.language][SIGHT_NAME]
            description = tourist_information["all_translations_grouped"][self.language][SIGHT_DESCRIPTION]
        else:
            name = tourist_information[SIGHT_NAME]
            description = tourist_information[SIGHT_DESCRIPTION]
        # get additional information translation
        if self.language != "de":
            additional_information = [
                SightText(
                    headline=info["all_translations_grouped"][self.language]["headline"],
                    text=info["all_translations_grouped"][self.language]["text"],
                )
                for info in tourist_information["texts"]
            ]
        else:
            additional_information = [
                SightText(headline=info["headline"], text=info["text"]) for info in tourist_information["texts"]
            ]

        return TouristInformationResponse(
            name=name,
            description=description,
            address=sight_address,
            contact_details=sight_contact_details,
            additional_information=additional_information,
        )

    def _fetch(
        self, url: str, method: str = "GET", payload: Optional[dict] = None, params: Optional[dict] = None
    ) -> dict:
        """
        Fetch data from the data portal.
        :param url: API url
        :param method: HTTP method. Defaults to GEt.
        :param payload: Data payload. Defaults to None.
        :param params: URL parameters. Defaults to None.
        :return: JSON response
        """
        response = requests.request(method, url, headers=self.header, data=payload, params=params, timeout=60)
        if not response.ok:
            logger.error(f"Error fetching data from {url}. Status code: {response.status_code}, {response.reason}")
            response.raise_for_status()
        return response.json()
