import phonenumbers
import requests
from phonenumbers import carrier
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .errors import ValidationError


def requests_retry_session(
    retries=3, backoff_factor=0.3, status_forcelist=(502, 504), session=None, **kwargs
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def validate_phone_number(number):
    phone_obj = phonenumbers.parse(number, "UG")
    if not phonenumbers.is_valid_number(phone_obj):
        raise ValidationError(f"Invalid phone number {number}")
    if carrier.name_for_number(phone_obj, "en") not in ["MTN", "Airtel"]:
        raise ValidationError(
            f"{number}: Only MTN and Airtel are supported at the moment."
        )

    return f"256{phone_obj.national_number}"


def validate_string(_string):
    if not isinstance(_string, str):
        raise ValidationError(f"{_string}: Must be a string.")

    return _string


def validate_number(number):
    number_types = (int, float)
    if not type(number) in number_types:
        raise ValidationError(f"{number}: Must be a number")

    return number
