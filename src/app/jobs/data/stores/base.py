from abc import ABC, abstractmethod
from typing import List
from src.app.jobs.data.models.stock_record import StockRecord
from src.app.jobs.data.models.ticker import Ticker


class BaseStore(ABC):
    @abstractmethod
    def store_stock_data(self, data: List[StockRecord]):
        pass

    @abstractmethod
    def store_ticker_metadata(self, tickers: List[Ticker]):
        pass

    @abstractmethod
    def get_all_tickers(self) -> List[str]:
        pass

