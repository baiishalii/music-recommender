import requests
import base64
import os
from datetime import datetime, timedelta

class SpotifyClient:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.access_token = None
        self.token_expiry = None
        
    def get_access_token(self):
        if self.access_token and datetime.now() < self.token_expiry:
            return self.access_token
            
        auth_url = 'https://accounts.spotify.com/api/token'
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {'Authorization': f'Basic {auth_header}'}
        data = {'grant_type': 'client_credentials'}
        
        response = requests.post(auth_url, headers=headers, data=data)
        response_data = response.json()
        
        self.access_token = response_data['access_token']
        self.token_expiry = datetime.now() + timedelta(seconds=response_data['expires_in'])
        return self.access_token
    
    def search_tracks(self, query):
        token = self.get_access_token()
        headers = {'Authorization': f'Bearer {token}'}
        url = f'https://api.spotify.com/v1/search?q={query}&type=track&limit=10'
        
        response = requests.get(url, headers=headers)
        return response.json()
    
    def get_audio_features(self, track_id):
        token = self.get_access_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        # Get track details
        track_url = f'https://api.spotify.com/v1/tracks/{track_id}'
        track_response = requests.get(track_url, headers=headers)
        track_data = track_response.json()
        
        # Get audio features
        features_url = f'https://api.spotify.com/v1/audio-features/{track_id}'
        features_response = requests.get(features_url, headers=headers)
        features_data = features_response.json()
        
        # Combine data
        combined_data = {
            'id': track_id,
            'name': track_data['name'],
            'artist': track_data['artists'][0]['name'],
            'album': track_data['album']['name'],
            'popularity': track_data['popularity'],
            'preview_url': track_data['preview_url'],
            'image_url': track_data['album']['images'][0]['url'] if track_data['album']['images'] else None,
            **features_data
        }
        
        return combined_data
