-- ============================================================
-- Jeu de données de test pour la BDD Backlog de jeux vidéo
-- ============================================================
--
-- À exécuter APRÈS que Flask ait créé les tables (via db.create_all()).
--
-- Pour charger les données :
--   docker compose cp init.sql db:/tmp/init.sql
--   docker compose exec db psql -U user_backlog -d backlog_jeux -f /tmp/init.sql
-- ============================================================


-- ============================================================
-- USERS
-- ============================================================
INSERT INTO users (email, username, created_at) VALUES
    ('alice@test.com', 'alice_gamer', NOW()),
    ('bob@test.com', 'bob_player', NOW()),
    ('karim@test.com', 'karim47', NOW())
ON CONFLICT DO NOTHING;


-- ============================================================
-- PROFILES (relation One-to-One avec User)
-- ============================================================
INSERT INTO profiles (user_id, favorite_platform, bio) VALUES
    (1, 'PC', 'Fan de jeux indés et de metroidvanias'),
    (2, 'PS5', 'Joueur de RPG depuis 15 ans'),
    (3, 'Switch', 'Jeux en coop avec les potes')
ON CONFLICT DO NOTHING;


-- ============================================================
-- GAMES
-- ============================================================
INSERT INTO games (title, developer, release_year) VALUES
    ('Hollow Knight', 'Team Cherry', 2017),
    ('Elden Ring', 'FromSoftware', 2022),
    ('Stardew Valley', 'ConcernedApe', 2016),
    ('Hades', 'Supergiant Games', 2020),
    ('Celeste', 'Maddy Makes Games', 2018),
    ('The Witcher 3', 'CD Projekt Red', 2015)
ON CONFLICT DO NOTHING;


-- ============================================================
-- TAGS
-- ============================================================
INSERT INTO tags (name) VALUES
    ('Indie'),
    ('RPG'),
    ('Metroidvania'),
    ('Rogue-like'),
    ('Soulslike'),
    ('Platformer'),
    ('Open World')
ON CONFLICT DO NOTHING;


-- ============================================================
-- GAME_TAGS (relation Many-to-Many entre Game et Tag)
-- ============================================================
INSERT INTO game_tags (game_id, tag_id) VALUES
    (1, 1), (1, 3),           -- Hollow Knight : Indie, Metroidvania
    (2, 2), (2, 5), (2, 7),   -- Elden Ring : RPG, Soulslike, Open World
    (3, 1),                    -- Stardew Valley : Indie
    (4, 1), (4, 4),           -- Hades : Indie, Rogue-like
    (5, 1), (5, 6),           -- Celeste : Indie, Platformer
    (6, 2), (6, 7)             -- The Witcher 3 : RPG, Open World
ON CONFLICT DO NOTHING;


-- ============================================================
-- BACKLOG_ENTRIES (relation One-to-Many)
-- ============================================================
INSERT INTO backlog_entries (user_id, game_id, status, rating, review, added_at) VALUES
    (1, 1, 'finished', 10, 'Chef-d''oeuvre absolu, l''ambiance est incroyable', NOW()),
    (1, 4, 'playing', 9, 'Très addictif', NOW()),
    (1, 5, 'to_play', NULL, NULL, NOW()),
    (2, 2, 'finished', 10, 'Meilleur jeu de la décennie selon moi', NOW()),
    (2, 6, 'playing', 9, 'Histoire captivante', NOW()),
    (3, 3, 'playing', 8, 'Parfait pour se détendre', NOW()),
    (3, 4, 'to_play', NULL, NULL, NOW())
ON CONFLICT DO NOTHING;