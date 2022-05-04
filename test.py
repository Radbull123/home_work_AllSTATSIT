from calendar import month
import logging
import math

from dataclasses import dataclass, field
from typing import Optional, Tuple

logging.basicConfig(format='%(asctime)s |%(levelname)s| %(message)s', level=logging.DEBUG)

class DateValError(Exception):
    def __init__(self, date_name: str, min_value: int, actual_value: int, max_value: Optional[int] = None) -> None:
        message = f"Not correct value. {date_name} should be: "\
            f"{min_value} {'-' + str(max_value) if max_value is not None else ''}, got {actual_value}"
        super().__init__(message)


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


@dataclass
class MonthData:
    month: int
    max_days_in_year: int
    min_month: int = field(default=1)
    max_month: int = field(default=12, init=False, repr=True)

    def __post_init__(self):
        if self.month not in range(self.min_month, self.max_month + 1):
            raise DateValError(self.__class__.__name__, min_value=1, max_value=self.max_month, actual_value=self.month)


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
                days_count += 30 if current_month.month % 2 == 0 and current_month.month != 12 else 31
            
            current_month = MonthData(current_month.month - 1, min_month=0)

        return days_count

    def convert_days_to_month(self, total_days: int) -> Tuple[MonthData, int]:
        current_month_data = MonthData(1)
        max_days_in_month_2 = 28 if self.max_days_in_year == 365 else 29
        while total_days >= max_days_in_month_2:
            if current_month_data.month == 2:
               total_days -= max_days_in_month_2
            else:
                total_days -= 30 if current_month_data.month % 2 == 0 and current_month_data.month != 12 else 31

            current_month_data = MonthData(current_month_data.month + 1)
        
        if total_days <= 0:  # That means that it the first day of that month
            total_days = 1

        return current_month_data, total_days

    @property
    def month(self):
        return self.__month_data.month

    @property
    def max_days_in_year(self):
        return self.__month_data.max_days_in_year

    def get_max_days_in_month(self) -> int:
        max_days = 0
        if self.__month_data.month == 2:
                max_days = 29 if self.max_days_in_year == 366 else 28
        else:
            max_days = 30 if self.__month_data.month % 2 == 0 and self.__month_data.month != 12 else 31
        
        return max_days


class DayInterface:
    def __init__(self, day_data: DayData):
        self.__day_data = day_data

    @property
    def day(self):
        return self.__day_data.day


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
                total_days, self.month_interface.get_max_days_in_month(year_data.max_days_in_year)
            ),
            month_data,
            year_data,
        )

    def add_date(self, days: int) -> Tuple[int, ...]:
        sum_of_days = self.__convert_date_to_total_days() + int(days)
        day_data, month_data, year_data = self.__convert_total_days_to_date_data(sum_of_days)

        return day_data.day, month_data.month, year_data.year


if __name__ == "__main__":
    try:
        while True:
            while True:
                try:
                    date = input("Hello user. Enter the date as sample: 30.02.2000 (dd.mm.yyyy):\t")
                    DateController.validate_date(date)            
                except (TypeError, ValueError) as error:
                    logging.error(f"{error}.\n\t\t\tPlease, try again!")
                else:
                    break
            while True:
                days_to_add = input("Enter the quantity of days that should be added to date:\t")
                if days_to_add.isdigit():
                    break
                else:
                    logging.warning(
                        "The entered days are not in valid format, please,"
                        "try to write only numeric symbols (for e.g. 10)"
                    )

            splitted_date = date.split(".")
            date_controller = DateController(*splitted_date)
            date_data = date_controller.add_date(days_to_add)
            logging.info("RESULT: %s.%s.%s", *date_data)
    except KeyboardInterrupt:
        logging.info("\nExit from the program.")