import re
from fastapi.testclient import TestClient

from web.app import app

client = TestClient(app)


def test_api_ping():
    r = client.get("/api/ping")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_api_now_basic():
    r = client.get("/api/now")
    assert r.status_code == 200
    data = r.json()
    for key in ["utc_iso", "frame_year", "day_index", "miliDies", "timestamp_proposed", "note"]:
        assert key in data, f"Missing key {key}"
    assert data["utc_iso"].endswith("Z")
    assert 0 <= data["miliDies"] <= 999
    assert re.match(r"^\d{4}eq:000\.\d{3}$", data["timestamp_proposed"])


def test_api_now_with_longitude():
    r = client.get("/api/now?include_longitude=true")
    assert r.status_code == 200
    data = r.json()
    assert "solar_longitude_deg" in data
    val = data["solar_longitude_deg"]
    if val is not None:
        assert isinstance(val, (int, float))


def test_api_equinox_not_implemented_or_ok():
    r = client.get("/api/equinox/2025")
    if r.status_code == 200:
        data = r.json()
        assert "equinox_utc" in data
    else:
        assert r.status_code in (501, 500)
