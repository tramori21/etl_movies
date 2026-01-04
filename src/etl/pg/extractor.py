import psycopg
from psycopg.rows import dict_row


class PostgresExtractor:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def fetch_movies(self, modified_after):
        query = """
        SELECT
            fw.id,
            fw.title,
            fw.description,
            fw.rating,
            fw.modified,

            ARRAY_AGG(DISTINCT g.name) AS genres,

            ARRAY_AGG(DISTINCT CASE WHEN pfw.role = 'director' THEN p.full_name END)
                FILTER (WHERE pfw.role = 'director') AS directors_names,
            ARRAY_AGG(DISTINCT CASE WHEN pfw.role = 'actor' THEN p.full_name END)
                FILTER (WHERE pfw.role = 'actor') AS actors_names,
            ARRAY_AGG(DISTINCT CASE WHEN pfw.role = 'writer' THEN p.full_name END)
                FILTER (WHERE pfw.role = 'writer') AS writers_names,

            COALESCE(
                ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
                    FILTER (WHERE pfw.role = 'director'),
                ARRAY[]::jsonb[]
            ) AS directors,

            COALESCE(
                ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
                    FILTER (WHERE pfw.role = 'actor'),
                ARRAY[]::jsonb[]
            ) AS actors,

            COALESCE(
                ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
                    FILTER (WHERE pfw.role = 'writer'),
                ARRAY[]::jsonb[]
            ) AS writers

        FROM content.film_work fw
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id

        WHERE fw.modified > %s
        GROUP BY fw.id
        ORDER BY fw.modified;
        """

        with psycopg.connect(self.dsn) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, (modified_after,))
                return cur.fetchall()
