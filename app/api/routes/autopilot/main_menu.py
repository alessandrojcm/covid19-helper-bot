import json

from fastapi import APIRouter, HTTPException, Form
from loguru import logger

from app.custom_routers import UserIdentifierRoute
from app.models import CountryStats
from app.services import NovelCOVIDApi
from app.core import config

main_menu = APIRouter()
main_menu.route_class = UserIdentifierRoute
novelcovid_api = NovelCOVIDApi(config)


@logger.catch
@main_menu.post("/stats-for-country")
async def stats_for_country(Memory: str = Form(...)):
    memory = json.loads(Memory)
    twilio = memory.pop("twilio")

    iso3_code = twilio["collected_data"]["country-iso-3"]["answers"]["country_info"][
        "answer"
    ]

    stats = str(novelcovid_api.get_country_data(iso3_code=iso3_code))
    return {"actions": [{"say": stats}, {"redirect": "task://menu-description"},]}
