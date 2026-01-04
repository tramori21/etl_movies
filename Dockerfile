FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY scripts ./scripts

# Создаем runtime-папку под state/прочие файлы, даже если ее нет в репозитории
RUN mkdir -p /app/data

ENV PYTHONPATH=/app

CMD ["sleep", "infinity"]
