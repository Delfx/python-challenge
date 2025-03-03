from datetime import date
from dataclasses import dataclass

@dataclass
class LocalDateRange:
    start: date
    end: date

    def __init__(self, start: date, end: date):
        self.start = start
        self.end = end

    def to_dict(self) -> dict:
        return f'{self.start.strftime("%Y-%m-%d")}/{self.end.strftime("%Y-%m-%d")}'
