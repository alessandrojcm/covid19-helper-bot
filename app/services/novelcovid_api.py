from datetime import date, timedelta

from app.models import Config, CountryStats, APIService


class NovelCOVIDApi(APIService):
    def __init__(self, config: Config):
        super().__init__(config.NOVELCOVID_JHUCSSE_API_URL)

    def get_country_data(
        self, iso3_code: str, last_days: int = 1, append_date=False
    ) -> CountryStats:
        res = self.get(
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

    def lives_in_risky_zone(self, country: str) -> bool:
        return self.get_country_data(country).cases > 0
