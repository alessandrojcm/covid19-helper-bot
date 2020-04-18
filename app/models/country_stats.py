from pydantic import BaseModel


class CountryStats(BaseModel):
    country_name: str
    iso3_code: str
    deaths: int
    cases: int
    recoveries: int
