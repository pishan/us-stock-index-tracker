import pandas as pd
import os
import tempfile
from src.app.db.repositories.base_repository import BaseIndexRepository
from src.app.utils.cache import cache_result
from src.app.services.performance import PerformanceService


@cache_result
def export_to_excel(performance_service: PerformanceService, start_date: str, end_date: str) -> tuple[str, str]:
    file_name = f"index_data_{start_date}_to_{end_date}.xlsx"
    file_path = os.path.join(tempfile.gettempdir(), file_name)

    # 1. Index Performance
    perf = performance_service.get_performance(start_date, end_date)
    perf_df = pd.DataFrame(perf).rename(columns={
        "date": "Date",
        "daily_return": "Daily Return",
        "cumulative_return": "Cumulative Return"
    })

    # 2. Daily Compositions
    comp_data = []
    dates = pd.date_range(start=start_date, end=end_date, freq="B").strftime("%Y-%m-%d")
    for d in dates:
        tickers = performance_service.get_composition(d)
        for t in tickers:
            comp_data.append({"Date": d, "Ticker": t})
    comp_df = pd.DataFrame(comp_data)

    # 3. Composition Changes (simplified if no detailed data)
    changes = performance_service.get_composition_changes(start_date, end_date)
    changes_df = pd.DataFrame(changes, columns=["Date", "Entered", "Exited"])

    # Write to Excel
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        perf_df.to_excel(writer, sheet_name="Performance", index=False)
        comp_df.to_excel(writer, sheet_name="Compositions", index=False)
        changes_df.to_excel(writer, sheet_name="Changes", index=False)

    return file_name, file_path
