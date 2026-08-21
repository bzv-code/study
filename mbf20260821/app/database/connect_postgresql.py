from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DATABASE}"
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def check_connection():

    print("=" * 50)
    print("POSTGRESQL")
    print("=" * 50)

    print(DATABASE_URL)

    try:

        with engine.connect() as conn:

            version = conn.execute(text("SELECT version()")).scalar()

            print("STATUS : OK")
            print(version)

    except Exception as e:

        print("STATUS : ERROR")
        print(e)


if __name__ == "__main__":
    check_connection()