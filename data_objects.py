"""Space where store data classes needed for parsing data.""" 
from dataclasses import dataclass, field
from typing import Any

from .errors import DateValError


@dataclass
class DayData:
    day: int
    max_days: int

    def __post_init__(self):
        if self.day not in range(1, self.max_days + 1):
            raise DateValError(self.__class__.__name__, min_value=1, max_value=self.max_days, actual_value=self.day)


@dataclass
class YearData:
    year: int
    avarage_days_in_year: int = field(default=365.2425, init=False, repr=True)
    max_days_in_year: int = field(init=False, repr=True)

    def __post_init__(self):
        if self.year < 1:
            raise DateValError(self.__class__.__name__, min_value=0, actual_value=self.year)
        else:
            self.max_days_in_year = 366 if self.year % 4 == 0 or self.year % 100 == 0 or self.year % 400 == 0 else 365

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        year = kwds['year'] if kwds else args[0] 
        self.__init__(year)
        return self

@dataclass
class MonthData:
    month: int
    max_days_in_year: int
    min_month: int = field(default=1)
    max_month: int = field(default=12, init=False, repr=True)

    def __post_init__(self):
        if self.month not in range(self.min_month, self.max_month + 1):
            raise DateValError(self.__class__.__name__, min_value=1, max_value=self.max_month, actual_value=self.month)
