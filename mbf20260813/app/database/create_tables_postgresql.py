from app.database.connect_postgresql import Base
from app.database.connect_postgresql import engine


# обязательно импортируем модели

from app.database.models_postgresql import (
    User,
    Portfolio,
    PortfolioHistory,
    PriceAlert
)



def create_tables():


    print("=" * 60)

    print(
        "CREATE POSTGRESQL TABLES"
    )

    print("=" * 60)



    Base.metadata.create_all(

        bind=engine

    )



    print(
        "SUCCESS"
    )



if __name__ == "__main__":

    create_tables()