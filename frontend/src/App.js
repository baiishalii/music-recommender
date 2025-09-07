import React, { useState } from 'react';
import axios from 'axios';
import Search from './components/Search';
import Recommendations from './components/Recommendations';
import Visualization from './components/Visualization';
import './App.css';

function App() {
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTrackSelect = async (track) => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/recommendations', {
        track_id: track.id
      });
      setRecommendations(response.data);
    } catch (error) {
      console.error('Error getting recommendations:', error);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Music Recommendation System</h1>
      </header>
      
      <main>
        <Search onTrackSelect={handleTrackSelect} />
        
        {loading && <div className="loading">Getting recommendations...</div>}
        
        {recommendations && (
          <Recommendations data={recommendations} />
        )}
        
        <Visualization />
      </main>
    </div>
  );
}

export default App;
