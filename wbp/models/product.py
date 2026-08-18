from dataclasses import dataclass


@dataclass
class Product:

    parse_date: str

    url: str

    sku: int

    title: str

    brand: str

    supplier: str

    sku_rating: float

    sku_reviews_count: int

    price_old: float

    price: float


    def to_dict(self):

        return {

            "Дата парсинга": self.parse_date,

            "URL": self.url,

            "SKU": self.sku,

            "Название": self.title,

            "Бренд": self.brand,

            "Продавец": self.supplier,

            "Рейтинг карточки": self.sku_rating,

            "Кол-во отзывов карточки": self.sku_reviews_count,

            "Цена без скидки": self.price_old,

            "Цена со скидкой": self.price

        }