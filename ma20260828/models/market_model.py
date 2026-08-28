from pydantic import BaseModel


class MarketModel(BaseModel):

    engine: str = ""

    name: str = ""

    title: str = ""