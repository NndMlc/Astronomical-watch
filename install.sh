#!/bin/bash
# Installation script for Astronomical Watch

set -e

echo "================================"
echo "Astronomical Watch - Installation"
echo "================================"
echo ""

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  This script needs sudo privileges to install system-wide."
    echo "Please run: sudo ./install.sh"
    exit 1
fi

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or newer."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ Found Python $PYTHON_VERSION"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✓ Found pip3"
echo ""

# Install the package
echo "📦 Installing Astronomical Watch..."
pip3 install --upgrade .

# Copy icon
echo "🎨 Installing icon..."
mkdir -p /usr/share/pixmaps
if [ -f "icons/astronomical_watch.png" ]; then
    cp icons/astronomical_watch.png /usr/share/pixmaps/astronomical-watch.png
elif [ -f "icons/astronomical_watch.ico" ]; then
    # Convert ICO to PNG if needed
    if command -v convert &> /dev/null; then
        convert icons/astronomical_watch.ico /usr/share/pixmaps/astronomical-watch.png
    else
        echo "⚠️  ImageMagick not found, skipping icon conversion"
    fi
fi

# Install desktop file
echo "🖥️  Installing desktop entry..."
cp astronomical-watch.desktop /usr/share/applications/
chmod 644 /usr/share/applications/astronomical-watch.desktop
update-desktop-database /usr/share/applications/ 2>/dev/null || true

echo ""
echo "✅ Installation complete!"
echo ""
echo "You can now:"
echo "  • Launch from your application menu"
echo "  • Run 'astronomical-watch' from terminal"
echo "  • Run 'awatch' as a shortcut"
echo ""
echo "To uninstall, run: sudo pip3 uninstall astronomical-watch"
