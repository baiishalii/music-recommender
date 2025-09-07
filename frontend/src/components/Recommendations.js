import React from 'react';

const Recommendations = ({ data }) => {
  if (!data || !data.recommendations) return null;

  return (
    <div className="recommendations-container">
      <h2>Recommendations based on: {data.input_track.name} by {data.input_track.artist}</h2>
      
      <div className="recommendations-list">
        {data.recommendations.map(track => (
          <div key={track.id} className="recommendation-item">
            <img src={track.image_url} alt={track.album} />
            <div className="track-details">
              <h3>{track.name}</h3>
              <p>{track.artist}</p>
              <p>Album: {track.album}</p>
              <p>Similarity: {(track.similarity_score * 100).toFixed(1)}%</p>
              
              {track.preview_url && (
                <audio controls>
                  <source src={track.preview_url} type="audio/mpeg" />
                  Your browser does not support the audio element.
                </audio>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recommendations;
