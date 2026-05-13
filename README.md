````markdown name=README.md
# Smart Booking Predictor

**ML model to predict the best days to book flights based on historical price patterns.**

## 🎯 Concept

Instead of showing average prices, this model:
1. **Collects historical flight data** (price for each day over 12+ weeks)
2. **Analyzes patterns** - For each week, identifies which day had the cheapest price
3. **Counts occurrences** - Counts how many times each day of week was the cheapest
4. **Recommends** - The day that was cheapest most frequently is recommended to book

### Example
```
Analyzing 12 weeks of data:
- Tuesday was cheapest 7 times ✅ RECOMMENDED
- Monday was cheapest 3 times
- Wednesday was cheapest 2 times
- Other days: 0 times

Recommendation: Book on TUESDAY for best prices
```

## 🏗️ Project Structure

```
smart-booking-predictor/
├── data/
│   └── sample_routes.py          # Route definitions
├── models/
│   └── predictor.py              # Core prediction logic
├── main.py                        # Run this file to see POC
├── config.py                      # Configuration
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the POC
```bash
python main.py
```

### 3. Open the Frontend
Open `index.html` in your browser to use the route search UI.

### 4. Search a Specific Sector
```bash
python main.py BOM DEL
```

If the sector is not available in the sample data, the script will show:
```bash
No flight found for that sector: BOM → HYD
```

### 5. View Results
The script will:
- Generate 12 weeks of synthetic flight data for 4 routes
- Analyze which day was cheapest most frequently
- Show rankings for each day of the week
- Provide a clear recommendation

### Sample Output
```
📍 Route: BOM → DEL
   Type: BUSINESS
   Analyzing 12 weeks of historical data...

   ✅ BEST DAY TO BOOK: Monday
   💡 Book on Monday for best prices

   Day Rankings (from cheapest to most expensive):
   🥇 1. Monday     - Cheapest 8 times (66.7%)
   🥈 2. Tuesday    - Cheapest 3 times (25.0%)
   🥉 3. Wednesday  - Cheapest 1 times (8.3%)
      4. Thursday   - Cheapest 0 times (0%)
      5. Friday     - Cheapest 0 times (0%)
      6. Saturday   - Cheapest 0 times (0%)
      7. Sunday     - Cheapest 0 times (0%)
```

## 📊 How It Works

### Current POC (Synthetic Data)
1. **Generates 84 days** (12 weeks) of realistic synthetic flight prices
2. **Route types**:
   - **Business routes** (BOM→DEL): Cheaper Mon-Thu, expensive Fri-Sun
   - **Leisure routes** (BOM→GOA): Cheaper weekdays, expensive weekends

3. **Analysis**:
   - For each week, finds the day with minimum price
   - Counts occurrences of each day being cheapest
   - Ranks days by frequency

4. **Prediction**:
   - Returns the day that was cheapest most frequently
   - Shows ranking and percentage for all days

### Next Steps
1. **Replace synthetic data** with real flight prices from APIs
2. **Add more routes** as needed
3. **Increase data collection** to 6+ months for better patterns
4. **Build API endpoint** for easy integration
5. **Add web interface** for user-friendly search

## 🔄 Data Requirements

For reliable predictions, collect:
- **Minimum**: 12 weeks (84 days) of price data per route
- **Ideal**: 6+ months of historical data
- **Fields**: Date, Day of Week, Price, Route, Airline

## 🛠️ Technology Stack

- **Language**: Python 3.8+
- **Data Processing**: Pandas, NumPy
- **Statistics**: Built-in Python

## 📈 Future Improvements

- [ ] Real flight data integration (Amadeus, Sabre APIs)
- [ ] Database storage (PostgreSQL)
- [ ] Web API (FastAPI/Flask)
- [ ] Web UI for searching routes
- [ ] Advanced ML models (LSTM for seasonality)
- [ ] Booking window analysis (when to book relative to flight date)
- [ ] Price trend visualization
- [ ] User preferences and filters

## 📝 License

MIT License

## 👤 Author

smart-booking-predictor

---

**Status**: Early POC with synthetic data ✨
**Next**: Integrate real flight data
````
