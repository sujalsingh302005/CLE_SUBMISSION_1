"""Week 2 Task 1 demo. Run: python -m taxi_pipeline.read_formats"""
from pathlib import Path

from taxi_pipeline.readers import read_any

RAW = Path("data/raw")

for name in ("taxi_zone_lookup.csv", "yellow_tripdata_2024-01.parquet", "api_response.json"):
    path = RAW / name
    if not path.exists():
        print(f"skip (not found): {path}")
        continue
    df = read_any(path)
    print(f"\n== {name} | shape={df.shape}")
    print(df.dtypes.head(8))
    print(df.head(3))
