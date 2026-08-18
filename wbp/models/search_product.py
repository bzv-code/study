from dataclasses import dataclass
from datetime import datetime



@dataclass
class SearchProduct:


    parse_date: datetime


    title: str


    brand: str


    supplier: str


    sku: int


    sku_rating: float


    sku_reviews_count: int


    price_old: float


    price: float


    url: str


    shop_url: str | None = None