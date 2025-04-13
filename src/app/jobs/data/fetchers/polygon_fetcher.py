import requests
import pandas as pd
import os
from polygon import RESTClient

from src.app.jobs.data.fetchers.base import StockDataFetcher


class PolygonFetcher(StockDataFetcher):
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("POLYGON_API_KEY")
        self.rest_client = RESTClient(self.api_key, retries=10)

    def fetch_ticker_metadata(self):
        all_tickers = []

        tickers = self.rest_client.list_tickers(
                        market="stocks",
                        active="true",
                        order="asc",
                        limit="1000",
                        sort="ticker",
                        )
        try:
            for ticker in tickers:
                all_tickers.append(ticker)
        except BaseException as e:
            pass

        return all_tickers

    def fetch_daily_stock_data(self, start_date, end_date):
        dates = self.get_business_dates(start_date, end_date)
        results = {}
        for date_str in dates:
            results[date_str] = self.rest_client.get_grouped_daily_aggs(
                date_str,
                adjusted="true",
            )
        return results



