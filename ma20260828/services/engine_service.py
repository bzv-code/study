from client.moex_client import MoexClient
from models.engine_model import EngineModel
from utils.iss_parser import IssParser


class EngineService:

    def __init__(
        self,
        client: MoexClient,
    ):

        self.client = client

    def get_all(
        self,
    ) -> list[EngineModel]:

        response = self.client.get_engines()

        engines = IssParser.table(
            response,
            "engines",
        )

        return [

            EngineModel(
                name=item["name"],
                title=item["title"],
            )

            for item in engines
        ]