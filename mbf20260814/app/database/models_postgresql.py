from datetime import datetime, date

from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.connect_postgresql import Base



# ==================================================
# USERS
# ==================================================

class User(Base):

    __tablename__ = "users"


    id: Mapped[int] = mapped_column(

        primary_key=True,

        autoincrement=True,

    )


    max_user_id: Mapped[int] = mapped_column(

        BigInteger,

        unique=True,

        nullable=False,

        index=True,

    )


    first_name: Mapped[str | None] = mapped_column(

        String(255),

        nullable=True,

    )


    last_name: Mapped[str | None] = mapped_column(

        String(255),

        nullable=True,

    )


    username: Mapped[str | None] = mapped_column(

        String(255),

        nullable=True,

    )


    created_at: Mapped[datetime] = mapped_column(

        DateTime,

        default=datetime.utcnow,

        nullable=False,

    )


    updated_at: Mapped[datetime] = mapped_column(

        DateTime,

        default=datetime.utcnow,

        onupdate=datetime.utcnow,

        nullable=False,

    )


    def __repr__(self):

        return (

            f"User("

            f"id={self.id}, "

            f"max_user_id={self.max_user_id}, "

            f"username={self.username}"

            f")"

        )



# ==================================================
# PORTFOLIO
# ==================================================

class Portfolio(Base):

    __tablename__ = "portfolio"


    id: Mapped[int] = mapped_column(

        primary_key=True,

        autoincrement=True,

    )


    # пользователь MAX

    user_id: Mapped[int] = mapped_column(

        BigInteger,

        nullable=False,

        index=True,

    )


    # тикер акции

    ticker: Mapped[str] = mapped_column(

        String(20),

        nullable=False,

        index=True,

    )


    # количество акций

    quantity: Mapped[float] = mapped_column(

        Float,

        nullable=False,

    )


    # цена покупки

    buy_price: Mapped[float] = mapped_column(

        Float,

        nullable=False,

    )


    # дата покупки

    buy_date: Mapped[date] = mapped_column(

        Date,

        nullable=False,

    )


    created_at: Mapped[datetime] = mapped_column(

        DateTime,

        default=datetime.utcnow,

        nullable=False,

    )


    def __repr__(self):

        return (

            f"Portfolio("

            f"id={self.id}, "

            f"user_id={self.user_id}, "

            f"ticker={self.ticker}, "

            f"quantity={self.quantity}, "

            f"buy_price={self.buy_price}"

            f")"

        )

# ==================================================
# PORTFOLIO HISTORY
# ==================================================

class PortfolioHistory(Base):

    __tablename__ = "portfolio_history"


    id: Mapped[int] = mapped_column(

        primary_key=True,

        autoincrement=True,

    )


    # пользователь MAX

    user_id: Mapped[int] = mapped_column(

        BigInteger,

        nullable=False,

        index=True,

    )


    # тикер акции

    ticker: Mapped[str] = mapped_column(

        String(20),

        nullable=False,

        index=True,

    )


    # сколько продали

    quantity: Mapped[float] = mapped_column(

        Float,

        nullable=False,

    )


    # средняя цена покупки

    buy_price: Mapped[float] = mapped_column(

        Float,

        nullable=False,

    )


    # цена продажи

    sell_price: Mapped[float] = mapped_column(

        Float,

        nullable=False,

    )


    # сумма покупки

    buy_total: Mapped[float] = mapped_column(

        Float,

        nullable=False,

    )


    # сумма продажи

    sell_total: Mapped[float] = mapped_column(

        Float,

        nullable=False,

    )


    # прибыль / убыток

    profit: Mapped[float] = mapped_column(

        Float,

        nullable=False,

    )


    # процент доходности

    percent: Mapped[float] = mapped_column(

        Float,

        nullable=False,

    )


    # дата продажи

    sell_date: Mapped[date] = mapped_column(

        Date,

        nullable=False,

    )


    created_at: Mapped[datetime] = mapped_column(

        DateTime,

        default=datetime.utcnow,

        nullable=False,

    )


    def __repr__(self):

        return (

            f"PortfolioHistory("

            f"id={self.id}, "

            f"user_id={self.user_id}, "

            f"ticker={self.ticker}, "

            f"quantity={self.quantity}, "

            f"profit={self.profit}"

            f")"

        )
    
# ==================================================
# PRICE ALERTS
# ==================================================

class PriceAlert(Base):

    __tablename__ = "price_alerts"


    id: Mapped[int] = mapped_column(

        primary_key=True,

        autoincrement=True,

    )


    # пользователь MAX

    user_id: Mapped[int] = mapped_column(

        BigInteger,

        nullable=False,

        index=True,

    )


    # тикер

    ticker: Mapped[str] = mapped_column(

        String(20),

        nullable=False,

        index=True,

    )


    # цена уведомления

    target_price: Mapped[float] = mapped_column(

        Float,

        nullable=False,

    )


    # условие

    # выше / ниже

    condition: Mapped[str] = mapped_column(

        String(10),

        nullable=False,

    )


    # отправлено ли уведомление

    is_active: Mapped[bool] = mapped_column(

        default=True,

        nullable=False,

    )


    created_at: Mapped[datetime] = mapped_column(

        DateTime,

        default=datetime.utcnow,

        nullable=False,

    )


    def __repr__(self):

        return (

            f"PriceAlert("

            f"id={self.id}, "

            f"user_id={self.user_id}, "

            f"ticker={self.ticker}, "

            f"target_price={self.target_price}, "

            f"condition={self.condition}"

            f")"

        )