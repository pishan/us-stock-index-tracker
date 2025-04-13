import pandas as pd
import os
import tempfile
from src.app.db.repositories.base_repository import BaseIndexRepository


def export_to_excel(repo: BaseIndexRepository, start_date: str, end_date: str) -> tuple[str, str]:
    file_name = f"index_data_{start_date}_to_{end_date}.xlsx"
    file_path = os.path.join(tempfile.gettempdir(), file_name)

    # 1. Index Performance
    perf = repo.get_index_performance_range(start_date, end_date)
    perf_df = pd.DataFrame(perf, columns=["Date", "Daily Return", "Cumulative Return"])

    # 2. Daily Compositions
    comp_data = []
    dates = pd.date_range(start=start_date, end=end_date, freq="B").strftime("%Y-%m-%d")
    for d in dates:
        tickers = repo.get_composition_for_date(d)
        for t in tickers:
            comp_data.append({"Date": d, "Ticker": t})
    comp_df = pd.DataFrame(comp_data)

    # 3. Composition Changes (simplified if no detailed data)
    changes = repo.get_composition_change_dates(start_date, end_date)
    changes_df = pd.DataFrame(changes, columns=["Date", "Entered", "Exited"])

    # Write to Excel
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        perf_df.to_excel(writer, sheet_name="Performance", index=False)
        comp_df.to_excel(writer, sheet_name="Compositions", index=False)
        changes_df.to_excel(writer, sheet_name="Changes", index=False)

    return file_name, file_path

