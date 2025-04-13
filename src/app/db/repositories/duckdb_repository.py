import duckdb
import threading
from typing import List, Tuple
from src.app.db.repositories.base_repository import BaseIndexRepository
from src.app.db.database import DB_PATH


class DuckDBIndexRepository(BaseIndexRepository):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_path=DB_PATH):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DuckDBIndexRepository, cls).__new__(cls)
                cls._instance.conn = duckdb.connect(db_path)
            return cls._instance

    def get_top_prices_by_date(self, date_str: str, top_n: int = 100) -> List[Tuple[str, float]]:
        query = f"""
        SELECT ticker, price FROM daily_prices
        WHERE date = '{date_str}'
        ORDER BY market_cap DESC
        LIMIT {top_n}
        """
        return self.conn.execute(query).fetchall()

    def save_index_performance(self, date: str, daily_return: float, cumulative_return: float):
        self.conn.execute("""
        INSERT OR REPLACE INTO index_performance (date, daily_return, cumulative_return)
        VALUES (?, ?, ?)""", (date, daily_return, cumulative_return))

    def save_index_composition(self, date: str, tickers: List[str]):
        for ticker in tickers:
            self.conn.execute("""
            INSERT OR REPLACE INTO index_composition (date, ticker)
            VALUES (?, ?)""", (date, ticker))

    def get_index_performance_range(self, start_date: str, end_date: str):
        return self.conn.execute("""
        SELECT * FROM index_performance
        WHERE date BETWEEN ? AND ?
        """, (start_date, end_date)).fetchall()

    def get_composition_by_date(self, date: str):
        return self.conn.execute("""
        SELECT ticker FROM index_composition
        WHERE date = ?
        """, (date,)).fetchall()

    def get_composition_for_date(self, date: str) -> List[str]:
        result = self.get_composition_by_date(date)
        return [row[0] for row in result]

    def get_composition_change_dates(self, start_date: str, end_date: str):
        from src.app.utils.date_utils import get_business_days_between

        dates = get_business_days_between(start_date, end_date)
        changes = []

        for i in range(1, len(dates)):
            prev_date = dates[i - 1]
            curr_date = dates[i]

            prev_set = set(self.get_composition_for_date(prev_date))
            curr_set = set(self.get_composition_for_date(curr_date))

            entered = sorted(curr_set - prev_set)
            exited = sorted(prev_set - curr_set)

            if entered or exited:
                changes.append((curr_date, entered, exited))

        return changes

    def get_prices_for_tickers(self, date: str, tickers: List[str]) -> List[Tuple[str, float]]:
        if not tickers:
            return []

        placeholders = ",".join(["?"] * len(tickers))
        query = f"""
            SELECT ticker, price FROM daily_prices
            WHERE date = ? AND ticker IN ({placeholders})
        """
        return self.conn.execute(query, [date] + tickers).fetchall()


