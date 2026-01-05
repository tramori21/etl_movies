# ETL Movies (PostgreSQL → Elasticsearch)

Учебный ETL-проект для загрузки данных о фильмах из PostgreSQL в Elasticsearch.

Проект сделан так, чтобы **запускаться с нуля одной командой** и быть
полностью воспроизводимым (как для ревьюера, так и для локальной проверки).

---

## Стек

- Python 3.10  
- PostgreSQL 16  
- Elasticsearch 7.17  
- Docker / Docker Compose  

---

## Как устроен проект

- PostgreSQL поднимается **уже с данными** (через `dump.sql`)
- ETL-сервис:
  - ждёт, пока поднимется Postgres
  - ждёт, пока поднимется Elasticsearch
  - автоматически создаёт индекс в Elasticsearch
  - загружает данные инкрементально
- Состояние ETL хранится в `data/state.json`

---

## Быстрый старт (как у ревьюера)

### 1. Клонировать репозиторий

```powershell
git clone https://github.com/tramori21/etl_movies
cd etl_movies
```

### 2. Подготовить переменные окружения

```powershell
Copy-Item .\.env.example .\.env
```

(значения подходят для локального запуска, менять ничего не нужно)

### 3. Запустить проект

```powershell
docker compose up -d --build
```

---

## Проверка, что всё работает

### Статус контейнеров

```powershell
docker compose ps
```

Все сервисы должны быть в статусе `Up`.

---

### Логи ETL

```powershell
docker compose logs -f etl
```

Ожидаемый вывод при первом запуске:

```
ETL started
Postgres is ready
Elasticsearch is ready
Loaded 999 movies
```

Дальше:

```
No new movies
```

---

### Проверка PostgreSQL

```powershell
docker compose exec postgres psql -U app -d movies_database -c "\dt content.*"
```

Ожидаемые таблицы:

- content.film_work  
- content.genre  
- content.genre_film_work  
- content.person  
- content.person_film_work  

---

### Проверка Elasticsearch

```powershell
Invoke-RestMethod http://127.0.0.1:9200/_cat/indices?v
Invoke-RestMethod http://127.0.0.1:9200/movies/_count?pretty
```

Ожидаемо:

- индекс `movies` существует
- количество документов: **999**
- статус `yellow` — это нормально для single-node Elasticsearch

---

## Инкрементальная загрузка

ETL загружает данные инкрементально по полю `modified`.

Состояние хранится в файле:

```
data/state.json
```

При повторном запуске:
- новые данные догружаются
- существующие документы не дублируются

---

## Примечания

- `dump.sql` применяется **только при первом запуске** (когда volume пустой)
- для переинициализации БД:
  ```powershell
  docker compose down -v
  docker compose up -d --build
  ```
- `.env` не хранится в репозитории
- `.env.example` используется как шаблон

---

## Структура проекта (кратко)

```
.
├── docker-compose.yml
├── Dockerfile
├── dump.sql
├── .env.example
├── src/
│   └── etl/
│       ├── main.py
│       ├── settings.py
│       ├── pg/
│       ├── es/
│       └── state/
├── data/
│   └── state.json
└── README.md
```
