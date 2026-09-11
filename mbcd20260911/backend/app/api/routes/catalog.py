"""Эндпоинты каталога: список категорий, список букетов, карточка букета."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.bouquet import Bouquet
from app.schemas.bouquet import BouquetOut

router = APIRouter()


@router.get("/categories", response_model=list[str])
async def list_categories(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Bouquet.category).distinct().order_by(Bouquet.category))
    return [row[0] for row in result.all()]


@router.get("/bouquets", response_model=list[BouquetOut])
async def list_bouquets(
    category: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    query = select(Bouquet)
    if category:
        query = query.where(Bouquet.category == category)
    query = query.order_by(Bouquet.id)

    result = await session.execute(query)
    return result.scalars().all()


@router.get("/bouquets/{bouquet_id}", response_model=BouquetOut)
async def get_bouquet(bouquet_id: int, session: AsyncSession = Depends(get_session)):
    bouquet = await session.get(Bouquet, bouquet_id)
    if bouquet is None:
        raise HTTPException(status_code=404, detail="Букет не найден")
    return bouquet
