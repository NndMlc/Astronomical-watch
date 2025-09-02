# Platform Notes

This document tracks current and planned platform support for Astronomical-watch.

## 1. Desktop (Current)

| Platform | Status | Interface | Notes |
|----------|--------|-----------|-------|
| Linux (x86_64/ARM) | Supported (manual) | CLI + Tkinter UI | Requires Python 3.10+ (adjust if different); `python3-tk` package for some distros. |
| macOS (Apple Silicon + Intel) | Supported (manual) | CLI + Tkinter UI | Use official python.org installer or brew. |
| Windows 10/11 | Supported (manual) | CLI + Tkinter UI | Standard CPython includes Tkinter. |

## 2. Web / PWA (Planned – introducing now)

We add a minimal FastAPI backend plus a static frontend that:
- Calls `/api/now` for current astronomical context.
- Can be “installed” as a Progressive Web App (Add to Home Screen).
- Caches core static assets for offline “shell” (timestamp will freeze offline).

### Initial Scope
- Endpoint: `/api/now` returns UTC + (optional) solar longitude.
- No user accounts, no DB.
- Re-uses existing `core.solar.solar_longitude_from_datetime` if available.
- Graceful fallback if astronomy module missing.

### Later Enhancements
- `/api/equinox/{year}`
- `/api/longitude?unit=deg`
- CORS + rate limiting (if public).
- Client-side smoothing / animated dial.

## 3. Native Mobile (Future Options)

| Option | Pros | Cons | Notes |
|--------|------|------|------|
| PWA only | Easiest | Limited OS integration | Good baseline; immediate. |
| BeeWare (Python) | Pure Python reuse | More packaging complexity | Bundle core; UI via Toga. |
| Kivy | Mature | Larger runtime | GPU-accelerated, custom UI. |
| Flutter + HTTP API | Polished UI | Two-language stack | Core runs on server. |
| React Native + API | Web skill reuse | Bridge complexity | Similar to Flutter tradeoffs. |

## 4. Packaging Strategy

| Layer | Minimal Dependencies | Extended (Web) |
|-------|----------------------|----------------|
| Core astronomical calc | stdlib only (target) | stdlib only |
| CLI | stdlib | stdlib |
| Web backend | – | fastapi, uvicorn[standard] |
| PWA frontend | – | Pure static (HTML/JS/CSS) |

We keep FastAPI confined to `web/` so core stays clean.

## 5. Security & Deployment Notes

- For public deployment set `UVICORN_HOST=0.0.0.0` behind a reverse proxy (nginx/Caddy).
- Enable gzip/HTTP caching for static.
- Add simple rate limiting (e.g. fastapi-limiter) if endpoints broaden.

## 6. Roadmap Table

| Milestone | Goal | Status |
|-----------|------|--------|
| M1 | CLI working | Done |
| M2 | Web API (now) + static page | In progress |
| M3 | Expose equinox endpoint | Planned |
| M4 | Add installable PWA manifest & offline shell | This commit |
| M5 | Mobile packaging decision | Open |
| M6 | Advanced UI (dial, progress rings) | Planned |

## 7. Local Quick Start (Web)

```bash
# Optional isolated venv
python -m venv .venv && source .venv/bin/activate
pip install fastapi uvicorn

# Run server
python -m web.app
# or uvicorn web.app:app --reload
```

Open: http://127.0.0.1:8000

## 8. License & Contribution

See main README for license. Contributions adding additional endpoints or front-end features welcome—keep core math dependency-light.
