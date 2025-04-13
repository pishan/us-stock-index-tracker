import duckdb
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "index_data.duckdb")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_connection():
    return duckdb.connect(database=DB_PATH)


def execute_db(query: str, params=()):
    with get_connection() as conn:
        conn.execute(query, params)


def query_db(query: str, params=()):
    with get_connection() as conn:
        return conn.execute(query, params).fetchall()


def initialize_db():
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()
    with get_connection() as conn:
        conn.execute(schema_sql)
