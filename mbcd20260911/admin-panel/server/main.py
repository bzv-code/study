"""Сервер админ-панели «Дом цветов»: вход по логину/паролю + CRUD товаров (картинки, цены).

Запуск:  uvicorn main:app --port 8010   (из папки admin-panel/server)
Веб-интерфейс раздаётся этой же службой со страницы / (статика из ../web).
"""
import hashlib
import hmac
import json
import time
import uuid
from base64 import urlsafe_b64decode, urlsafe_b64encode
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from config import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    ALLOWED_IMAGE_EXTENSIONS,
    DATABASE_PATH,
    MAX_UPLOAD_SIZE,
    SECRET_KEY,
    TOKEN_TTL_MINUTES,
    UPLOADS_DIR,
)
from models import Base, LoginAttempt, Product
1
WEB_DIR = Path(__file__).resolve().parent.parent / "web"

engine = create_engine(f"sqlite:///{DATABASE_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SEED_PRODUCTS = [
    dict(title="Нежность", category="Классические", description="Розы, эвкалипт, крафт-упаковка.",
         price=3500, photo_url="https://picsum.photos/seed/flowers1/600/400"),
    dict(title="Солнечный день", category="Авторские", description="Жёлтые тюльпаны и мимоза.",
         price=2200, photo_url="https://picsum.photos/seed/flowers2/600/400"),
    dict(title="Лавандовый вечер", category="Премиум", description="Пионы, лаванда, атласная лента.",
         price=5900, photo_url="https://picsum.photos/seed/flowers3/600/400"),
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if db.scalar(select(Product).limit(1)) is None:
            db.add_all([Product(**p) for p in SEED_PRODUCTS])
            db.commit()
    yield


app = FastAPI(title="Дом цветов — админ-панель", lifespan=lifespan)
app.mount("/static/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")


# --------------------------------------------------------------------------- #
# Аутентификация: минимальный JWT (HS256) на hmac/hashlib без внешних зависимостей
# --------------------------------------------------------------------------- #
def _b64(data: bytes) -> str:
    return urlsafe_b64encode(data).rstrip(b"=").decode()


def _unb64(s: str) -> bytes:
    return urlsafe_b64decode(s + "=" * (-len(s) % 4))


def create_token(username: str) -> str:
    header = _b64(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    payload = _b64(json.dumps({
        "sub": username,
        "exp": int(time.time()) + TOKEN_TTL_MINUTES * 60,
        "jti": uuid.uuid4().hex,
    }).encode())
    signing_input = f"{header}.{payload}".encode()
    signature = _b64(hmac.new(SECRET_KEY.encode(), signing_input, hashlib.sha256).digest())
    return f"{header}.{payload}.{signature}"


def decode_token(token: str) -> dict | None:
    try:
        header, payload, signature = token.split(".")
        signing_input = f"{header}.{payload}".encode()
        expected = _b64(hmac.new(SECRET_KEY.encode(), signing_input, hashlib.sha256).digest())
        if not hmac.compare_digest(expected, signature):
            return None
        data = json.loads(_unb64(payload))
        if data.get("exp", 0) < time.time():
            return None
        return data
    except Exception:
        return None


def require_admin(request: Request) -> str:
    """Достаёт Bearer-токен из заголовка Authorization; 401 — если недействителен."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Требуется авторизация")
    data = decode_token(auth.removeprefix("Bearer ").strip())
    if data is None or data.get("sub") != ADMIN_USERNAME:
        raise HTTPException(status_code=401, detail="Сессия истекла, войдите заново")
    return data["sub"]


MAX_FAILED_LOGINS = 5      # попыток с одного IP за окно
LOCKOUT_WINDOW_MINUTES = 15


class LoginBody(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=200)


@app.post("/api/login")
def login(body: LoginBody, request: Request, db: Session = Depends(get_db)):
    ip = request.client.host if request.client else "unknown"
    window_start = datetime.now(timezone.utc) - timedelta(minutes=LOCKOUT_WINDOW_MINUTES)
    recent_fails = len(db.execute(
        select(LoginAttempt.id).where(LoginAttempt.ip == ip, LoginAttempt.at >= window_start)
    ).all())
    if recent_fails >= MAX_FAILED_LOGINS:
        raise HTTPException(status_code=429, detail="Слишком много неудачных попыток. Подождите 15 минут.")

    if body.username != ADMIN_USERNAME or body.password != ADMIN_PASSWORD:
        db.add(LoginAttempt(ip=ip))
        db.commit()
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    # успех — сбрасываем счётчик ошибок для этого IP
    for attempt in db.scalars(select(LoginAttempt).where(LoginAttempt.ip == ip)).all():
        db.delete(attempt)
    db.commit()
    return {"token": create_token(body.username), "username": body.username}


@app.get("/api/me")
def me(username: str = Depends(require_admin)):
    return {"username": username}


# --------------------------------------------------------------------------- #
# Товары: список / создание / изменение (цена, картинка, текст) / удаление
# --------------------------------------------------------------------------- #
class ProductIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    category: str = Field(default="", max_length=100)
    description: str = Field(default="", max_length=1000)
    price: int = Field(ge=0)
    photo_url: str = Field(default="", max_length=500)
    is_active: bool = True


class ProductPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    category: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    price: int | None = Field(default=None, ge=0)
    photo_url: str | None = Field(default=None, max_length=500)
    is_active: bool | None = None


@app.get("/api/products")
def list_products(db: Session = Depends(get_db), _: str = Depends(require_admin)):
    products = db.scalars(select(Product).order_by(Product.id)).all()
    return [p.to_dict() for p in products]


@app.post("/api/products", status_code=201)
def create_product(body: ProductIn, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    product = Product(**body.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product.to_dict()


@app.patch("/api/products/{product_id}")
def update_product(product_id: int, body: ProductPatch,
                   db: Session = Depends(get_db), _: str = Depends(require_admin)):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(product, field, int(value) if field == "is_active" and isinstance(value, bool) else value)
    db.commit()
    db.refresh(product)
    return product.to_dict()


@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    # удаляем загруженный файл картинки, если он лежал в наших uploads
    if product.photo_url.startswith("/static/uploads/"):
        stale = UPLOADS_DIR / Path(product.photo_url).name
        stale.unlink(missing_ok=True)
    db.delete(product)
    db.commit()
    return {"deleted": product_id}


@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...), _: str = Depends(require_admin)):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(status_code=400,
                            detail=f"Можно загружать только изображения: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}")
    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="Файл больше 5 МБ")
    safe_name = f"{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
    (UPLOADS_DIR / safe_name).write_bytes(content)
    return {"photo_url": f"/static/uploads/{safe_name}"}


# --------------------------------------------------------------------------- #
# Статика веб-интерфейса
# --------------------------------------------------------------------------- #
@app.get("/")
def index():
    return FileResponse(WEB_DIR / "index.html")


app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")
