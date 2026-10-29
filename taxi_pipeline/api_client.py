"""Week 2 Tasks 3-4: pull from a public REST API, wrapped in a reusable function
with logging, retries and error handling."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import requests

from taxi_pipeline.logging_setup import get_logger

log = get_logger(__name__)


class APIError(RuntimeError):
    """Raised when the API call fails after all retries."""


def fetch_json(
    url: str,
    params: dict[str, Any] | None = None,
    retries: int = 3,
    backoff: float = 2.0,
    timeout: float = 15.0,
) -> Any:
    """GET a URL and return parsed JSON. Retries on network errors, 429 and 5xx."""
    for attempt in range(1, retries + 1):
        try:
            log.info("GET %s (attempt %d/%d)", url, attempt, retries)
            resp = requests.get(url, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except (requests.ConnectionError, requests.Timeout) as exc:
            log.warning("Network error: %s", exc)
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else None
            log.warning("HTTP error %s", status)
            if status is not None and 400 <= status < 500 and status != 429:
                raise APIError(f"Client error {status} for {url}") from exc
        except ValueError as exc:
            raise APIError(f"Response from {url} was not valid JSON") from exc
        if attempt < retries:
            time.sleep(backoff**attempt)
    raise APIError(f"Failed to fetch {url} after {retries} attempts")


def fetch_and_save(url: str, out_path: str | Path, **kwargs: Any) -> Path:
    """Fetch JSON from `url` and write it to `out_path`."""
    data = fetch_json(url, **kwargs)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2))
    log.info("Saved %s (%d bytes)", out, out.stat().st_size)
    return out
