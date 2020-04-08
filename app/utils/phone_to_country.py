from phonenumbers import geocoder
import phonenumbers


def phone_to_country(number: str):
    parsed = phonenumbers.parse(number)

    if not phonenumbers.is_possible_number(parsed):
        raise ValueError("Invalid phone number")

    return geocoder.country_name_for_number(parsed, "en")
