import json
from datetime import date

from fastapi import APIRouter, Form
from loguru import logger

from app.core import config
from app.custom_router import AutopilotRoute
from app.services import NovelCOVIDApi

main_menu = APIRouter()
main_menu.route_class = AutopilotRoute
novelcovid_api = NovelCOVIDApi(config)


@logger.catch
@main_menu.post("/stats-for-country")
async def stats_for_country(Memory: str = Form(...)):
    """
    Gets the latest data for a single country
    :param: Memory: JSON Stringified object from Twilio
    """
    memory = json.loads(Memory)
    twilio = memory.pop("twilio")

    iso3_code = twilio["collected_data"]["country-iso-3"]["answers"]["country_info"][
        "answer"
    ]

    stats = str(novelcovid_api.get_country_data(iso3_code=iso3_code))
    return {"actions": [{"say": stats}, {"redirect": "task://menu-description"}]}


@logger.catch
@main_menu.post("/history-for-country")
async def history_for_country(Memory: str = Form(...)):
    """
    Gets the data for a single country on a given date
    :param: Memory: JSON Stringified object from Twilio
    """
    memory = json.loads(Memory)
    twilio = memory.pop("twilio")

    today = date.today()

    iso3_code = twilio["collected_data"]["country-and-date"]["answers"]["country_info"][
        "answer"
    ]
    # For some reason, Twilio parses the date as 1 year in the future ¯\_(ツ)_/¯
    history_point = date.fromisoformat(
        twilio["collected_data"]["country-and-date"]["answers"]["historical_date"][
            "answer"
        ]
    ).replace(year=today.year)

    if history_point > today:
        return {
            "actions": [
                {
                    "say": "Sorry {name}, looks like that day has not arrived yet! Let's try again".format(
                        name=memory["name"]
                    )
                },
                {"redirect": "task://history-for-country"},
            ]
        }

    timedelta = (today - history_point).days
    stats = str(
        novelcovid_api.get_country_data(
            iso3_code=iso3_code, last_days=timedelta, append_date=True
        )
    )

    return {"actions": [{"say": stats}, {"redirect": "task://menu-description"}]}
