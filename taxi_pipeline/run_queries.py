"""Run every query in sql/*.sql against MySQL and save the real output to results/*.md.

These files are your evidence that the queries ran. Run: python -m taxi_pipeline.run_queries
"""
import os
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from taxi_pipeline.logging_setup import get_logger

log = get_logger("run_queries")

HOST = os.getenv("MYSQL_HOST", "localhost")
PORT = os.getenv("MYSQL_PORT", "3306")
USER = os.getenv("MYSQL_USER", "root")
PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB = os.getenv("MYSQL_DATABASE", "nyc_taxi")

SQL_FILES = ["sql/queries.sql", "sql/window_queries.sql"]


def to_markdown(df: pd.DataFrame) -> str:
    if df.empty:
        return "_(no rows)_"
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for row in df.itertuples(index=False):
        lines.append("| " + " | ".join(str(v) for v in row) + " |")
    return "\n".join(lines)


def split_statements(sql: str) -> list[tuple[str, str]]:
    """Return (title, statement) pairs. Title = first '-- ' comment above the statement."""
    out = []
    for chunk in sql.split(";"):
        lines = [ln for ln in chunk.strip().splitlines()]
        title = next((ln[2:].strip() for ln in lines if ln.startswith("--")), "")
        body = "\n".join(ln for ln in lines if not ln.startswith("--")).strip()
        if body and not body.upper().startswith("USE "):
            out.append((title, body))
    return out


def main() -> None:
    engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")
    Path("results").mkdir(exist_ok=True)
    for sql_file in SQL_FILES:
        statements = split_statements(Path(sql_file).read_text())
        parts = [f"# Results: `{sql_file}`", "",
                 f"_Generated {datetime.now():%Y-%m-%d %H:%M} from database `{DB}`._", ""]
        for title, body in statements:
            log.info("Running: %s", title)
            df = pd.read_sql(text(body), engine)
            parts += [f"## {title}", "", "```sql", body + ";", "```", "",
                      f"{len(df)} row(s) returned.", "", to_markdown(df.head(25)), ""]
        out = Path("results") / (Path(sql_file).stem + "_results.md")
        out.write_text("\n".join(parts))
        log.info("Wrote %s", out)


if __name__ == "__main__":
    main()
