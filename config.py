"""
Configuration settings for Smart Booking Predictor.
"""

# Data generation
DATA_COLLECTION_WEEKS = 12
DATA_COLLECTION_DAYS = DATA_COLLECTION_WEEKS * 7  # 84 days

# Model settings
MIN_DATA_POINTS_FOR_PREDICTION = 7  # Minimum weeks needed for reliable prediction

# Routes
SUPPORTED_CITIES = ['BOM', 'DEL', 'GOA', 'BLR', 'HYD', 'CCU', 'MAA', 'PNQ']
