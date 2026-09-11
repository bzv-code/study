FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bot_app ./bot_app
CMD ["python", "-m", "bot_app.main"]
