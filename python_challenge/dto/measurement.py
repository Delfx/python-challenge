from dataclasses import dataclass
from decimal import Decimal
import re

@dataclass
class Measurement:
    value: Decimal
    unit: str

    def __init__(self, value: float, unit: str):
        self.value = value
        self.unit = unit

    def to_dict(self) -> dict:
        return {
            'value': float(self.value),
            'unit': self.unit
        }
