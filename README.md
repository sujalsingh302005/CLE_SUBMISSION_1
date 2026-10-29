# NYC Taxi Data Engineering - Hands-on Tasks (Weeks 1-2)

Hands-on work for Sessions 1-2: loading NYC Yellow Taxi data into MySQL, analysing it with SQL,
and building a small pandas pipeline (read, clean, save, pull from an API).

## Repository structure

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── sql/
│   ├── queries.sql            # Week 1 Task 2 - 10 queries (filters, joins, GROUP BY, CTEs)
│   └── window_queries.sql     # Week 1 Task 3 - rank, running total, top-N per group
├── taxi_pipeline/
│   ├── load_mysql.py          # Week 1 Task 1 - load data into MySQL
│   ├── readers.py             # Week 2 Task 1 - read CSV / JSON / Parquet
│   ├── read_formats.py        #   demo script for the readers
│   ├── cleaning.py            # Week 2 Task 2 - nulls, dates, duplicates
│   ├── clean_to_parquet.py    #   runs cleaning and saves Parquet
│   ├── api_client.py          # Week 2 Task 4 - reusable fn: logging + error handling + retries
│   ├── pull_api.py            # Week 2 Task 3 - pull public REST API, save JSON
│   ├── run_queries.py         # runs the SQL files and saves real output to results/
│   └── logging_setup.py
├── results/                   # created by run_queries.py (query output as markdown)
└── data/{raw,processed}/      # data files are git-ignored
```

## Task checklist

| Week | Task | Description | Where |
|------|------|-------------|-------|
| 1 | 1 | Install MySQL and VS Code, load NYC Taxi data | `taxi_pipeline/load_mysql.py` |
| 1 | 2 | 10 queries: filters, joins, GROUP BY, CTEs | `sql/queries.sql` |
| 1 | 3 | 3 window queries | `sql/window_queries.sql` |
| 2 | 1 | Read CSV, JSON, Parquet with pandas | `taxi_pipeline/readers.py` |
| 2 | 2 | Clean nulls, dates, duplicates; save Parquet | `taxi_pipeline/cleaning.py`, `clean_to_parquet.py` |
| 2 | 3 | Pull from public REST API, save JSON | `taxi_pipeline/pull_api.py` |
| 2 | 4 | Reusable function with logging and error handling | `taxi_pipeline/api_client.py` |
| 3 | 1 | Create repo and push Week 1-2 work with a README | this repo |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Download from the [NYC TLC trip record page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
into `data/raw/`:

- `yellow_tripdata_2024-01.parquet`
- `taxi_zone_lookup.csv`

Set MySQL credentials as environment variables (do not commit passwords):

```bash
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_HOST=localhost
export MYSQL_DATABASE=nyc_taxi
```

## How to run (from the repo root)

```bash
python -m taxi_pipeline.load_mysql        # Week 1: load data into MySQL (a few minutes)
python -m taxi_pipeline.run_queries       # Week 1: run all 13 queries, save output to results/

python -m taxi_pipeline.pull_api          # Week 2: save API JSON to data/raw/api_response.json
python -m taxi_pipeline.read_formats      # Week 2: read CSV / JSON / Parquet
python -m taxi_pipeline.clean_to_parquet  # Week 2: clean and save to data/processed/
```

## Design notes

- **Cleaning rules:** drop exact duplicates; parse dates (bad values become NaT); drop rows missing
  pickup/dropoff time or location IDs; fill missing `passenger_count` with 1; drop trips where dropoff
  is not after pickup or where distance/fare is negative.
- **API function:** `fetch_json` retries on timeouts, connection errors, 429 and 5xx with exponential
  backoff, fails fast on other 4xx, logs every attempt, and raises a clear `APIError`.
- **Logging:** console plus `logs/pipeline.log`.

## Results

After running `run_queries`, the output of every query is saved in
[`results/queries_results.md`](results/queries_results.md) and
[`results/window_queries_results.md`](results/window_queries_results.md).
