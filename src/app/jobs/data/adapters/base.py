from abc import ABC, abstractmethod
from typing import List
from src.app.jobs.data.models.stock_record import StockRecord
from src.app.jobs.data.models.ticker import Ticker
import datetime


class StockDataAdapter(ABC):
    @abstractmethod
    def get_normalized_data(self, start_date: datetime.date, end_date: datetime.date) -> List[StockRecord]:
        pass

    @abstractmethod
    def get_normalized_tickers(self, raw_df) -> List[Ticker]:
        pass

