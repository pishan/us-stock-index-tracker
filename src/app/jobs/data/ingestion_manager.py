from src.app.jobs.data.adapters.base import StockDataAdapter
from src.app.jobs.data.stores.base import BaseStore
import datetime


class DataIngestionManager:
    def __init__(self, adapter: StockDataAdapter, store_strategy: BaseStore):
        self.adapter = adapter
        self.store = store_strategy

    def ingest_tickers(self):
        tickers = self.adapter.get_normalized_tickers()
        self.store.store_ticker_metadata(tickers)

    def ingest_stock_data(self, start_date: datetime.date, end_date: datetime.date):
        records = self.adapter.get_normalized_data(start_date, end_date)
        self.store.store_stock_data(records)


if __name__ == "__main__":
    from src.app.jobs.data.adapters.polygon_adapter import PolygonAdapter
    from src.app.jobs.data.stores.duckdb import DuckDBStore
    import datetime
    import pandas as pd

    API_KEY = "API_KEY_HERE"

    adapter = PolygonAdapter(API_KEY)
    store = DuckDBStore()
    ingestion_manager = DataIngestionManager(adapter, store)

    start_date = datetime.date(2025, 4, 10)
    end_date = datetime.date(2025, 4, 11)
    date_range = pd.bdate_range(start=start_date, end=end_date).tolist()

    for date in date_range:
        ingestion_manager.ingest_stock_data(date, date)
