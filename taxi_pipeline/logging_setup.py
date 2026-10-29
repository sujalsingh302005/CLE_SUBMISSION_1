"""Shared logging: console + logs/pipeline.log."""
from __future__ import annotations

import logging
from pathlib import Path


def get_logger(name: str, logfile: str = "logs/pipeline.log") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)
    Path(logfile).parent.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(logfile)
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    return logger
