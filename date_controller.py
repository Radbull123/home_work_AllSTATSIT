"""Date Controller helps to have maniplation with provided data"""

from typing import Tuple
from data_objects import YearData, MonthData, DayData
from interfaces.day_interface import DayInterface
from interfaces.month_interface import MonthInterface
from interfaces.year_interface import YearInterface


class DateController:

    def __init__(self, day: str, month: str, year: str) -> None:
        self.year_interface = YearInterface(YearData(int(year)))
        self.month_interface = MonthInterface(MonthData(int(month), self.year_interface.max_days_in_a_year))
        self.day_interface = DayInterface(
            DayData(int(day), self.month_interface.get_max_days_in_month())
        )

    @staticmethod
    def validate_date(full_date: str) -> Tuple[int, ...]:
        if (dot_count := full_date.count(".")) != 2:
            raise ValueError(f"Has to be 3 dots in a date, got: {dot_count}")

        elif not all(date.isdigit() for date in full_date.split(".")):
            raise TypeError(
                f"Incorrect date value: {full_date}, date should be contained from digits only, and separated by dots."
                "The following order: dd.mm.yyyy"
            )
    
    def __convert_date_to_total_days(self):
        return self.day_interface.day\
             + self.month_interface.convert_month_in_days(self.month_interface.month -1)\
             + self.year_interface.convert_year_in_days(self.year_interface.year - 1)

    def __convert_total_days_to_date_data(self, total_days: int):
        year_data, total_days = self.year_interface.convert_days_to_year(total_days)
        month_data, total_days = self.month_interface.convert_days_to_month(total_days)
        return (
            DayData(
                day=total_days, 
                max_days=self.month_interface.get_max_days_in_month(month_data.month)
            ),
            month_data,
            year_data,
        )

    def add_date(self, days: int) -> Tuple[int, ...]:
        sum_of_days = self.__convert_date_to_total_days() + int(days)
        day_data, month_data, year_data = self.__convert_total_days_to_date_data(sum_of_days)

        return day_data.day, month_data.month, year_data.year
