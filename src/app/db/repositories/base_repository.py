from abc import ABC, abstractmethod
from typing import List, Tuple


class BaseIndexRepository(ABC):
    @abstractmethod
    def get_top_prices_by_date(self, date_str: str, top_n: int = 100) -> List[Tuple[str, float]]:
        pass

    @abstractmethod
    def save_index_performance(self, date: str, daily_return: float, cumulative_return: float):
        pass

    @abstractmethod
    def save_index_composition(self, date: str, tickers: List[str]):
        pass

    @abstractmethod
    def get_index_performance_range(self, start_date: str, end_date: str):
        pass

    @abstractmethod
    def get_composition_by_date(self, date: str):
        pass

    @abstractmethod
    def get_composition_change_dates(self, start_date: str, end_date: str) -> List[str]:
        pass

    @abstractmethod
    def get_composition_for_date(self, date: str) -> List[str]:
        pass

    @abstractmethod
    def get_prices_for_tickers(self, date: str, tickers: List[str]) -> List[Tuple[str, float]]:
        pass
