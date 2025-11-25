#!/bin/bash
# Astronomical Watch Widget - Auto Startup Script
# Add this to your desktop autostart applications

echo "========================================"
echo " ASTRONOMICAL WATCH WIDGET AUTO-START"
echo "========================================"
echo

# Navigate to script directory
cd "$(dirname "$0")"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    echo "Please install Python 3.6+ from your package manager"
    exit 1
fi

echo "🐍 Python version: $(python3 --version)"
echo "🚀 Starting floating astronomical widget..."
echo

# Launch widget with error handling
python3 astronomical_watch_widget_only.py

if [ $? -ne 0 ]; then
    echo
    echo "❌ Error starting widget"
    echo "Check Python installation and dependencies"
fi