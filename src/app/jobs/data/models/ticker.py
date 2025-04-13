from dataclasses import dataclass


@dataclass
class Ticker:
    ticker: str
    name: str
    primary_exchange: str
    market: str
    locale: str
    type: str
    currency_name: str

    def __post_init__(self):
        assert self.ticker, "Ticker symbol cannot be empty"
        assert self.currency_name == "usd", f"{self.ticker}: unsupported currency"
