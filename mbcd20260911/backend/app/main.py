"""Точка входа FastAPI: подключение роутеров каталога, заказов, пользователей, оплаты, админки."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import admin, catalog, orders, payments, users

app = FastAPI(title="Дом цветов — API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: сузить до домена mini app в проде (тот же URL, что указан в настройках бота на MAX для партнёров)
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(catalog.router, prefix="/catalog", tags=["catalog"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
