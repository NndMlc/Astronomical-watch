#!/bin/bash

echo "========================================="
echo "  ASTRONOMICAL WATCH DESKTOP LAUNCHER"
echo "========================================="
echo

cd "$(dirname "$0")"

echo "🌟 Launching mikroDies precision desktop widget..."
echo

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Try to run the main desktop app first  
if [ -f "desktop_app.py" ]; then
    echo "✓ Running main desktop application..."
    python3 desktop_app.py
elif [ -f "standalone_desktop.py" ]; then
    echo "✓ Running standalone version..."
    python3 standalone_desktop.py
else
    echo "❌ Error: No desktop application found!"
    echo "Please ensure desktop_app.py or standalone_desktop.py exists."
    exit 1
fi

echo
echo "👋 Desktop application closed."