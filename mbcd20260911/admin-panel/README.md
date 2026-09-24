# admin-panel — админ-панель каталога «Дом цветов»

Веб-панель для менеджера: **вход по логину и паролю** + управление товарами каталога —
можно **менять картинки** (загрузкой файла или URL), **стоимость**, название/описание,
скрывать товары, а также **добавлять и удалять** товары.

## Структура

```
admin-panel/
├── server/          # backend на FastAPI (Python)
│   ├── main.py      # приложение: /api/login, /api/products, /api/upload + статика веб-интерфейса
│   ├── models.py    # SQLAlchemy: Product (поля совпадают с Bouquet из основного backend), LoginAttempt
│   ├── config.py    # учётные данные, секрет JWT, лимиты загрузок
│   ├── requirements.txt
│   └── uploads/     # загруженные картинки (раздаются по /static/uploads/...)
└── web/             # фронтенд (vanilla JS, без сборки)
    ├── index.html   # экран входа + сетка товаров + модальное окно редактирования
    ├── app.js       # логика: fetch-API с Bearer-токеном, CRUD, загрузка файлов
    └── styles.css
```

## Запуск

```bash
cd admin-panel/server
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8010
```

Открыть: **http://localhost:8010**

Логин/пароль по умолчанию: `admin` / `admin123`
(переопределяются переменными окружения `ADMIN_USERNAME` / `ADMIN_PASSWORD`).

## Как это работает

- **Вход**: `POST /api/login` проверяет логин/пароль и выдаёт JWT (HS256, срок 12 ч).
  Все остальные API требуют заголовок `Authorization: Bearer <token>`.
  Есть защита от перебора: 5 неудачных попыток с одного IP → блокировка на 15 минут.
- **Токен** хранится в localStorage браузера; кнопка «Выйти» очищает его.
- **Хранилище**: SQLite (`server/admin_panel.db`) создаётся автоматически при первом
  запуске; при пустой таблице добавляются 3 демо-товара. Схема `Product` повторяет
  модель `Bouquet` из `backend/app/models/bouquet.py`, поэтому панель позже можно
  переключить на основную PostgreSQL-БД проекта, заменив engine/соединение.
- **Картинки**: загружаются через `POST /api/upload` (jpg/png/gif/webp до 5 МБ)
  в `server/uploads/` и раздаются как `/static/uploads/<файл>`; либо задаётся внешний URL.
- **CRUD товаров**: `GET/POST /api/products`, `PATCH/DELETE /api/products/{id}`.

## Безопасность (для прода)

- Задайте стабильный `ADMIN_SECRET_KEY` и свой `ADMIN_PASSWORD` в окружении.
- Размещайте панель за HTTPS (nginx) и ограничьте доступ по IP/домену.
