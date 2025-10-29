#!/usr/bin/env python3
"""
Astronomical Watch - Funkcionalni Web Server
FastAPI server koji služi PWA aplikaciju
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path

# Koristimo našu radnu logiku
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

def first_noon_after_equinox(equinox: datetime) -> datetime:
    """
    Nađi prvi 'mean solar noon' na referentnom meridijanu nakon ravnodnevnice
    Referentni meridijan: 168°58'30"W 
    Mean solar noon = 23:15:54 UTC
    """
    NOON_UTC_HOUR = 23
    NOON_UTC_MINUTE = 15
    NOON_UTC_SECOND = 54
    
    eq_date = equinox.date()
    
    noon_candidate = datetime(
        eq_date.year, eq_date.month, eq_date.day,
        NOON_UTC_HOUR, NOON_UTC_MINUTE, NOON_UTC_SECOND,
        tzinfo=timezone.utc
    )
    
    if noon_candidate >= equinox:
        return noon_candidate
    
    return noon_candidate + timedelta(days=1)

def get_astronomical_data():
    """Vraća kompletan set astronomskih podataka sa mikroDies preciznosću"""
    now = datetime.now(timezone.utc)
    year = now.year
    
    current_equinox = compute_simple_equinox(year)
    
    # Ako je pre ravnodnevnice trenutne godine, koristi prethodnu
    if now < current_equinox:
        year -= 1
        current_equinox = compute_simple_equinox(year)
    
    next_equinox = compute_simple_equinox(year + 1)
    
    # Nađi prvi noon nakon ravnodnevnice (početak Dana 0)
    first_noon = first_noon_after_equinox(current_equinox)
    
    # Ako je vreme pre prvog noon-a, dan_index = 0
    if now < first_noon:
        elapsed_from_eq = now - current_equinox
        total_seconds = elapsed_from_eq.total_seconds()
        
        # Dan 0 traje od ravnodnevnice do prvog noon-a
        day_seconds = (first_noon - current_equinox).total_seconds()
        
        if day_seconds > 0:
            # Koliko ukupno mikroDies-a u Dan 0
            total_mikro_dies = 1000000  # 1 milion mikroDies-a u danu
            current_mikro_dies = (total_seconds / day_seconds) * total_mikro_dies
            
            mili_dies = int(current_mikro_dies // 1000)
            mikro_dies_in_current_mili = int(current_mikro_dies % 1000)
            mikro_dies_fraction = (current_mikro_dies % 1)
        else:
            mili_dies = 0
            mikro_dies_in_current_mili = 0
            mikro_dies_fraction = 0.0
            
        day_index = 0
        mili_dies = min(mili_dies, 999)
    else:
        # Računaj od prvog noon-a
        elapsed_from_first_noon = now - first_noon
        total_seconds = elapsed_from_first_noon.total_seconds()
        
        # Koliko punih dana je prošlo
        day_index = int(total_seconds // 86400) + 1  # +1 jer je Dan 0 bio pre prvog noon-a
        
        # Ostatak sekundi u trenutnom danu
        remainder_seconds = total_seconds % 86400
        
        # Konvertuj u mikroDies sistem
        # 1 Dan = 86400 sekundi = 1,000,000 mikroDies-a
        # 1 mikroDies = 0.0864 sekunde
        mikro_dies_per_second = 1000000 / 86400  # ~11.574 mikroDies-a po sekundi
        
        current_mikro_dies = remainder_seconds * mikro_dies_per_second
        
        # miliDies (0-999)
        mili_dies = int(current_mikro_dies // 1000)
        
        # mikroDies unutar trenutnog miliDies-a (0-999)
        mikro_dies_in_current_mili = int(current_mikro_dies % 1000)
        
        # Frakcija unutar trenutnog mikroDies-a za smooth progres bar
        mikro_dies_fraction = (current_mikro_dies % 1)
    
    return {
        "utc_iso": now.isoformat().replace("+00:00", "Z"),
        "day_index": day_index,
        "mili_dies": mili_dies,
        "mikro_dies": mikro_dies_in_current_mili,
        "mikro_dies_fraction": mikro_dies_fraction,  # Progres unutar trenutnog mikroDies-a
        "timestamp": f"{day_index:03d}.{mili_dies:03d}",
        "timestamp_full": f"{day_index:03d}.{mili_dies:03d}.{mikro_dies_in_current_mili:03d}",
        "current_equinox": current_equinox.isoformat().replace("+00:00", "Z"),
        "next_equinox": next_equinox.isoformat().replace("+00:00", "Z"),
        "first_noon": first_noon.isoformat().replace("+00:00", "Z")
    }

# FastAPI aplikacija
app = FastAPI(title="Astronomical Watch API", version="1.0.0")

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
    <title>Astronomical Watch</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            text-align: center;
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        .time-display {
            font-size: 3em;
            margin: 20px 0;
            font-weight: bold;
            letter-spacing: 2px;
        }
        .label {
            font-size: 1.2em;
            margin: 10px 0;
            opacity: 0.8;
        }
        .progress-bar {
            width: 300px;
            height: 15px;
            background: rgba(255,255,255,0.2);
            border-radius: 8px;
            margin: 20px auto;
            overflow: hidden;
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
        <h1>Astronomical Watch</h1>
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
        setInterval(updateTime, 100);  // 100ms = 0.1 sekunde
        
        // Initial load
        updateTime();
        
        // Debug toggle funkcija
        window.toggleDebug = function() {
            window.showDebug = !window.showDebug;
            console.log('Debug mode:', window.showDebug ? 'ON' : 'OFF');
        };
    </script>
</body>
</html>
"""

@app.get("/api/now")
async def get_now():
    """API endpoint za trenutno astronomsko vreme"""
    return JSONResponse(get_astronomical_data())

@app.get("/api/equinox/{year}")
async def get_equinox(year: int):
    """API endpoint za ravnodnevnicu određene godine"""
    try:
        equinox = compute_simple_equinox(year)
        return JSONResponse({
            "year": year,
            "equinox": equinox.isoformat().replace("+00:00", "Z")
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "astronomical-watch"}

if __name__ == "__main__":
    import uvicorn
    print("Pokretam Astronomical Watch web server...")
    print("Otvorite http://localhost:8000 u browseru")
    uvicorn.run(app, host="0.0.0.0", port=8000)