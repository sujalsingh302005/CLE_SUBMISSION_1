"""Week 2 Task 1: read CSV, JSON and Parquet with pandas."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_any(path: str | Path) -> pd.DataFrame:
    """Read a file into a DataFrame based on its extension."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix == ".json":
        return pd.read_json(path)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported file type: {suffix}")
