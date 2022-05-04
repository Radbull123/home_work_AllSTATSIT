import math
from typing import Tuple
from data_objects import YearData


class YearInterface:

    def __init__(self, year_data: YearData):
        self.__year_data = year_data
        
    def convert_year_in_days(self, year):
        return math.floor(year * self.avarage_days_in_year)

    def convert_days_to_year(self, total_days) -> Tuple[YearData, int]:
        current_year = math.ceil(total_days / self.avarage_days_in_year)
        total_days = math.ceil(total_days % self.avarage_days_in_year)
        current_year_data = YearData(current_year)
        return current_year_data, total_days

    @property
    def year(self):
        return self.__year_data.year

    @property
    def avarage_days_in_year(self):
        return self.__year_data.avarage_days_in_year

    @property
    def max_days_in_a_year(self):
        return self.__year_data.max_days_in_year
