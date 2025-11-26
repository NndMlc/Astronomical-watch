#!/bin/bash
# Astronomical Watch Widget - Linux Autostart Setup

echo "========================================"
echo " ASTRONOMICAL WATCH AUTOSTART SETUP"
echo "========================================"
echo

# Create desktop file for autostart
DESKTOP_FILE="$HOME/.config/autostart/astronomical-watch-widget.desktop"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Creating autostart entry..."

# Create autostart directory if it doesn't exist
mkdir -p "$HOME/.config/autostart"

# Create desktop file
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Type=Application
Name=Astronomical Watch Widget
Comment=Floating astronomical timekeeping widget
Exec=$SCRIPT_DIR/startup_widget.sh
Icon=$SCRIPT_DIR/icons/astronomical_watch.png
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
StartupNotify=false
EOF

if [ -f "$DESKTOP_FILE" ]; then
    echo "✅ Autostart entry created successfully!"
    echo "📁 Location: $DESKTOP_FILE"
    echo
    echo "Widget will now start automatically when you log in."
    echo
    echo "To disable autostart:"
    echo "  rm '$DESKTOP_FILE'"
    echo
    echo "To test autostart now:"
    echo "  $SCRIPT_DIR/startup_widget.sh"
else
    echo "❌ Failed to create autostart entry"
    echo "Manual setup required"
fi

echo
echo "Manual autostart setup (alternative):"
echo "1. Copy this command to your shell startup file:"
echo "   ($SCRIPT_DIR/startup_widget.sh &)"
echo "2. Add to ~/.bashrc, ~/.profile, or ~/.xsessionrc"