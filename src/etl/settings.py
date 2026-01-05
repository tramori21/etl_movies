from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_dsn: str = "dbname=movies_database user=app password=app host=postgres port=5432"
    es_host: str = "http://elasticsearch:9200"

    index_name: str = "movies"
    state_path: str = "/app/data/state.json"
    state_key: str = "etl_state"

    class Config:
        env_prefix = "ETL_"


settings = Settings()
