"""Week 2 Task 2. Run: python -m taxi_pipeline.clean_to_parquet"""
from pathlib import Path

from taxi_pipeline.cleaning import clean_trips
from taxi_pipeline.logging_setup import get_logger
from taxi_pipeline.readers import read_any

log = get_logger("clean")


def main() -> None:
    raw = read_any(Path("data/raw/yellow_tripdata_2024-01.parquet"))
    log.info("Raw rows: %d", len(raw))
    clean = clean_trips(raw)
    log.info("Clean rows: %d (removed %d)", len(clean), len(raw) - len(clean))
    out = Path("data/processed/yellow_tripdata_2024-01_clean.parquet")
    out.parent.mkdir(parents=True, exist_ok=True)
    clean.to_parquet(out, index=False)
    log.info("Saved %s", out)


if __name__ == "__main__":
    main()
