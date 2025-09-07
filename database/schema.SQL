CREATE DATABASE music_recommender;
USE music_recommender;

CREATE TABLE tracks (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    artist VARCHAR(255),
    album VARCHAR(255),
    popularity INT,
    danceability FLOAT,
    energy FLOAT,
    key INT,
    loudness FLOAT,
    mode INT,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    tempo FLOAT,
    duration_ms INT,
    time_signature INT,
    preview_url VARCHAR(255),
    image_url VARCHAR(255)
);

CREATE TABLE user_searches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    track_id VARCHAR(255),
    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (track_id) REFERENCES tracks(id)
);
