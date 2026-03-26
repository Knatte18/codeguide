#!/usr/bin/env python3
"""Print current UTC time as YYYY-MM-DD-HHMMSS."""

from datetime import datetime, timezone

TIMESTAMP_FMT = "%Y-%m-%d-%H%M%S"


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime(TIMESTAMP_FMT)


if __name__ == "__main__":
    print(utcnow())
