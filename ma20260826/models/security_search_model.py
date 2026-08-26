from pydantic import BaseModel


class SecuritySearchModel(BaseModel):

    secid: str = ""

    shortname: str = ""

    board: str = ""

    engine: str = ""

    market: str = ""