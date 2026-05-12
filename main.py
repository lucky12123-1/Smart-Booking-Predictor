"""
Smart Booking Predictor - Main POC Script
Demonstrates finding the cheapest day to book flights based on historical data.
"""

import pandas as pd
from datetime import datetime, timedelta
import random
from data.sample_routes import get_sample_routes
from models.predictor import RoutePricePredictor


def generate_synthetic_flight_data(route_type, start_date, days=84):
    """
    Generate 12 weeks (84 days) of synthetic flight price data.
    
    Args:
        route_type: 'business' or 'leisure'
        start_date: Starting date for data generation
        days: Number of days of data (default 84 = 12 weeks)
    
    Returns:
        DataFrame with columns: date, day_of_week, price
    """
    data = []
    
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        day_name = current_date.strftime('%A')
        day_of_week = current_date.weekday()  # 0=Monday, 6=Sunday
        
        # Generate price based on day of week and route type
        base_price = 3000
        
        if route_type == 'business':
            # Business routes: Cheaper weekdays (Mon-Thu), expensive weekends
            if day_of_week < 4:  # Monday to Thursday
                price_multiplier = random.uniform(0.9, 1.0)
            else:  # Friday to Sunday
                price_multiplier = random.uniform(1.4, 1.7)
        else:  # leisure
            # Leisure routes: Cheaper weekdays, expensive weekends
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


def main():
    print("\n" + "="*60)
    print("SMART BOOKING PREDICTOR - POC")
    print("Finding cheapest days to book flights")
    print("="*60 + "\n")
    
    # Start date for synthetic data (12 weeks ago)
    start_date = datetime.now() - timedelta(days=84)
    
    # Get sample routes
    routes = get_sample_routes()
    
    # Train models for each route
    results = []
    
    for route in routes:
        route_name = f"{route['from']} → {route['to']}"
        route_type = route['type']
        
        print(f"\n📍 Route: {route_name}")
        print(f"   Type: {route_type.upper()}")
        print(f"   Analyzing 12 weeks of historical data...\n")
        
        # Generate synthetic data
        data = generate_synthetic_flight_data(route_type, start_date, days=84)
        
        # Train predictor
        predictor = RoutePricePredictor(route_name)
        predictor.fit(data)
        
        # Get prediction
        prediction = predictor.predict_best_day()
        detailed = predictor.get_detailed_analysis()
        
        # Display results
        best_day = prediction['best_day']
        print(f"   ✅ BEST DAY TO BOOK: {best_day}")
        print(f"   💡 {prediction['recommendation']}\n")
        
        # Show ranking of all days
        print("   Day Rankings (from cheapest to most expensive):")
        for day in predictor.days_of_week:
            if day in detailed['detailed_analysis']:
                stats = detailed['detailed_analysis'][day]
                position = stats['position']
                times = stats['times_cheapest']
                percentage = stats['percentage']
                
                # Create visual indicator
                if position == 1:
                    icon = "🥇"
                elif position == 2:
                    icon = "🥈"
                elif position == 3:
                    icon = "🥉"
                else:
                    icon = "  "
                
                print(f"   {icon} {position}. {day:10} - Cheapest {times:2} times ({percentage})")
        
        results.append({
            'route': route_name,
            'best_day': best_day,
            'type': route_type
        })
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for result in results:
        print(f"{result['route']:25} → Best day: {result['best_day']}")
    
    print("\n" + "="*60)
    print("HOW IT WORKS:")
    print("="*60)
    print("""
1. We collected 12 weeks (84 days) of flight price data
2. For each week, we identified which day had the cheapest price
3. We counted how many times each day was the cheapest
4. The day that was cheapest most frequently is recommended

Example:
- If Tuesday was cheapest 7 out of 12 weeks
- Monday was cheapest 3 out of 12 weeks
- We recommend: TUESDAY ✅

This shows the statistical pattern of pricing for that route.
""")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
