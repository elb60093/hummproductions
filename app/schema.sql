-- Drop tables in correct dependency order
DROP TABLE IF EXISTS podcasts;
DROP TABLE IF EXISTS videos;

-- Videos table
CREATE TABLE videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    youtube_id TEXT NOT NULL UNIQUE,
    description TEXT
);

-- Podcasts table
CREATE TABLE podcasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id INTEGER NOT NULL,
    platform TEXT NOT NULL,
    episode_id TEXT NOT NULL,
    FOREIGN KEY (video_id) REFERENCES videos (id) ON DELETE CASCADE
);
