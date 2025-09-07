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
    # Use Vercel's environment variables for database connection
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'music_recommender'),
        'port': os.getenv('DB_PORT', 3306)
    }
    
    # For Vercel, we might need to use a different approach
    # If no database is available, we'll use a fallback method
    try:
        return mysql.connector.connect(**db_config)
    except Exception as e:
        print(f"Database connection failed: {e}")
        # Return a mock connection object that will allow the app to run
        # but will use alternative data sources
        return None

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
    
    # Try to store search in database if available
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_searches (track_id) VALUES (%s)",
                (track_id,)
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Failed to store search: {e}")
    
    return jsonify(recommendations)

@app.route('/api/analysis', methods=['GET'])
def get_analysis():
    # Try to get data from database
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql("SELECT * FROM tracks", conn)
            conn.close()
            
            # Generate analysis visualizations
            analysis_data = recommender.generate_visualizations(df)
            return jsonify(analysis_data)
        except Exception as e:
            print(f"Database query failed: {e}")
    
    # Fallback: return sample data if database is not available
    return jsonify({
        "message": "Database not available, using sample data",
        "stats": {
            "danceability": {"mean": 0.65, "std": 0.15},
            "energy": {"mean": 0.70, "std": 0.18},
            "valence": {"mean": 0.60, "std": 0.20}
        }
    })

# This is needed for Vercel to recognize the app
if __name__ == '__main__':
    app.run(debug=True)
