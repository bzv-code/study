from pydantic import BaseModel


class EngineModel(BaseModel):

    name: str = ""

    title: str = ""