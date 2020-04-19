from pydantic import BaseModel


class CountryStats(BaseModel):
    country_name: str
    iso3_code: str
    deaths: int
    cases: int
    recoveries: int

    def __str__(self):
        return "{country} has {cases} cases, {deaths} deaths and {recoveries} recoveries.\nSource: John Hopkins University.".format(
            country=self.country_name,
            deaths=self.deaths,
            cases=self.cases,
            recoveries=self.recoveries,
        )
