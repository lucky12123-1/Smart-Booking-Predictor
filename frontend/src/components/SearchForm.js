import React, { useState } from 'react';
import './SearchForm.css';

function SearchForm({ onSearch, disabled }) {
  const [fromCity, setFromCity] = useState('');
  const [toCity, setToCity] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (fromCity.trim() && toCity.trim()) {
      onSearch(fromCity, toCity);
    }
  };

  const handleSwap = () => {
    const temp = fromCity;
    setFromCity(toCity);
    setToCity(temp);
  };

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="from">From</label>
        <input
          id="from"
          type="text"
          placeholder="e.g., BOM"
          value={fromCity}
          onChange={(e) => setFromCity(e.target.value.toUpperCase())}
          disabled={disabled}
          maxLength="3"
        />
      </div>

      <button
        type="button"
        className="swap-button"
        onClick={handleSwap}
        disabled={disabled}
        title="Swap cities"
      >
        ⇄
      </button>

      <div className="form-group">
        <label htmlFor="to">To</label>
        <input
          id="to"
          type="text"
          placeholder="e.g., DEL"
          value={toCity}
          onChange={(e) => setToCity(e.target.value.toUpperCase())}
          disabled={disabled}
          maxLength="3"
        />
      </div>

      <button
        type="submit"
        className="search-button"
        disabled={disabled || !fromCity.trim() || !toCity.trim()}
      >
        🔍 Search
      </button>
    </form>
  );
}

export default SearchForm;
