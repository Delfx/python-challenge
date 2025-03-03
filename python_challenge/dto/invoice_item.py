from dataclasses import dataclass
from datetime import date, time
from typing import Optional, Any, List
from decimal import Decimal
from .currency_rate import CurrencyRate
from .unit_price import UnitPrice
from .measurement import Measurement
from .money import Money

@dataclass
class InvoiceItemDTO:
    id: Optional[int] = None
    date: Optional[date] = None
    time: Optional[time] = None
    base: Optional[str] = None
    description: Optional[str] = None
    aircraft_registration: Optional[str] = None
    aircraft_type: Optional[str] = None
    flight_number: Optional[str] = None
    quantity_ambient: Optional[Measurement] = None
    quantity_delivered: Optional[Measurement] = None
    quantity_priced: Optional[Measurement] = None
    unit_price_dto: Optional[UnitPrice] = None
    primary_amount: Optional[Money] = None
    secondary_amount: Optional[Money] = None
    vat_rate: Optional[Decimal] = None
    vat_amount: Optional[Money] = None
    currency_rate: Optional[CurrencyRate] = None
    external_id: Optional[str] = None
    reference: Optional[str] = None
    extra_data: Optional[dict[str, Any]] = None
    child_items: List['InvoiceItemDTO'] = None
    maintenance: Optional[bool] = None

    def __init__(
        self,
        id: Optional[int] = None,
        date: Optional[date] = None,
        time: Optional[time] = None,
        base: Optional[str] = None,
        departure_base: Optional[str] = None,
        arrival_base: Optional[str] = None,
        description: Optional[str] = None,
        aircraft_registration: Optional[str] = None,
        aircraft_type: Optional[str] = None,
        flight_number: Optional[str] = None,
        quantity_ambient: Optional[Measurement] = None,
        quantity_delivered: Optional[Measurement] = None,
        quantity_priced: Optional[Measurement] = None,
        unit_price_dto: Optional[UnitPrice] = None,
        primary_amount: Optional[Money] = None,
        secondary_amount: Optional[Money] = None,
        vat_rate: Optional[Decimal] = None,
        vat_amount: Optional[Money] = None,
        currency_rate: Optional[CurrencyRate] = None,
        external_id: Optional[str] = None,
        reference: Optional[str] = None,
        extra_data: Optional[dict[str, Any]] = None,
        child_items: Optional[List['InvoiceItemDTO']] = None,
        maintenance: Optional[bool] = None
    ):
        self.id = id
        self.date = date
        self.time = time
        self.base = base
        self.departure_base = departure_base
        self.arrival_base = arrival_base
        self.description = description
        self.aircraft_registration = aircraft_registration
        self.aircraft_type = aircraft_type
        self.flight_number = flight_number
        self.external_id = external_id
        self.reference = reference
        self.quantity_ambient = quantity_ambient
        self.quantity_delivered = quantity_delivered
        self.quantity_priced = quantity_priced
        self.unit_price_dto = unit_price_dto
        self.primary_amount = primary_amount
        self.secondary_amount = secondary_amount
        self.vat_rate = vat_rate
        self.vat_amount = vat_amount
        self.currency_rate = currency_rate
        self.extra_data = extra_data
        self.child_items = child_items
        self.maintenance = maintenance
    def add_child(self, child: 'InvoiceItemDTO'):
        if self.child_items is None:
            self.child_items = []

        self.child_items.append(child)

    def to_dict(self) -> dict:
        """Convert the DTO to a dictionary for JSON serialization"""
        result = {}
        for field, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, date) or isinstance(value, time):
                    result[field] = value.isoformat()
                elif isinstance(value, Decimal):
                    result[field] = float(value)
                elif isinstance(value, list):
                    result[field] = [item.to_dict() for item in value]
                elif isinstance(value, CurrencyRate):
                    result[field] = value.to_dict()
                elif isinstance(value, UnitPrice):
                    result[field] = value.to_dict()
                elif isinstance(value, Money):
                    result[field] = value.to_dict()
                elif isinstance(value, Measurement):
                    result[field] = value.to_dict()
                else:
                    result[field] = value
        return result