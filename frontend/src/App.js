import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import SearchForm from './components/SearchForm';
import ResultCard from './components/ResultCard';
import LoadingSpinner from './components/LoadingSpinner';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (fromCity, toCity) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/search`, {
        from: fromCity,
        to: toCity
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Error fetching prediction. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>✈️ Smart Booking Predictor</h1>
          <p>Find the best day to book your flight</p>
        </header>

        <SearchForm onSearch={handleSearch} disabled={loading} />

        {loading && <LoadingSpinner />}
        {error && <div className="error-message">❌ {error}</div>}
        {result && <ResultCard result={result} />}
      </div>
    </div>
  );
}

export default App;
