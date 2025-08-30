"""
CLI entry point (stub) for astronomical-watch.

Planirani podkomandni interfejs (kasnije):
  astronomical-watch now
  astronomical-watch eot
  astronomical-watch equinox
  astronomical-watch dev

Za sada samo 'now' (ili bez argumenata) ispisuje UTC vrijeme.
"""
from __future__ import annotations
import datetime
import sys

def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    now = datetime.datetime.utcnow().replace(microsecond=0)
    if not args or args[0] == "now":
        print(f"Astronomical Watch UTC now: {now.isoformat()}Z (stub)")
        return 0
    if args[0] in {"-h", "--help"}:
        print("Usage: astronomical-watch [now]")
        return 0
    print(f"Unknown command: {args[0]}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
