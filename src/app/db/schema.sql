CREATE TABLE IF NOT EXISTS stocks (
    ticker TEXT PRIMARY KEY,
    name TEXT,
    primary_exchange TEXT,
    market TEXT,
    locale TEXT,
    type TEXT,
    currency_name TEXT
);

CREATE TABLE IF NOT EXISTS daily_prices (
    date DATE,
    ticker TEXT,
    price REAL,
    market_cap REAL,
    PRIMARY KEY (date, ticker)
);

CREATE TABLE IF NOT EXISTS index_composition (
    date DATE,
    ticker TEXT,
    weight REAL,
    PRIMARY KEY (date, ticker)
);

CREATE TABLE IF NOT EXISTS index_performance (
    date DATE,
    daily_return REAL,
    cumulative_return REAL,
    PRIMARY KEY (date)
);

