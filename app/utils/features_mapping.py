from typing import Dict

"""
Here are dictionaries to map the collected responses from autopilot
to the features from the Endless Medical API, see: https://www.endlessmedical.com/APIFiles/Features.json
"""
features_mapping: Dict[str, str] = {
    "contact-with-ill-person": "Contacts",
    "has-cough": "SeverityCough",
    "has-fever": "HistoryFever",
    "has-chills": "Chills",
    "has-dyspnea": "DyspneaSeveritySubjective",
    "has-sore-throat": "SoreThroatROS",
    "has-nasal-congestion": "NoseCongestion",
    "lives-in-area": "ExposureToCovid",
}

"""
This contains from collected responses to Endless Medical API valid response values
"""
reponse_mappings: Dict[str, int] = {
    "no": 2,
    "yes": 3,
    "mild": 3,
    "moderate": 4,
    "severe": 5,
}

outcomes_mapping: Dict[str, str] = {"covid-19": "Coronavirus disease 2019 (Covid-19)"}
