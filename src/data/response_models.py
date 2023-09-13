# -*- coding: utf-8 -*-
import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.utils.constants import HTML_REGEX


class SightAddress(BaseModel):
    """
    Model for address.
    """

    # define fields
    street: Optional[str] = Field(..., description="Street of the sight")
    house_number: Optional[str] = Field(..., description="House number of the sight")
    postal_code: Optional[str] = Field(..., description="Postal code of the sight")

    @field_validator("*", mode="before")
    def replace_none_with_empty(cls, value):
        """
        Replace None with empty string.
        :param value: value to check
        :return: input value or empty string
        """
        return value if value is not None else ""


class SightContactDetails(BaseModel):
    """
    Model for contact details.
    """

    # define fields
    phone: str = Field(..., description="Phone number of the sight")
    email: str = Field(..., description="Email address of the sight")
    website: str = Field(..., description="Website of the sight")


class SightText(BaseModel):
    """
    Model for interesting information.
    """

    # define fields
    headline: str = Field(..., description="Headline of the text")
    text: str = Field(..., description="Text")

    @field_validator("text")
    def parse_html(cls, text: str) -> str:
        """
        Remove and parse html tags from text using regex.
        """
        if (r"<ul>" or r"<li>") in text:
            text = re.sub(r"<ul>|</ul>", r"\n" * 2, text)
            text = re.sub(r"<li>|</li>", r"\n", text)
        return re.sub(HTML_REGEX, "", text)


class TouristInformationResponse(BaseModel):
    """
    Response model for tourist information.
    """

    # define fields
    name: str = Field(..., description="Name of the sight")
    description: str = Field(..., pattern=HTML_REGEX, description="Description of the sight")
    address: SightAddress = Field(..., description="Address of the sight")
    additional_information: Optional[list[SightText]] = Field(
        ..., description="Interesting information about the sight"
    )
    contact_details: SightContactDetails = Field(..., description="Contact details of the sight's facility")

    @field_validator("description")
    def remove_html_tags(cls, descr: str) -> str:
        """
        Remove html tags from text using a regex.
        """
        return re.sub(HTML_REGEX, "", descr)
