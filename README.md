# Music Recommendation System

A full-stack web application that provides music recommendations based on audio features using the Spotify API.

## Features

- Search for songs and artists
- Get recommendations based on audio features
- Listen to song previews
- View data visualizations of music features

## Tech Stack

- Frontend: React.js
- Backend: Flask (Python)
- Database: MySQL
- Data Analysis: Pandas, Scikit-learn, Matplotlib, Seaborn
- API: Spotify Web API

## Setup Instructions

1. Clone the repository
2. Set up MySQL database using schema.sql
3. Configure environment variables in backend/.env
4. Install backend dependencies: `pip install -r requirements.txt`
5. Install frontend dependencies: `npm install`
6. Populate the database: `python populate_database.py`
7. Start backend: `python app.py`
8. Start frontend: `npm start`

## API Endpoints

- GET /api/search?q={query} - Search for tracks
- POST /api/recommendations - Get recommendations for a track
- GET /api/analysis - Get data visualizations
