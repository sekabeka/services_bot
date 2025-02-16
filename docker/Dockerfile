FROM python:3.12-slim

WORKDIR /app

COPY ../requirements.txt .

RUN pip install --no-cache-dir --default-timeout=10 -r requirements.txt

COPY .. .

CMD ["python", "app.py"]