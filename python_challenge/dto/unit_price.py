from dataclasses import dataclass
from decimal import Decimal

@dataclass
class UnitPrice:
    amount: Decimal
    currency: str
    unit: str

    def __init__(self, amount: Decimal, currency: str, unit: str):
        self.amount = amount
        self.currency = currency
        self.unit = unit

    def to_dict(self) -> dict:
        return {
            'amount': float(self.amount),
            'currency': self.currency,
            'unit': self.unit
        }
