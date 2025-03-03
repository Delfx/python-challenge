from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

@dataclass
class CurrencyRate:
    base_currency: Optional[str] = None
    rate: Optional[Decimal] = None
    target_currency: Optional[str] = None

    def __init__(self, base_currency: Optional[str] = None, rate: Optional[Decimal] = None, target_currency: Optional[str] = None):
        self.base_currency = base_currency
        self.rate = rate
        self.target_currency = target_currency

    def to_dict(self) -> dict:
        return {
            'base_currency': self.base_currency,
            'rate': float(self.rate),
            'target_currency': self.target_currency
        }
