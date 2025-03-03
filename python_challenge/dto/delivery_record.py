from datetime import date
from typing import Optional
from dataclasses import dataclass
from .measurement import Measurement

@dataclass
class DeliveryRecord:
    id: str
    base: str
    date: date
    flight_number: str
    aircraft_registration: str
    quantity: Measurement
    product: Optional[str]

    def __init__(self, id: str, base: str, date: date, flight_number: str, aircraft_registration: str, quantity: Measurement, product: Optional[str] = None):
        self.id = id
        self.base = base
        self.date = date
        self.flight_number = flight_number
        self.aircraft_registration = aircraft_registration
        self.quantity = quantity
        self.product = product

    def to_dict(self) -> dict:
        result = {
            'id': self.id,
            'base': self.base,
            'date': self.date.isoformat(),
            'flight_number': self.flight_number,
            'aircraft_registration': self.aircraft_registration,
            'quantity': self.quantity.to_dict(),
        }

        if self.product:
            result['product'] = self.product

        return result
