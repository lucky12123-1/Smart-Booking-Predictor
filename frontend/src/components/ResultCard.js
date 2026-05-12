import React from 'react';
import './ResultCard.css';

function ResultCard({ result }) {
  const getMedalEmoji = (position) => {
    switch (position) {
      case 1:
        return '🥇';
      case 2:
        return '🥈';
      case 3:
        return '🥉';
      default:
        return '  ';
    }
  };

  return (
    <div className="result-card">
      <div className="result-header">
        <h2>{result.from} → {result.to}</h2>
        <span className="route-type">({result.route_type.toUpperCase()})</span>
      </div>

      <div className="best-day-section">
        <div className="best-day-box">
          <p className="best-day-label">✈️ Best Day to Book</p>
          <p className="best-day-value">{result.best_day}</p>
        </div>
      </div>

      <div className="recommendation">
        <p>💡 {result.recommendation}</p>
      </div>

      <div className="day-rankings">
        <h3>📊 Day Rankings</h3>
        <div className="rankings-list">
          {result.day_rankings.map((day, index) => (
            <div key={index} className="ranking-item">
              <div className="rank-info">
                <span className="medal">{getMedalEmoji(day.position)}</span>
                <span className="position">{day.position}.</span>
                <span className="day-name">{day.day}</span>
              </div>
              <div className="rank-stats">
                <span className="times">{day.times_cheapest}x</span>
                <span className="percentage">{day.percentage}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="info-box">
        <p>
          Based on 12 weeks of historical data, <strong>{result.best_day}</strong> has been the cheapest day
          {result.day_rankings[0].times_cheapest > 0 ? ` ${result.day_rankings[0].times_cheapest} times` : ' most often'}.
        </p>
      </div>
    </div>
  );
}

export default ResultCard;
