from typing import Optional
from datetime import date

from pydantic import BaseModel


class CountryStats(BaseModel):
    country_name: str
    iso3_code: str
    deaths: int
    cases: int
    recoveries: int
    stats_date: Optional[date]

    def __str__(self):
        return self.__generate_str_repr()

    def __generate_str_repr(self):
        if not self.stats_date:
            return (
                "{country} has {cases} cases, {deaths} deaths and {recoveries} recoveries.\nSource: John Hopkins "
                "University.".format(
                    country=self.country_name,
                    deaths=self.deaths,
                    cases=self.cases,
                    recoveries=self.recoveries,
                )
            )

        return (
            "On {date}, {country} had {cases} cases, {deaths} deaths and {recoveries} recoveries.\nSource: John "
            "Hopkins University.".format(
                country=self.country_name,
                deaths=self.deaths,
                cases=self.cases,
                recoveries=self.recoveries,
                date=self.stats_date.strftime("%A %d of %B"),
            )
        )
