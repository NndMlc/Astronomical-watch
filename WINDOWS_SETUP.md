# 🪟 Windows Setup - Astronomical Watch Desktop

## 🚀 Kako pokrenuti na Windows-u

### Metoda 1: Direktno pokretanje (Preporučeno)

1. **Download fajlova na Windows**
   ```cmd
   # Kopiraj ove fajlove na tvoj Windows sistem:
   - desktop_app.py
   - standalone_desktop.py  
   - src/ folder (ceo)
   - launch_desktop.bat
   ```

2. **Instaluj Python (ako nemaš)**
   - Idi na https://python.org/downloads/
   - Download Python 3.8+ 
   - Tokom instalacije, štikliraj "Add Python to PATH"

3. **Pokretanje**
   ```cmd
   # Otvori Command Prompt u folderu sa fajlovima
   python desktop_app.py
   
   # Ili dupli klik na:
   launch_desktop.bat
   ```

### Metoda 2: Standalone verzija (Ne traži src/ folder)

```cmd
# Pokreni standalone verziju koja ima ugrađene kalkulacije
python standalone_desktop.py
```

### Metoda 3: Kreiranje .exe fajla

1. **Instaliraj PyInstaller**
   ```cmd
   pip install pyinstaller
   ```

2. **Kreiraj executable**
   ```cmd
   pyinstaller --onefile --windowed --name="AstronomicalWatch" standalone_desktop.py
   ```

3. **Pokreni .exe**
   ```cmd
   dist\AstronomicalWatch.exe
   ```

## 🔧 Troubleshooting

### Problem: "No module named 'astronomical_watch'"
**Rešenje:** Koristi standalone_desktop.py umesto desktop_app.py

### Problem: "tkinter not found" 
**Rešenje:** 
```cmd
pip install tk
# ili reinstaliraj Python sa "tcl/tk and IDLE" opcijom
```

### Problem: Window se ne prikazuje
**Rešenje:** Proveri da li imaš GUI desktop (ne command-line only)

## 🎨 Šta ćeš videti

Desktop widget će prikazati:
```
🌟 Astronomical Watch mikroDies
┌─────────────────────────┐
│       224.995.709       │
│   Dies.miliDies.mikroDies│
├─────────────────────────┤
│ UTC: 15:30:45           │
│ [████████░░] 85%        │
├─────────────────────────┤
│ Dies: 224    Frakc: 0.709│
│ Status: OK              │
└─────────────────────────┘
```

- **Always on top** - ostaje preko drugih aplikacija
- **Real-time updates** - ažurira se svakih 100ms
- **mikroDies precision** - pokazuje 1/1,000,000 dela dana

## 📥 Download instrukcije

Iz dev containera možeš eksportovati fajlove:

1. **Kopiraj sadržaj fajlova:**
   - Otvori `standalone_desktop.py`
   - Select All (Ctrl+A) → Copy (Ctrl+C) 
   - Kreiraj novi .py fajl na Windows-u
   - Paste sadržaj

2. **Ili koristi git:**
   ```cmd
   git clone https://github.com/NndMlc/Astronomical-watch.git
   cd Astronomical-watch
   python standalone_desktop.py
   ```

## ✨ Brzo testiranje

Ako hoćeš brzo test, kopiraj ovaj kod u .py fajl na Windows-u:

```python
# Mini verzija za brz test
import tkinter as tk
from datetime import datetime, timezone

root = tk.Tk()
root.title("Astro Test")
root.geometry("200x100")

def update():
    now = datetime.now(timezone.utc)
    # Simulacija astronomical time
    days = (now - datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)).days
    label.config(text=f"Dies: {days}")
    root.after(1000, update)

label = tk.Label(root, text="Loading...", font=("Arial", 14))
label.pack(pady=30)

update()
root.mainloop()
```

Desktop aplikacija je ready za Windows! 🎉