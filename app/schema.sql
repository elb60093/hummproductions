DROP TABLE IF EXISTS videos;
DROP TABLE IF EXISTS podcasts;

CREATE TABLE videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    youtube_id TEXT NOT NULL,
    description TEXT
);

CREATE TABLE podcasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id INTEGER NOT NULL,
    platform TEXT NOT NULL,
    episode_id TEXT NOT NULL,
    FOREIGN KEY (video_id) REFERENCES videos (id)
);
