import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Visualization = () => {
  const [analysisData, setAnalysisData] = useState(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/analysis');
        setAnalysisData(response.data);
      } catch (error) {
        console.error('Error fetching analysis:', error);
      }
    };

    fetchAnalysis();
  }, []);

  if (!analysisData) return <div>Loading analysis...</div>;

  // Prepare data for feature averages chart
  const featureAverages = [];
  if (analysisData.stats) {
    for (const [feature, stats] of Object.entries(analysisData.stats)) {
      if (typeof stats === 'object' && 'mean' in stats) {
        featureAverages.push({
          feature,
          average: stats.mean
        });
      }
    }
  }

  return (
    <div className="visualization-container">
      <h2>Music Analysis</h2>
      
      <div className="plots">
        <div className="plot">
          <h3>Feature Averages</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={featureAverages}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="feature" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="average" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        
        <div className="plot">
          <h3>Feature Distribution</h3>
          <img 
            src={`data:image/png;base64,${analysisData.distribution_plot}`} 
            alt="Feature Distribution" 
          />
        </div>
        
        <div className="plot">
          <h3>Feature Correlation</h3>
          <img 
            src={`data:image/png;base64,${analysisData.correlation_plot}`} 
            alt="Feature Correlation" 
          />
        </div>
      </div>
    </div>
  );
};

export default Visualization;
