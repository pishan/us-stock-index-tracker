from src.app.db.repositories.base_repository import BaseIndexRepository
from src.app.utils.date_utils import get_business_days_between, validate_date_string
from typing import List, Optional
from src.app.utils.cache import cache_result


class IndexBuilder:
    def __init__(self, repo: BaseIndexRepository):
        self.repo = repo
        self.cumulative_return = 0.0  # Resettable across builds

    @cache_result
    def build_index(self, start_date: str, end_date: Optional[str] = None) -> dict:
        validate_date_string(start_date)
        if end_date:
            validate_date_string(end_date)
            date_range = get_business_days_between(start_date, end_date)
        else:
            date_range = [start_date]

        compositions = {}

        for i, date in enumerate(date_range):
            top_stocks = self.repo.get_top_prices_by_date(date)
            tickers = [ticker for ticker, _ in top_stocks]
            self.repo.save_index_composition(date, tickers)
            compositions[date] = tickers

            if i > 0:
                prev_date = date_range[i - 1]
                self.calculate_index_performance(prev_date, date, tickers)

        return compositions

    def calculate_index_performance(self, prev_date: str, curr_date: str, tickers: List[str]):
        # Get prices for both dates
        prev_prices = dict(self.repo.get_prices_for_tickers(prev_date, tickers))
        curr_prices = dict(self.repo.get_prices_for_tickers(curr_date, tickers))

        returns = []
        for ticker in tickers:
            if ticker in prev_prices and ticker in curr_prices and prev_prices[ticker] > 0:
                ret = (curr_prices[ticker] - prev_prices[ticker]) / prev_prices[ticker]
                returns.append(ret)

        if not returns:
            daily_return = 0.0
        else:
            daily_return = sum(returns) / len(returns)

        self.cumulative_return += daily_return
        self.repo.save_index_performance(curr_date, daily_return, self.cumulative_return)

