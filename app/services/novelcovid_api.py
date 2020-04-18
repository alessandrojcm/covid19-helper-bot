from typing import Dict

from requests import Response, get

from app.models import Config, CountryStats


class NovelCOVIDApi(object):
    base_url: str

    def __init__(self, config: Config):
        self.base_url = config.NOVELCOVID_JHUCSSE_API_URL

    def get_country_data(self, iso3_code: str, last_days: int = 1) -> CountryStats:
        res = self.get_request(
            "/historical", {"query": iso3_code, "lastdays": last_days}
        ).json()

        return CountryStats(
            country_name=res["country"],
            iso3_code=iso3_code,
            deaths=list(res["timeline"]["deaths"].values()).pop(),
            cases=list(res["timeline"]["cases"].values()).pop(),
            recoveries=list(res["timeline"]["recoveries"].values()).pop(),
        )

    def get_request(self, path: str, params: Dict[str, str]) -> Response:
        return get(
            self.base_url + path,
            params=params,
            headers={"Content-Type": "application/json"},
        )
