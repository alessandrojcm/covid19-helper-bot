from typing import Dict
from datetime import date, timedelta

from requests import Response, get

from app.models import Config, CountryStats


class NovelCOVIDApi(object):
    base_url: str

    def __init__(self, config: Config):
        self.base_url = config.NOVELCOVID_JHUCSSE_API_URL

    def get_country_data(
        self, iso3_code: str, last_days: int = 1, append_date=False
    ) -> CountryStats:
        res = self.get_request(
            "/historical/{code}".format(code=iso3_code), {"lastdays": last_days}
        ).json()

        if append_date:
            return CountryStats(
                country_name=res["country"],
                iso3_code=iso3_code,
                deaths=list(res["timeline"]["deaths"].values())[0],
                cases=list(res["timeline"]["cases"].values())[0],
                recoveries=list(res["timeline"]["recovered"].values())[0],
                stats_date=date.today() - timedelta(days=last_days),
            )
        return CountryStats(
            country_name=res["country"],
            iso3_code=iso3_code,
            deaths=list(res["timeline"]["deaths"].values())[0],
            cases=list(res["timeline"]["cases"].values())[0],
            recoveries=list(res["timeline"]["recovered"].values())[0],
        )

    def get_request(self, path: str, params: Dict[str, str]) -> Response:
        return get(
            self.base_url + path,
            params=params,
            headers={"Content-Type": "application/json"},
        )
