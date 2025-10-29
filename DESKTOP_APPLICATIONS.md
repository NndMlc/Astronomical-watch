# 🌟 Astronomical Watch Desktop Applications

Kreirao sam kompletnu desktop aplikaciju sa mikroDies preciznosću! 

## 📱 Dostupne Aplikacije

### 1. **desktop_app.py** - Glavni Desktop Widget
- Koristi originalni core AstroYear sistem
- Pun spektar mikroDies funkcionalnosti
- Elegant UI sa progress bar-om
- Always-on-top widget funkcionalnost

### 2. **standalone_desktop.py** - Standalone Verzija  
- Ugrađen minimalni astronomical calculator
- Može biti pakovana u .exe
- Ne zahteva external dependencies
- Idealna za distribuciju

## 🚀 Pokretanje

### Linux/macOS:
```bash
# Glavni desktop app (koristi core)
python desktop_app.py

# Standalone verzija
python standalone_desktop.py

# Ili koristiti installer
bash install_desktop.sh
```

### Windows:
```batch
# Direktno pokretanje
python desktop_app.py

# Za distribuciju - pakovati u .exe
bash package_desktop.sh
```

## ✨ Funkcionalnosti

### Prikaz Vremena
- **Format**: `DDD.mmm.µµµ` (Dies.miliDies.mikroDies)
- **Real-time updates**: Svakih 100ms
- **Primjer**: `224.995.709` = Dies 224, 995 miliDies, 709 mikroDies

### UI Komponente
- 🕐 **Glavni prikaz**: Velký time display sa mikroDies preciznosću
- 📊 **Progress bar**: Pokazuje napredak trenutnog miliDies-a
- 🌍 **UTC vreme**: Regullarno UTC vreme za referenču
- 📈 **Detalji**: Dies, miliDies, mikroDies, preciznost

### Astronomical Features
- **Reference meridian**: 168°58'30"W (between Diomede Islands)
- **Day boundary**: Mean solar noon = 23:15:54 UTC
- **Equinox alignment**: Automatic equinox period detection
- **mikroDies precision**: 1/1,000,000 of a Dies (0.0864 seconds)

## 🔧 Instalacija i Distribucija

### Desktop Integration (Linux)
```bash
# Kopirati .desktop fajl
cp astronomical-watch.desktop ~/.local/share/applications/

# Ili auto-install
bash install_desktop.sh
```

### Windows Executable
```bash
# Kreirati .exe fajl
bash package_desktop.sh

# Rezultat: dist/AstronomicalWatch_Install/AstronomicalWatch.exe
```

### Dependencies
- **Python 3.8+**
- **tkinter** (ugrađen u Python)
- **datetime, timezone** (built-in)
- **Optional**: PyInstaller za .exe packaging

## 🎨 UI Design

### Color Scheme
- **Background**: Deep space blue (`#0a0a1a`)
- **Primary panels**: Cosmic blue (`#1a1a3a`)
- **Accent**: Nebula blue (`#2a2a5a`)
- **Text**: Bright white (`#ffffff`)
- **Highlights**: Stellar orange (`#ffaa00`)

### Layout
```
┌─────────────────────────────────────┐
│  🌟 Astronomical Watch mikroDies   │
├─────────────────────────────────────┤
│           224.995.709               │
│        Dies.miliDies.mikroDies      │
├─────────────────────────────────────┤
│  UTC: 23:15:54                      │
│  [████████████░░░] 85% miliDies     │
├─────────────────────────────────────┤
│ Dies: 224        Frakc: 0.709       │
│ Godina: 2024-25  Status: OK         │
└─────────────────────────────────────┘
```

## 🔄 Updates & Precision

### Real-time Updates
- **Frequency**: 100ms (smooth mikroDies animation)
- **Precision**: mikroDies + mikroDies_fraction
- **Accuracy**: ±0.001 mikroDies

### Astronomical Accuracy
- **Equinox precision**: Computed from VSOP87D
- **Day boundary**: Solar noon calculation
- **Time base**: UTC with ΔT corrections

## 📦 Distribution Files

Nakon pokretanja installer/packaging script-ova:

```
AstronomicalWatch_Install/
├── AstronomicalWatch.exe          # Windows executable
├── README.txt                     # Instrukcije za korisnika  
├── Start_AstronomicalWatch.bat    # Windows launcher
└── astronomical-watch.desktop     # Linux desktop entry
```

## 🌟 Korišćenje

1. **Pokretanje**: Dupli klik na executable ili `python desktop_app.py`
2. **Widget mode**: Aplikacija ostaje always-on-top
3. **Real-time**: Trenutno astronomical vreme sa mikroDies preciznosću
4. **Monitoring**: Progress bar pokazuje napredak kroz trenutni miliDies

Desktop aplikacija je kompletan sistem koji koristi naš mikroDies core i prikazuje vreme u elegantan, persistent widget!

---
*Astronom Watch mikroDies Desktop - Realizacija astronomical time sistema na desktop platformama* 🚀