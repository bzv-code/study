from client.moex_client import MoexClient
from models.market_model import MarketModel
from utils.iss_parser import IssParser


class MarketService:

    def __init__(
        self,
        client: MoexClient,
    ):

        self.client = client

    def get_all(
        self,
        engine: str,
    ) -> list[MarketModel]:

        response = self.client.get_markets(
            engine
        )

        markets = IssParser.table(
            response,
            "markets",
        )

        return [

            MarketModel(
                engine=engine,
                name=item["NAME"],
                title=item["TITLE"],
            )

            for item in markets
        ]