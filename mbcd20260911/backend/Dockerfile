FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY api_app ./api_app
COPY alembic ./alembic
COPY alembic.ini .
CMD ["uvicorn", "api_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
