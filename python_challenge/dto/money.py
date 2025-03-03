from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Money:
    amount: Decimal
    currency: str

    def __init__(self, amount: Decimal, currency: str):
        self.amount = amount
        self.currency = currency

    def to_dict(self) -> dict:
        return {
            'amount': float(self.amount),
            'currency': self.currency
        }
