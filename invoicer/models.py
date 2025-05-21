from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class DateRange:
    start: date
    end: date


@dataclass
class LineItem:
    client: str
    hours: float
    description: str
    total: str


@dataclass
class Invoice:
    date: str
    start_date: str
    end_date: str
    rate: str
    terms: str
    due: str
    total: str
    line_items: List[LineItem]
