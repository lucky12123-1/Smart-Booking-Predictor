import React from 'react';
import './LoadingSpinner.css';

function LoadingSpinner() {
  return (
    <div className="loading-spinner">
      <div className="spinner"></div>
      <p>Finding the best day for you...</p>
    </div>
  );
}

export default LoadingSpinner;
