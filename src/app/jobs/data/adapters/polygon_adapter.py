from src.app.jobs.data.fetchers.polygon_fetcher import PolygonFetcher
from src.app.jobs.data.adapters.base import StockDataAdapter
from src.app.jobs.data.models.stock_record import StockRecord
from src.app.jobs.data.models.ticker import Ticker


class PolygonAdapter(StockDataAdapter):
    def __init__(self, api_key=None):
        self.fetcher = PolygonFetcher(api_key)

    def get_normalized_data(self, start_date, end_date):
        data = self.fetcher.fetch_daily_stock_data(start_date, end_date)
        normalized = []

        for date, rows in data.items():
            for row in rows:
                price = row.close
                if price is not None:
                    normalized.append(StockRecord(
                        date=date,
                        ticker=row.ticker,
                        price=float(row.close),
                        market_cap=float(price * float(row.volume))
                    ))

        return normalized

    def get_normalized_tickers(self):
        tickers = self.fetcher.fetch_ticker_metadata()
        results = []

        for ticker in tickers:
            results.append(Ticker(
                ticker=ticker.ticker,
                name=ticker.name,
                primary_exchange=ticker.primary_exchange,
                market=ticker.market,
                locale=ticker.locale,
                type=ticker.type,
                currency_name=ticker.currency_name
            ))

        return results


