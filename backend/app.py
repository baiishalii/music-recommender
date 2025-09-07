from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from spotify_client import SpotifyClient
from recommendation_engine import RecommendationEngine
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

# Initialize Spotify client and recommendation engine
spotify_client = SpotifyClient()
recommender = RecommendationEngine()

@app.route('/api/search', methods=['GET'])
def search_tracks():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    results = spotify_client.search_tracks(query)
    return jsonify(results)

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    track_id = data.get('track_id')
    
    # Get track features
    track_features = spotify_client.get_audio_features(track_id)
    
    # Get recommendations
    recommendations = recommender.get_recommendations(track_features)
    
    # Store search in database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_searches (track_id) VALUES (%s)",
        (track_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify(recommendations)

@app.route('/api/analysis', methods=['GET'])
def get_analysis():
    # Get data for visualization
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM tracks", conn)
    conn.close()
    
    # Generate analysis visualizations
    analysis_data = recommender.generate_visualizations(df)
    
    return jsonify(analysis_data)

if __name__ == '__main__':
    app.run(debug=True)
