from pathlib import Path

def test_static_assets_exist():
    base = Path(__file__).resolve().parent.parent / "web" / "static"
    for fname in ["index.html", "app.js", "service-worker.js", "manifest.webmanifest"]:
        assert (base / fname).exists(), f"Missing static asset: {fname}"
