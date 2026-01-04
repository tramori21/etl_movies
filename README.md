\# ETL Movies (PostgreSQL → Elasticsearch)



ETL-сервис для загрузки данных о фильмах из PostgreSQL в Elasticsearch.



Проект выполнен в рамках учебного задания (ETL + Elasticsearch).



---



\## Стек

\- Python 3.10

\- PostgreSQL 16

\- Elasticsearch 7.17

\- Docker / Docker Compose



---



\## Структура проекта



```

etl\_movies/

├── docker-compose.yml

├── scripts/

│   ├── init\_db.sql

│   ├── test\_extract.py

│   ├── test\_transform.py

│   └── test\_load.py

├── src/

│   └── etl/

│       ├── pg/

│       │   └── extractor.py

│       ├── transformer.py

│       ├── es/

│       │   ├── loader.py

│       │   ├── index\_manager.py

│       │   └── es\_schema.json

│       ├── state/

│       │   └── state.py

│       └── main.py

├── data/

│   └── state.json

└── README.md

```



---



\## Запуск проекта



\### 1. Поднять сервисы



```powershell

docker compose up -d

```



Проверить, что контейнеры запущены:



```powershell

docker compose ps

```



---



\### 2. Инициализация базы данных



Для локальной проверки можно использовать `init\_db.sql`:



```powershell

Get-Content .\\scripts\\init\_db.sql -Raw |

docker compose exec -T postgres psql -U app -d movies\_database

```



Проверка:



```powershell

docker compose exec -T postgres psql -U app -d movies\_database -c "SELECT COUNT(\*) FROM content.film\_work;"

```



---



\### 3. Запуск ETL



```powershell

docker compose exec etl python -m src.etl.main

```



Ожидаемый вывод при первом запуске:



```

Loaded: 999

```



При повторных запусках:



```

Loaded: 0

```



---



\## Проверка Elasticsearch



Количество документов:



```powershell

Invoke-RestMethod http://127.0.0.1:9200/movies/\_count

```



Ожидаемо:



```

count: 999

```



Проверка mapping:



```powershell

curl.exe http://127.0.0.1:9200/movies/\_mapping?pretty

```



---



\## Инкрементальная загрузка



ETL поддерживает инкрементальную загрузку по полю `modified`.



При изменении записи в PostgreSQL и повторном запуске ETL

в Elasticsearch догружаются только изменённые документы.



Состояние хранится в файле:



```

data/state.json

```



---



\## Postman



Для проверки API используется коллекция Postman из файла:



```

Тесты для работы

```



Коллекция проверяет:

\- количество документов

\- поиск по тексту

\- вложенные поля (actors / writers / directors)

\- агрегации по жанрам



---



\## Примечания



\- Индекс Elasticsearch создаётся автоматически при запуске ETL

\- Mapping строго соответствует `es\_schema.json`

\- `state.json` не хранится в репозитории





