"""Space to store custom errors."""
from typing import Optional


class DateValError(Exception):
    """Error appeared when invalid date trying to be set."""

    def __init__(self, date_name: str, min_value: int, actual_value: int, max_value: Optional[int] = None) -> None:
        message = f"Not correct value. {date_name} should be: "\
            f"{min_value} {'-' + str(max_value) if max_value is not None else ''}, got {actual_value}"
        super().__init__(message)
