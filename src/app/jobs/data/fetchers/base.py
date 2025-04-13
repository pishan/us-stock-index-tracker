from abc import ABC, abstractmethod
import pandas as pd
import datetime


class StockDataFetcher(ABC):
    @abstractmethod
    def fetch_daily_stock_data(self, tickers: list, start_date: str, end_date: str) -> list[dict]:
        pass

    @abstractmethod
    def fetch_ticker_metadata(self, exchanges: list):
        pass

    def get_business_dates(self, start_date: datetime.date, end_date: datetime.date) -> list[str]:
        return pd.bdate_range(start=start_date, end=end_date).strftime('%Y-%m-%d').tolist()