import phonenumbers
from phonenumbers import geocoder


def phone_to_country(number: str):
    # Helper function to take a country from a phone number
    parsed = phonenumbers.parse(number)

    if not phonenumbers.is_possible_number(parsed):
        raise ValueError("Invalid phone number")

    return geocoder.country_name_for_number(parsed, "en")
