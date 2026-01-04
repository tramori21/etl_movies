CREATE SCHEMA IF NOT EXISTS content;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================
-- Таблицы-справочники
-- =========================

CREATE TABLE IF NOT EXISTS content.genre (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.person (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========================
-- Таблица фильмов
-- =========================

CREATE TABLE IF NOT EXISTS content.film_work (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========================
-- Таблицы связей
-- =========================

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    film_work_id UUID NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
    genre_id UUID NOT NULL REFERENCES content.genre(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS genre_film_work_unique
ON content.genre_film_work (film_work_id, genre_id);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    film_work_id UUID NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
    person_id UUID NOT NULL REFERENCES content.person(id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS person_film_work_unique
ON content.person_film_work (film_work_id, person_id, role);

-- =========================
-- Индексы updated_at
-- =========================

CREATE INDEX IF NOT EXISTS film_work_updated_at_idx
ON content.film_work(updated_at);

CREATE INDEX IF NOT EXISTS genre_updated_at_idx
ON content.genre(updated_at);

CREATE INDEX IF NOT EXISTS person_updated_at_idx
ON content.person(updated_at);

-- =========================
-- Тестовые данные
-- =========================

INSERT INTO content.genre (id, name, description, created_at, updated_at)
VALUES
('11111111-1111-1111-1111-111111111111', 'Drama', 'Dramatic genre', NOW(), NOW()),
('22222222-2222-2222-2222-222222222222', 'Comedy', 'Comedy genre', NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

INSERT INTO content.person (id, full_name, created_at, updated_at)
VALUES
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'John Director', NOW(), NOW()),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'Alice Actor', NOW(), NOW()),
('cccccccc-cccc-cccc-cccc-cccccccccccc', 'Bob Writer', NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

INSERT INTO content.film_work (
    id, title, description, creation_date, rating, type, created_at, updated_at
)
VALUES
(
    '99999999-9999-9999-9999-999999999999',
    'Test Movie',
    'A movie for ETL test',
    '2020-01-01',
    8.7,
    'movie',
    NOW(),
    NOW()
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO content.genre_film_work (film_work_id, genre_id, created_at)
VALUES
('99999999-9999-9999-9999-999999999999', '11111111-1111-1111-1111-111111111111', NOW()),
('99999999-9999-9999-9999-999999999999', '22222222-2222-2222-2222-222222222222', NOW())
ON CONFLICT DO NOTHING;

INSERT INTO content.person_film_work (film_work_id, person_id, role, created_at)
VALUES
('99999999-9999-9999-9999-999999999999', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'director', NOW()),
('99999999-9999-9999-9999-999999999999', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'actor', NOW()),
('99999999-9999-9999-9999-999999999999', 'cccccccc-cccc-cccc-cccc-cccccccccccc', 'writer', NOW())
ON CONFLICT DO NOTHING;
