"""
Flask Backend API for Smart Booking Predictor
Provides endpoints to search for best days to book flights
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime, timedelta
import random
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.predictor import RoutePricePredictor

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Store generated data in memory (for POC)
route_data_cache = {}


def generate_synthetic_flight_data(route_type, start_date, days=84):
    """
    Generate 12 weeks (84 days) of synthetic flight price data.
    """
    data = []
    
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        day_name = current_date.strftime('%A')
        day_of_week = current_date.weekday()  # 0=Monday, 6=Sunday
        
        # Generate price based on day of week and route type
        base_price = 3000
        
        if route_type == 'business':
            if day_of_week < 4:  # Monday to Thursday
                price_multiplier = random.uniform(0.9, 1.0)
            else:  # Friday to Sunday
                price_multiplier = random.uniform(1.4, 1.7)
        else:  # leisure
            if day_of_week < 5:  # Monday to Friday
                price_multiplier = random.uniform(0.85, 1.0)
            else:  # Saturday and Sunday
                price_multiplier = random.uniform(1.3, 1.6)
        
        price = int(base_price * price_multiplier)
        
        data.append({
            'date': current_date,
            'day_of_week': day_name,
            'price': price
        })
    
    return pd.DataFrame(data)


def determine_route_type(from_city, to_city):
    """
    Determine if route is business or leisure based on city pairs.
    For POC, we'll use simple heuristics.
    """
    leisure_destinations = ['GOA', 'BALI', 'MALDIVES', 'PARIS', 'LONDON', 'DUBAI']
    
    if any(dest in to_city.upper() for dest in leisure_destinations):
        return 'leisure'
    else:
        return 'business'


@app.route('/api/search', methods=['POST'])
def search_route():
    """
    Search for cheapest day to book a flight route.
    Expected JSON: {"from": "BOM", "to": "DEL"}
    """
    try:
        data = request.get_json()
        from_city = data.get('from', '').upper().strip()
        to_city = data.get('to', '').upper().strip()
        
        # Validate input
        if not from_city or not to_city:
            return jsonify({'error': 'Please provide both from and to cities'}), 400
        
        if from_city == to_city:
            return jsonify({'error': 'From and To cities cannot be the same'}), 400
        
        route_key = f"{from_city}→{to_city}"
        
        # Check if route data is already cached
        if route_key not in route_data_cache:
            # Generate synthetic data for this route
            route_type = determine_route_type(from_city, to_city)
            start_date = datetime.now() - timedelta(days=84)
            flight_data = generate_synthetic_flight_data(route_type, start_date, days=84)
            
            # Train predictor
            predictor = RoutePricePredictor(route_key)
            predictor.fit(flight_data)
            
            # Cache the result
            route_data_cache[route_key] = {
                'predictor': predictor,
                'route_type': route_type,
                'created_at': datetime.now()
            }
        
        # Get cached predictor
        cached = route_data_cache[route_key]
        predictor = cached['predictor']
        route_type = cached['route_type']
        
        # Get prediction
        prediction = predictor.predict_best_day()
        detailed = predictor.get_detailed_analysis()
        
        # Format response
        response = {
            'from': from_city,
            'to': to_city,
            'route': route_key,
            'best_day': prediction['best_day'],
            'route_type': route_type,
            'recommendation': prediction['recommendation'],
            'day_rankings': []
        }
        
        # Add day rankings
        for day in predictor.days_of_week:
            if day in detailed['detailed_analysis']:
                stats = detailed['detailed_analysis'][day]
                response['day_rankings'].append({
                    'day': day,
                    'position': stats['position'],
                    'times_cheapest': stats['times_cheapest'],
                    'percentage': stats['percentage']
                })
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({'status': 'API is running'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
