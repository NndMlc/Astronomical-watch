#!/bin/bash

# Astronomical Watch - Desktop Widget Launcher
# Priority: Desktop Widget App -> GUI fallbacks -> Console mode

echo "=================================================="
echo "  ASTRONOMICAL WATCH - DESKTOP WIDGET LAUNCHER"
echo "=================================================="
echo
echo "Launches in widget mode with double-click for normal mode!"
echo

# Check Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python not found!"
    echo "Install Python 3.8+ from your package manager"
    exit 1
fi

# Use python3 if available, otherwise python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo "Python: $($PYTHON_CMD --version)"
echo

# Test tkinter availability
if $PYTHON_CMD -c "import tkinter" 2>/dev/null; then
    echo "tkinter OK - launching desktop widget application"
    echo
    
    # Try desktop widget versions in order
    if [ -f "desktop_widget_app.py" ]; then
        echo "Launching Desktop Widget Application..."
        echo "- Widget mode: Double-click for normal mode"
        echo "- Normal mode: 'Minimize to Widget' button"
        echo
        $PYTHON_CMD desktop_widget_app.py
    elif [ -f "awatch_ultimate.py" ]; then
        echo "Launching ultimate version (GUI mode)..."
        $PYTHON_CMD awatch_ultimate.py
    elif [ -f "desktop_app.py" ]; then
        echo "Launching main desktop application..."
        $PYTHON_CMD desktop_app.py
    else
        echo "ERROR: No desktop application found!"
        echo
        echo "Required files:"
        echo "- desktop_widget_app.py (WIDGET + NORMAL MODE)"
        echo "- awatch_ultimate.py"
        echo "- desktop_app.py"
        echo
        exit 1
    fi
else
    echo "tkinter not available - using console version"
    echo
    
    if [ -f "awatch_ultimate.py" ]; then
        echo "Launching ultimate version (console mode)..."
        $PYTHON_CMD awatch_ultimate.py
    elif [ -f "instant_awatch.py" ]; then
        echo "Launching instant console version..."
        $PYTHON_CMD instant_awatch.py
    else
        echo "ERROR: No console application found!"
        exit 1
    fi
fi

echo
echo "Desktop application closed"