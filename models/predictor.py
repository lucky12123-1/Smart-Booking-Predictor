"""
Route-specific predictor that identifies cheapest days based on historical data.
Approach: Analyze historical data and find which day of week had cheapest prices most frequently.
"""

import pandas as pd
from collections import defaultdict


class RoutePricePredictor:
    """Predicts best days to buy based on historical price patterns."""
    
    def __init__(self, route_name):
        self.route_name = route_name
        self.historical_data = None
        self.cheapest_day = None
        self.day_rankings = {}
        self.days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
    def fit(self, data):
        """
        Train on historical data to find which days are cheapest most frequently.
        
        Args:
            data: DataFrame with columns ['date', 'day_of_week', 'price']
        """
        self.historical_data = data.copy()
        self._analyze_cheapest_days()
        
    def _analyze_cheapest_days(self):
        """
        Analyze historical data to find:
        - Which day had cheapest price most frequently
        - Ranking of all days from cheapest to most expensive
        """
        if self.historical_data is None or len(self.historical_data) == 0:
            return
        
        # Group by day of week and find cheapest price for each week
        cheapest_by_day = defaultdict(int)  # Count how many times each day was cheapest
        
        # Get all unique weeks in data
        self.historical_data['week'] = self.historical_data['date'].dt.isocalendar().week
        weeks = self.historical_data['week'].unique()
        
        # For each week, find which day had the cheapest price
        for week in weeks:
            week_data = self.historical_data[self.historical_data['week'] == week]
            if len(week_data) > 0:
                cheapest_row = week_data.loc[week_data['price'].idxmin()]
                cheapest_day = cheapest_row['day_of_week']
                cheapest_by_day[cheapest_day] += 1
        
        # Sort days by frequency of being cheapest (descending)
        sorted_days = sorted(cheapest_by_day.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_days:
            self.cheapest_day = sorted_days[0][0]  # Most frequent cheapest day
            
            # Create ranking of all days
            self.day_rankings = {}
            for rank, (day, count) in enumerate(sorted_days, 1):
                self.day_rankings[day] = {
                    'rank': rank,
                    'times_cheapest': count,
                    'percentage': f"{(count / len(weeks) * 100):.1f}%"
                }
            
            # Add days that were never cheapest
            for day in self.days_of_week:
                if day not in self.day_rankings:
                    self.day_rankings[day] = {
                        'rank': len(sorted_days) + 1,
                        'times_cheapest': 0,
                        'percentage': '0%'
                    }
    
    def predict_best_day(self):
        """
        Returns the day with cheapest prices historically.
        
        Returns:
            dict: Contains 'best_day', 'recommendation', and full day rankings
        """
        if self.cheapest_day is None:
            return {
                'route': self.route_name,
                'best_day': 'Unknown',
                'recommendation': 'Insufficient data',
                'day_rankings': self.day_rankings
            }
        
        return {
            'route': self.route_name,
            'best_day': self.cheapest_day,
            'recommendation': f"Book on {self.cheapest_day} for best prices",
            'day_rankings': self.day_rankings
        }
    
    def get_detailed_analysis(self):
        """
        Get detailed analysis of all days with their statistics.
        
        Returns:
            dict: Comprehensive analysis of pricing by day
        """
        result = self.predict_best_day()
        
        # Add detailed stats
        detailed_stats = {}
        for day in self.days_of_week:
            if day in self.day_rankings:
                ranking = self.day_rankings[day]
                detailed_stats[day] = {
                    'position': ranking['rank'],
                    'times_cheapest': ranking['times_cheapest'],
                    'percentage': ranking['percentage']
                }
        
        result['detailed_analysis'] = detailed_stats
        return result
