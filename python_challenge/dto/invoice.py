from dataclasses import dataclass
from datetime import date
from typing import Optional, List
from decimal import Decimal
from .invoice_item import InvoiceItemDTO
from .currency_rate import CurrencyRate
from .money import Money
from .delivery_record import DeliveryRecord
from .local_date_range import LocalDateRange

@dataclass
class InvoiceDTO:
    supplier: Optional[str] = None
    date: Optional[date] = None
    due_date: Optional[date] = None
    period: Optional[LocalDateRange] = None
    number: Optional[str] = None
    primary_amount: Optional[Money] = None
    secondary_amount: Optional[Money] = None
    credit: Optional[bool] = None
    credited_invoice_number: Optional[str] = None

    currency_rate: Optional[CurrencyRate] = None
    items: Optional[List[InvoiceItemDTO]] = None
    aggregated_items: Optional[List[InvoiceItemDTO]] = None
    delivery_records: Optional[List[DeliveryRecord]] = None

    date_range_based_invoice: Optional[bool] = None

    def __post_init__(self):
        if self.items is None:
            self.items = []

        if self.aggregated_items is None:
            self.aggregated_items = []

    def add_item(self, item: InvoiceItemDTO) -> None:
        self.items.append(item)

    def add_aggregated_item(self, item: InvoiceItemDTO) -> None:
        self.aggregated_items.append(item)

    def add_delivery_record(self, delivery_record: DeliveryRecord):
        if self.delivery_records is None:
            self.delivery_records = []

        self.delivery_records.append(delivery_record)

    def to_dict(self) -> dict:
        """Convert the DTO to a dictionary for JSON serialization"""
        result = {}
        for field, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, date):
                    result[field] = value.isoformat()
                elif isinstance(value, Decimal):
                    result[field] = float(value)
                elif isinstance(value, list):
                    result[field] = [item.to_dict() for item in value]
                elif isinstance(value, CurrencyRate) or isinstance(value, LocalDateRange) or isinstance(value, DeliveryRecord) or isinstance(value, Money):
                    result[field] = value.to_dict()
                else:
                    result[field] = value
        return result
