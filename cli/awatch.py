#!/usr/bin/env python
"""CLI tool (MIT licensed) printing astronomical time as DDD.mmm"""
from __future__ import annotations
from datetime import datetime, timezone
from astronomical_watch import astronomical_time

def main():
    now = datetime.now(timezone.utc)
    dies, miliDies = astronomical_time(now)
    print(f"{dies:03d}.{miliDies:03d}")

if __name__ == "__main__":
    main()
