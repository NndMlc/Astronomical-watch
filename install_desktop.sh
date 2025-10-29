#!/bin/bash
# Instalacijski script za Astronomical Watch Desktop

echo "🌟 ASTRONOMICAL WATCH DESKTOP - INSTALLATION SCRIPT"
echo "================================================="
echo

# Proveri da li Python postoji
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nije pronađen. Molimo instaliraj Python 3.8+"
    exit 1
fi

echo "✓ Python3 pronađen: $(python3 --version)"

# Kreiraj virtual environment
echo "📦 Kreiram virtual environment..."
python3 -m venv venv_awatch
source venv_awatch/bin/activate

# Instaliraj dependencies
echo "⬇️  Instaliram potrebne biblioteke..."
pip install tkinter-dev || echo "tkinter već installiran"

# Kopiraj potrebne fajlove
echo "📁 Pripremam aplikaciju..."
mkdir -p awatch_desktop/src
cp -r src/* awatch_desktop/src/
cp desktop_app.py awatch_desktop/

# Kreiraj launcher script
cat > awatch_desktop/launch.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source ../venv_awatch/bin/activate
python desktop_app.py
EOF

chmod +x awatch_desktop/launch.sh

# Kreiraj .desktop fajl za Linux
cat > astronomical-watch.desktop << EOF
[Desktop Entry]
Name=Astronomical Watch mikroDies
Comment=Astronomical timekeeping with mikroDies precision
Exec=$(pwd)/awatch_desktop/launch.sh
Icon=$(pwd)/awatch_desktop/icon.png
Terminal=false
Type=Application
Categories=Utility;Science;
StartupNotify=true
EOF

echo "📱 Desktop aplikacija je pripremljena!"
echo
echo "🚀 Za pokretanje:"
echo "   1. Linux: Kopiraj astronomical-watch.desktop u ~/.local/share/applications/"
echo "   2. Manual: cd awatch_desktop && bash launch.sh"
echo "   3. Python: cd awatch_desktop && python desktop_app.py"
echo
echo "✨ Aplikacija prikazuje vreme u formatu DDD.mmm.µµµ (Dies.miliDies.mikroDies)"
echo "💡 Widget ostaje uvek na vrhu (always on top)"
echo