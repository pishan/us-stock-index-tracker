from src.app.db.database import execute_db, query_db
from src.app.jobs.data.stores.base import BaseStore
from src.app.jobs.data.models.stock_record import StockRecord
from src.app.jobs.data.models.ticker import Ticker
from typing import List


class DuckDBStore(BaseStore):
    def store_stock_data(self, data: List[StockRecord]):
        for row in data:
            execute_db(
                """
                INSERT OR REPLACE INTO daily_prices (date, ticker, price, market_cap)
                VALUES (?, ?, ?, ?)
                """,
                (row.date, row.ticker, row.price, row.market_cap)
            )

    def store_ticker_metadata(self, tickers: List[Ticker]):
        for t in tickers:
            execute_db(
                """
                INSERT OR REPLACE INTO stocks (
                    ticker, name, primary_exchange,
                    market, locale, type, currency_name
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    t.ticker,
                    t.name,
                    t.primary_exchange,
                    t.market,
                    t.locale,
                    t.type,
                    t.currency_name
                )
            )

    def get_all_tickers(self) -> List[str]:
        result = query_db("SELECT ticker FROM stocks")
        return [row[0] for row in result]

    def get_all_stock_data(self) -> List[StockRecord]:
        rows = query_db("SELECT date, ticker, price, market_cap FROM daily_prices")
        return [
            StockRecord(date=row[0], ticker=row[1], price=row[2], market_cap=row[3])
            for row in rows
        ]