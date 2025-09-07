import React, { useState } from 'react';
import axios from 'axios';

const Search = ({ onTrackSelect }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const searchTracks = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:5000/api/search?q=${query}`);
      setResults(response.data.tracks.items);
    } catch (error) {
      console.error('Error searching tracks:', error);
    }
    setLoading(false);
  };

  return (
    <div className="search-container">
      <h2>Search for a Song</h2>
      <div className="search-box">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter song or artist name"
        />
        <button onClick={searchTracks} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>
      
      <div className="search-results">
        {results.map(track => (
          <div key={track.id} className="track-item" onClick={() => onTrackSelect(track)}>
            <img src={track.album.images[0]?.url} alt={track.album.name} />
            <div className="track-info">
              <h4>{track.name}</h4>
              <p>{track.artists[0].name}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Search;
