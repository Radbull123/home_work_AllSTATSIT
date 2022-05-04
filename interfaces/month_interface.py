"""Interface for month dataclass"""

from typing import Tuple
from data_objects import MonthData


class MonthInterface:

    def __init__(self, month_data: MonthData) -> None:
        self.__month_data = month_data

    def convert_month_in_days(self, month: int):
        days_count = 0
        current_month = MonthData(month, self.max_days_in_year, min_month=0)
        max_days_in_month_2 = 28 if self.max_days_in_year == 365 else 29
        
        while current_month.month > 0:
            if current_month.month == 2:
                days_count += max_days_in_month_2
            else:
                days_count += 30 if current_month.month % 2 == 0 and current_month.month not in (4, 12) else 31
            
            current_month = MonthData(current_month.month - 1, max_days_in_year=self.max_days_in_year, min_month=0)

        return days_count

    def convert_days_to_month(self, total_days: int) -> Tuple[MonthData, int]:
        current_month_data = MonthData(1, self.max_days_in_year)
        max_days_in_month_2 = 28 if self.max_days_in_year == 365 else 29
        while total_days >= self.get_max_days_in_month():
            if current_month_data.month == 2:
               total_days -= max_days_in_month_2
            else:
                total_days -= 30 if current_month_data.month % 2 == 0\
                    and current_month_data.month not in (4, 12) else 31

            current_month_data = MonthData(current_month_data.month + 1, self.max_days_in_year)
        
        if total_days == 0:  # That means that it the first day of that month
            total_days = 1

        return (current_month_data, total_days)

    def get_max_days_in_month(self, required_month: int = None) -> int:
        if required_month is None:
            required_month = self.month

        max_days = 0
        if required_month == 2:
                max_days = 29 if self.max_days_in_year == 366 else 28
        else:
            max_days = 30 if required_month % 2 == 0 and required_month not in (4, 12) else 31
        
        return max_days

    @property
    def month(self):
        return self.__month_data.month

    @property
    def max_days_in_year(self):
        return self.__month_data.max_days_in_year
