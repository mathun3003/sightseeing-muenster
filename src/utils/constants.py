# -*- coding: utf-8 -*-
from typing import Final, Literal, Type

SIGHT_NAME: Final[str] = "name"
SIGHT_DESCRIPTION: Final[str] = "description_text"

SIGHT_ADDRESS: Final[str] = "address"
SIGHT_ADDRESS_STREET: Final[str] = "street"
SIGHT_ADDRESS_HOUSE_NUMBER: Final[str] = "house_number"
SIGHT_ADDRESS_POSTAL_CODE: Final[str] = "postal_code"


SIGHT_CONTACT_DETAILS: Final[str] = "contact_details"
SIGHT_CONTACT_DETAILS_PHONE: Final[str] = "phone"
SIGHT_CONTACT_DETAILS_EMAIL: Final[str] = "email"
SIGHT_CONTACT_DETAILS_WEBSITE: Final[str] = "website"

LANGUAGES: Type[str] = Literal["de", "en", "nl"]
