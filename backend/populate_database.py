import mysql.connector
import os
from dotenv import load_dotenv
from spotify_client import SpotifyClient

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

def store_track(track_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if track already exists
    cursor.execute("SELECT id FROM tracks WHERE id = %s", (track_data['id'],))
    if cursor.fetchone():
        print(f"Track {track_data['name']} already exists in database")
        cursor.close()
        conn.close()
        return
    
    # Insert new track
    insert_query = """
    INSERT INTO tracks (
        id, name, artist, album, popularity, danceability, energy, 
        key, loudness, mode, speechiness, acousticness, instrumentalness, 
        liveness, valence, tempo, duration_ms, time_signature, preview_url, image_url
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor.execute(insert_query, (
        track_data['id'],
        track_data['name'],
        track_data['artist'],
        track_data['album'],
        track_data['popularity'],
        track_data['danceability'],
        track_data['energy'],
        track_data['key'],
        track_data['loudness'],
        track_data['mode'],
        track_data['speechiness'],
        track_data['acousticness'],
        track_data['instrumentalness'],
        track_data['liveness'],
        track_data['valence'],
        track_data['tempo'],
        track_data['duration_ms'],
        track_data['time_signature'],
        track_data['preview_url'],
        track_data['image_url']
    ))
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Stored track: {track_data['name']} by {track_data['artist']}")

def main():
    spotify = SpotifyClient()
    
    # Search for popular songs to populate the database
    search_queries = [
        "popular songs",
        "top hits",
        "billboard top 100",
        "rock classics",
        "jazz standards",
        "hip hop essentials",
        "electronic dance music",
        "indie folk",
        "R&B classics",
        "country hits"
    ]
    
    for query in search_queries:
        print(f"Searching for: {query}")
        results = spotify.search_tracks(query)
        
        if 'tracks' in results and 'items' in results['tracks']:
            for track in results['tracks']['items']:
                track_id = track['id']
                try:
                    track_features = spotify.get_audio_features(track_id)
                    store_track(track_features)
                except Exception as e:
                    print(f"Error processing track {track['name']}: {str(e)}")
    
    print("Database population completed!")

if __name__ == "__main__":
    main()
