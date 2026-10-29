"""Week 1 Task 1: load NYC Taxi data into MySQL.

Download into data/raw/ first (https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page):
  yellow_tripdata_2024-01.parquet
  taxi_zone_lookup.csv
Credentials are read from environment variables (see README) - never hard-code them.
Loading ~3M rows takes a few minutes.
Run: python -m taxi_pipeline.load_mysql
"""
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from taxi_pipeline.logging_setup import get_logger

log = get_logger("load_mysql")

HOST = os.getenv("MYSQL_HOST", "localhost")
PORT = os.getenv("MYSQL_PORT", "3306")
USER = os.getenv("MYSQL_USER", "root")
PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB = os.getenv("MYSQL_DATABASE", "nyc_taxi")


def main() -> None:
    base = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}"
    with create_engine(base).begin() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB}"))
    engine = create_engine(f"{base}/{DB}")

    zones = pd.read_csv(Path("data/raw/taxi_zone_lookup.csv"))
    zones.to_sql("taxi_zones", engine, if_exists="replace", index=False)
    log.info("Loaded taxi_zones: %d rows", len(zones))

    trips = pd.read_parquet(Path("data/raw/yellow_tripdata_2024-01.parquet"))
    trips.to_sql("taxi_trips", engine, if_exists="replace", index=False,
                 chunksize=10_000, method="multi")
    log.info("Loaded taxi_trips: %d rows", len(trips))

    # Indexes make the joins and date filters in sql/*.sql run in seconds, not minutes.
    with engine.begin() as conn:
        conn.execute(text("CREATE INDEX idx_zones_id ON taxi_zones (LocationID)"))
        conn.execute(text("CREATE INDEX idx_trips_pu ON taxi_trips (PULocationID)"))
        conn.execute(text("CREATE INDEX idx_trips_do ON taxi_trips (DOLocationID)"))
        conn.execute(text("CREATE INDEX idx_trips_pickup ON taxi_trips (tpep_pickup_datetime)"))
    log.info("Created indexes")


if __name__ == "__main__":
    main()
