"""Interface related to communicate with day dataclass."""

from data_objects import DayData


class DayInterface:
    def __init__(self, day_data: DayData):
        self.__day_data = day_data

    @property
    def day(self):
        return self.__day_data.day
