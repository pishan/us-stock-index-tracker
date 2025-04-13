from dataclasses import dataclass


@dataclass
class StockRecord:
    date: str
    ticker: str
    price: float
    market_cap: float

    def __post_init__(self):
        assert self.price >= 0, f"Invalid price for {self.ticker} on {self.date}"
        assert self.market_cap >= 0, f"Invalid market cap for {self.ticker} on {self.date}"
