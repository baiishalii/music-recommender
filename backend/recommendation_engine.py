import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
import mysql.connector
import os

class RecommendationEngine:
    def __init__(self):
        self.feature_columns = [
            'danceability', 'energy', 'key', 'loudness', 'mode', 
            'speechiness', 'acousticness', 'instrumentalness', 
            'liveness', 'valence', 'tempo'
        ]
        self.scaler = StandardScaler()
        
    def get_db_tracks(self):
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        
        df = pd.read_sql("SELECT * FROM tracks", conn)
        conn.close()
        return df
    
    def get_recommendations(self, track_features, n_recommendations=5):
        # Get tracks from database
        df = self.get_db_tracks()
        
        if df.empty:
            return {"recommendations": [], "message": "No tracks in database"}
        
        # Prepare the input track features
        input_features = pd.DataFrame([[
            track_features['danceability'],
            track_features['energy'],
            track_features['key'],
            track_features['loudness'],
            track_features['mode'],
            track_features['speechiness'],
            track_features['acousticness'],
            track_features['instrumentalness'],
            track_features['liveness'],
            track_features['valence'],
            track_features['tempo']
        ]], columns=self.feature_columns)
        
        # Scale features
        db_features = df[self.feature_columns]
        all_features = pd.concat([db_features, input_features], ignore_index=True)
        scaled_features = self.scaler.fit_transform(all_features)
        
        # Split back into db and input features
        db_scaled = scaled_features[:-1, :]
        input_scaled = scaled_features[-1, :].reshape(1, -1)
        
        # Calculate similarity
        similarities = cosine_similarity(input_scaled, db_scaled).flatten()
        
        # Get top recommendations
        top_indices = similarities.argsort()[-n_recommendations:][::-1]
        recommendations = df.iloc[top_indices].to_dict('records')
        
        # Add similarity score to each recommendation
        for i, idx in enumerate(top_indices):
            recommendations[i]['similarity_score'] = float(similarities[idx])
        
        return {
            "input_track": {
                "name": track_features['name'],
                "artist": track_features['artist'],
                "image_url": track_features['image_url']
            },
            "recommendations": recommendations
        }
    
    def generate_visualizations(self, df):
        if df.empty:
            return {"error": "No data available for visualization"}
        
        # Create feature distribution plot
        plt.figure(figsize=(12, 8))
        numeric_features = df.select_dtypes(include=['float64', 'int64']).columns
        numeric_features = [f for f in numeric_features if f in self.feature_columns]
        
        df[numeric_features].hist(bins=15, figsize=(15, 10))
        plt.suptitle('Distribution of Audio Features')
        plt.tight_layout()
        
        # Save plot to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        distribution_plot = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        # Create correlation heatmap
        plt.figure(figsize=(10, 8))
        correlation_matrix = df[numeric_features].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Audio Features Correlation Heatmap')
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        correlation_plot = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return {
            "distribution_plot": distribution_plot,
            "correlation_plot": correlation_plot,
            "stats": df[numeric_features].describe().to_dict()
        }
