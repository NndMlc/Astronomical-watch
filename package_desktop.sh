# Astronomical Watch Desktop - Package Script
# Kreiranje executable fajlova za različite platforme

echo "📦 ASTRONOMICAL WATCH PACKAGING SCRIPT"
echo "======================================"
echo

# Instaliraj PyInstaller ako nije
echo "⬇️  Instaliram PyInstaller..."
pip install pyinstaller

# Kreiraj spec fajl
cat > astronomical_watch.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['standalone_desktop.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AstronomicalWatch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
EOF

echo "🔨 Pravim Windows executable..."
pyinstaller --onefile --windowed --name="AstronomicalWatch" standalone_desktop.py

echo "📁 Kreiranje installation foldera..."
mkdir -p dist/AstronomicalWatch_Install

# Kopiraj executable
cp dist/AstronomicalWatch* dist/AstronomicalWatch_Install/

# Kreiraj README za distribuciju
cat > dist/AstronomicalWatch_Install/README.txt << 'EOF'
ASTRONOMICAL WATCH DESKTOP
=========================

🌟 Astronomical Watch mikroDies Precision

POKRETANJE:
- Windows: Dupli klik na AstronomicalWatch.exe
- Linux: ./AstronomicalWatch (ili python standalone_desktop.py)
- macOS: Dupli klik na AstronomicalWatch

FUNKCIJE:
- Prikazuje vreme u formatu DDD.mmm.μμμ
- DDD = Dies (astronomical day broj)
- mmm = miliDies (1/1000 od Dies) 
- μμμ = mikroDies (1/1000 od miliDies)

KARAKTERISTIKE:
- Always-on-top widget
- Ažuriranje svakih 100ms
- UTC vreme prikaz
- Standalone - ne traži instalaciju

ASTRONOMICAL TIME SYSTEM:
- Baziran na vernal equinox-u
- Reference meridian: 168°58'30"W
- Day boundary: Mean solar noon
- 1 Dies = 86400 sekundi
- 1 miliDies = 86.4 sekundi
- 1 mikroDies = 0.0864 sekundi

© 2024 Astronomical Watch Project
EOF

# Kreiraj batch fajl za Windows
cat > dist/AstronomicalWatch_Install/Start_AstronomicalWatch.bat << 'EOF'
@echo off
title Astronomical Watch mikroDies
echo Starting Astronomical Watch...
AstronomicalWatch.exe
pause
EOF

echo "✅ Packaging završen!"
echo
echo "📂 Fajlovi su u: dist/AstronomicalWatch_Install/"
echo "🚀 Za distribuciju, zapakovaj ceo folder"
echo "💡 Windows korisnici mogu pokrenuti .exe direktno"
echo