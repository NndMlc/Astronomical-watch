"""
Command-line interface for the astronomical-watch project.

Usage examples:
  astronomical-watch now
  astronomical-watch now --json
  astronomical-watch now --max-error-arcsec 5
  astronomical-watch equinox 2025
  astronomical-watch longitude --unit deg
  astronomical-watch longitude --max-error-arcsec 1 --unit rad
  astronomical-watch version

Design goals:
- Zero non-stdlib dependencies.
- Graceful degradation if certain higher-precision modules are not present yet.
- Future extension hook for a precise equinox solver.
"""  
from __future__ import annotations
import argparse
import json
import math
import sys
from datetime import datetime, timezone

# Fallback imports with defensive guards
try:
    from core.solar import solar_longitude_from_datetime
except Exception:  # pragma: no cover
    solar_longitude_from_datetime = None  # type: ignore

try:
    from astronomical_watch import compute_vernal_equinox
except Exception:  # pragma: no cover
    compute_vernal_equinox = None  # type: ignore

PACKAGE_VERSION = "0.0.1"  # Keep in sync with pyproject.toml

def fmt_timestamp(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

def cmd_now(args: argparse.Namespace) -> int:
    now_dt = datetime.now(timezone.utc)
    data = {
        "utc": fmt_timestamp(now_dt),
    }

    # Optionally compute solar longitude
    if solar_longitude_from_datetime:
        try:
            lon = solar_longitude_from_datetime(
                now_dt,
                max_error_arcsec=args.max_error_arcsec
            ) if args.max_error_arcsec is not None else solar_longitude_from_datetime(now_dt)

            data["solar_longitude_rad"] = lon
            data["solar_longitude_deg"] = lon * 180.0 / math.pi
        except Exception as e:  # pragma: no cover
            data["solar_longitude_error"] = str(e)

    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print(f"UTC now: {data['utc']}")
        if "solar_longitude_deg" in data:
            print(f"Solar longitude: {data['solar_longitude_deg']:.6f}° "
                  f"({data['solar_longitude_rad']:.9f} rad)")

    return 0

def cmd_equinox(args: argparse.Namespace) -> int:
    year = args.year
    if not compute_vernal_equinox:
        print("Equinox computation not available (module missing).", file=sys.stderr)
        return 2
    try:
        dt = compute_vernal_equinox(year)
    except Exception as e:
        print(f"Error computing equinox for {year}: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"year": year, "approx_vernal_equinox_utc": fmt_timestamp(dt)}, indent=2))
    else:
        print(f"Approximate vernal equinox {year}: {fmt_timestamp(dt)}")
    return 0

def cmd_longitude(args: argparse.Namespace) -> int:
    if not solar_longitude_from_datetime:
        print("Solar longitude function not available.", file=sys.stderr)
        return 2
    now_dt = datetime.now(timezone.utc)
    try:
        lon = solar_longitude_from_datetime(
            now_dt,
            max_error_arcsec=args.max_error_arcsec
        ) if args.max_error_arcsec is not None else solar_longitude_from_datetime(now_dt)
    except Exception as e:
        print(f"Error computing solar longitude: {e}", file=sys.stderr)
        return 1

    if args.unit == "deg":
        value = lon * 180.0 / math.pi
    else:
        value = lon

    out = {
        "utc": fmt_timestamp(now_dt),
        "solar_longitude": value,
        "unit": args.unit
    }
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"{out['utc']}  solar_longitude={out['solar_longitude']:.9f} {args.unit}")
    return 0

def cmd_version(_: argparse.Namespace) -> int:
    print(PACKAGE_VERSION)
    return 0

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="astronomical-watch",
        description="Astronomical Watch CLI (experimental)"
    )
    p.add_argument(
        "--max-error-arcsec",
        type=float,
        default=None,
        help="Desired max error for VSOP87D solar longitude (arcseconds). Optional."
    )
    sub = p.add_subparsers(dest="command", required=True)

    # now
    sp_now = sub.add_parser("now", help="Show current astronomical timestamp context (UTC + solar data).")
    sp_now.add_argument("--json", action="store_true", help="Output JSON.")
    sp_now.set_defaults(func=cmd_now)

    # equinox
    sp_eq = sub.add_parser("equinox", help="Compute approximate vernal equinox for a given year.")
    sp_eq.add_argument("year", type=int, help="Gregorian year (e.g. 2025).")
    sp_eq.add_argument("--json", action="store_true", help="Output JSON.")
    sp_eq.set_defaults(func=cmd_equinox)

    # longitude
    sp_lon = sub.add_parser("longitude", help="Show current apparent solar longitude.")
    sp_lon.add_argument("--unit", choices=["rad", "deg"], default="deg", help="Output unit.")
    sp_lon.add_argument("--json", action="store_true", help="Output JSON.")
    sp_lon.set_defaults(func=cmd_longitude)

    # version
    sp_ver = sub.add_parser("version", help="Print package version.")
    sp_ver.set_defaults(func=cmd_version)

    return p

def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())