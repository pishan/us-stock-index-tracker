from datetime import datetime
import pandas as pd
from typing import List


def validate_date_string(date_str: str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: '{date_str}'. Expected format: YYYY-MM-DD.")


def get_business_days_between(start_date: str, end_date: str) -> List[str]:
    return pd.bdate_range(start=start_date, end=end_date).strftime('%Y-%m-%d').tolist()
