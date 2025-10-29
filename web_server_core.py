#!/usr/bin/env python3
"""
Astronomical Watch - Core-based Web Server
FastAPI server koji koristi core AstroYear sa mikroDies preciznosću
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import sys

# Dodaj src direktorijum u path
sys.path.insert(0, 'src')

# Import direktno iz astro_time_core
from astronomical_watch.core.astro_time_core import AstroYear

# Koristimo jednostavnu equinox funkciju
def compute_simple_equinox(year: int) -> datetime:
    """Aproksimativno izračunavanje prolećne ravnodnevnice - poboljšano"""
    # Tačniji datumi za poznate godine (sa sekundama)
    base_dates = {
        2023: datetime(2023, 3, 20, 21, 24, 20, tzinfo=timezone.utc),
        2024: datetime(2024, 3, 20, 3, 6, 28, tzinfo=timezone.utc),
        2025: datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc),
    }
    
    if year in base_dates:
        return base_dates[year]
    
    # Za ostale godine, linearno ekstrapolišemo
    tropical_year_seconds = 365.24219 * 86400
    
    if year < 2023:
        ref_year = 2023
        ref_equinox = base_dates[2023]
        years_diff = ref_year - year
        estimated_equinox = ref_equinox - timedelta(seconds=years_diff * tropical_year_seconds)
    else:
        ref_year = 2025
        ref_equinox = base_dates[2025]
        years_diff = year - ref_year
        estimated_equinox = ref_equinox + timedelta(seconds=years_diff * tropical_year_seconds)
    
    return estimated_equinox

# Globalni AstroYear objekat
_astro_year = None

def get_astro_year():
    """Lazy inicijalizacija AstroYear objekta"""
    global _astro_year
    now = datetime.now(timezone.utc)
    year = now.year
    
    # Ako je pre ravnodnevnice trenutne godine, koristi prethodnu
    current_equinox = compute_simple_equinox(year)
    if now < current_equinox:
        year -= 1
        current_equinox = compute_simple_equinox(year)
    
    next_equinox = compute_simple_equinox(year + 1)
    
    # Kreiraj novi AstroYear ako ne postoji ili je potreban rollover
    if _astro_year is None or now >= next_equinox:
        _astro_year = AstroYear(current_equinox, next_equinox)
    
    return _astro_year

def get_astronomical_data():
    """Vraća kompletan set astronomskih podataka koristeći core AstroYear"""
    now = datetime.now(timezone.utc)
    astro_year = get_astro_year()
    
    # Dobij reading iz core-a
    reading = astro_year.reading(now)
    
    return {
        "utc_iso": reading.iso(),
        "day_index": reading.day_index,
        "mili_dies": reading.miliDies,
        "mikro_dies": reading.mikroDies,
        "mikro_dies_fraction": reading.mikroDies_fraction,
        "timestamp": reading.timestamp(),
        "timestamp_full": reading.timestamp_full(),
        "current_equinox": astro_year.current_equinox.isoformat().replace("+00:00", "Z"),
        "next_equinox": astro_year.next_equinox.isoformat().replace("+00:00", "Z") if astro_year.next_equinox else None,
    }

# FastAPI aplikacija
app = FastAPI(title="Astronomical Watch Core API", version="2.0.0")

# Statičke datoteke
app.mount("/static", StaticFiles(directory="web/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Služi glavnu HTML stranicu"""
    return """
<!DOCTYPE html>
<html lang="sr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Astronomical Watch Core</title>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            text-align: center;
            padding: 40px;
            border-radius: 20px;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.2);
            max-width: 400px;
            width: 90%;
        }
        h1 {
            margin-bottom: 30px;
            font-size: 2.5em;
            font-weight: 300;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .time-display {
            font-size: 3em;
            font-weight: bold;
            margin: 20px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            font-family: 'Courier New', monospace;
        }
        .label {
            font-size: 1.2em;
            opacity: 0.8;
            margin-bottom: 20px;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            overflow: hidden;
            margin: 20px 0;
            border: 1px solid rgba(255,255,255,0.3);
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #8BC34A, #CDDC39);
            border-radius: 8px;
            transition: width 0.2s ease;
            box-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
        }
        .info {
            margin-top: 20px;
            font-size: 0.9em;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Astronomical Watch Core</h1>
        <div class="time-display" id="time">000.000</div>
        <div class="label">Dies.miliDies</div>
        
        <div class="progress-bar">
            <div class="progress-fill" id="milidi-progress"></div>
        </div>
        
        <div class="label" style="font-size: 0.9em; margin-top: 10px;">
            mikroDies: <span id="mikro-dies">000</span>
        </div>
        
        <div class="info" style="border-top: 1px solid rgba(255,255,255,0.2); padding-top: 15px; margin-top: 20px;">
            <div><span id="local-timezone">UTC</span>: <span id="utc">-</span></div>
        </div>
    </div>

    <script>
        async function updateTime() {
            try {
                const response = await fetch('/api/now');
                const data = await response.json();
                
                // Prikaži vreme DDD.mmm format
                document.getElementById('time').textContent = data.timestamp;
                
                // Prikaži lokalno vreme sa vremenskom zonom
                const localDate = new Date(data.utc_iso);
                document.getElementById('utc').textContent = localDate.toLocaleString();
                
                // Automatski detektuj i prikaži vremensku zonu
                const timezoneOffset = -localDate.getTimezoneOffset();
                const hours = Math.floor(Math.abs(timezoneOffset) / 60);
                const minutes = Math.abs(timezoneOffset) % 60;
                const sign = timezoneOffset >= 0 ? '+' : '-';
                const timezoneString = `UTC${sign}${hours}${minutes > 0 ? ':' + minutes.toString().padStart(2, '0') : ''}`;
                document.getElementById('local-timezone').textContent = timezoneString;
                
                // Prikaži trenutni mikroDies
                document.getElementById('mikro-dies').textContent = data.mikro_dies.toString().padStart(3, '0');
                
                // Update progress bar za miliDies kroz mikroDies (0-100%)
                // 0 mikroDies = 0%, 1000 mikroDies = 100% (jedan miliDies)
                const mikroDiesProgress = (data.mikro_dies + data.mikro_dies_fraction) / 1000;
                const progressPercent = mikroDiesProgress * 100;
                document.getElementById('milidi-progress').style.width = progressPercent + '%';
                
                // Debug info (opciono - možete ukloniti)
                if (window.showDebug) {
                    console.log(`miliDies: ${data.mili_dies}, mikroDies u miliDies: ${data.mikro_dies}, progres miliDies: ${progressPercent.toFixed(1)}%`);
                }
                
            } catch (error) {
                console.error('Greška:', error);
                document.getElementById('time').textContent = 'Greška';
            }
        }
        
        // Auto-update brže za mikroDies preciznost (10 puta u sekundi)
        setInterval(updateTime, 100);
        
        // Početno učitavanje
        updateTime();
    </script>
</body>
</html>
"""

@app.get("/api/now")
async def get_now():
    """API endpoint za trenutne astronomske podatke"""
    try:
        data = get_astronomical_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": f"Greška u izračunu: {str(e)}"},
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    print("Pokretam Astronomical Watch Core web server...")
    print("Otvorite http://localhost:8000 u browseru")
    uvicorn.run(app, host="0.0.0.0", port=8000)