"""Week 2 Task 2: clean nulls, dates and duplicates."""
from __future__ import annotations

import pandas as pd

PICKUP = "tpep_pickup_datetime"
DROPOFF = "tpep_dropoff_datetime"


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates().reset_index(drop=True)


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Convert pickup/dropoff to datetime; unparseable values become NaT."""
    out = df.copy()
    for col in (PICKUP, DROPOFF):
        if col in out.columns:
            out[col] = pd.to_datetime(out[col], errors="coerce")
    return out


def handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows missing key fields; fill missing passenger_count with 1."""
    out = df.copy()
    required = [c for c in (PICKUP, DROPOFF, "PULocationID", "DOLocationID") if c in out.columns]
    out = out.dropna(subset=required)
    if "passenger_count" in out.columns:
        out["passenger_count"] = out["passenger_count"].fillna(1).astype("int64")
    return out


def remove_invalid_trips(df: pd.DataFrame) -> pd.DataFrame:
    """Dropoff must be after pickup; distance and amounts must be non-negative."""
    out = df.copy()
    if PICKUP in out.columns and DROPOFF in out.columns:
        out = out[out[DROPOFF] > out[PICKUP]]
    for col in ("trip_distance", "fare_amount", "total_amount"):
        if col in out.columns:
            out = out[out[col] >= 0]
    return out.reset_index(drop=True)


def clean_trips(df: pd.DataFrame) -> pd.DataFrame:
    return remove_invalid_trips(handle_nulls(parse_dates(drop_duplicates(df))))
