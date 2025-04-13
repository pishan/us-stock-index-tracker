from src.app.db.repositories.base_repository import BaseIndexRepository
from src.app.utils.cache import cache_result
from src.app.utils.date_utils import validate_date_string


class PerformanceService:
    def __init__(self, repo: BaseIndexRepository):
        self.repo = repo

    @cache_result
    def get_performance(self, start_date: str, end_date: str):
        validate_date_string(start_date)
        validate_date_string(end_date)
        rows = self.repo.get_index_performance_range(start_date, end_date)
        return [
            {
                "date": row[0].isoformat(),
                "daily_return": round(row[1], 2),
                "cumulative_return": round(row[2], 2)
            } for row in rows
        ]

    @cache_result
    def get_composition(self, date: str):
        validate_date_string(date)
        tickers = self.repo.get_composition_for_date(date)
        return tickers

    @cache_result
    def get_composition_changes(self, start_date: str, end_date: str):
        validate_date_string(start_date)
        validate_date_string(end_date)
        rows = self.repo.get_composition_change_dates(start_date, end_date)

        return rows

