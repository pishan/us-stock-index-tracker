# Stock Index Tracker

A backend service to track and manage a custom equal-weighted stock index of the top 100 US stocks by daily market capitalization.

---

## 🚀 Setup Instructions

### Local Development

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/stock-index.git
cd stock-index
```

2. **Install Dependencies** (using Poetry)
```bash
poetry install
```

3. **Run the API**
```bash
poetry run uvicorn src.app.main:app --reload
```

4. **Start Redis (Locally)**
```bash
redis-server
```

### Docker Setup

1. **Run Everything via Docker Compose**
```bash
docker-compose up --build
```

This will start:
- FastAPI app
- Redis instance

---

## 📅 Running the Data Acquisition Job

The data acquisition job runs independently to fetch historical market cap and price data.

### Run the job manually:
```bash
poetry run python src/app/jobs/data/ingestion_manager.py
```

This script will:
- Fetch at least 30 trading days of top stock data (via Polygon API or alternative).
- Store the data into DuckDB.

You can adjust the data sources inside the `fetchers/` directory and use `PolygonFetcher` or similar implementations.

---

## 🔗 API Usage

Swagger UI: `http://localhost:8000/docs`

### 📋 Build Index
```bash
curl -X POST "http://localhost:8000/build-index?start_date=2025-04-01&end_date=2025-04-11"
```

### 📈 Get Index Performance
```bash
curl "http://localhost:8000/index-performance?start_date=2025-04-01&end_date=2025-04-11"
```

### 🗓 Get Index Composition for a Day
```bash
curl "http://localhost:8000/index-composition?date=2025-04-08"
```

### 📊 Get Composition Changes
```bash
curl "http://localhost:8000/composition-changes?start_date=2025-04-01&end_date=2025-04-11"
```

### 📄 Export Data (Downloadable Excel)
```bash
curl -X POST "http://localhost:8000/export-data?start_date=2025-04-01&end_date=2025-04-11" --output index_data.xlsx
```

---

## 🔹 Database Schema Overview

### `daily_prices`
Stores daily price and market cap for each stock.
```sql
CREATE TABLE daily_prices (
    date TEXT,
    ticker TEXT,
    price REAL,
    market_cap REAL
);
```

### `index_composition`
Stores the top 100 tickers per day.
```sql
CREATE TABLE index_composition (
    date TEXT,
    ticker TEXT
);
```

### `index_performance`
Stores daily return and cumulative return.
```sql
CREATE TABLE index_performance (
    date TEXT,
    daily_return REAL,
    cumulative_return REAL
);
```

---

## 🛠 Notes
- All SQL runs via DuckDB.
- Redis caches computed results.
- Index construction happens at API runtime.

For improvements and production deployment ideas, see `PRODUCTION_NOTES.md` (if included).

---

Made with ❤️ using FastAPI, DuckDB, and Redis.
