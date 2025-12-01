#!/bin/bash
# Astronomical Watch Desktop Launcher for Linux/Mac

# Auto-detect timezone if not already set
if [ -z "$TZ" ]; then
    # Try /etc/timezone first (Debian/Ubuntu)
    if [ -f /etc/timezone ]; then
        export TZ=$(cat /etc/timezone)
        echo "Detected timezone: $TZ"
    # Try timedatectl (systemd)
    elif command -v timedatectl &> /dev/null; then
        DETECTED=$(timedatectl show --property=Timezone --value 2>/dev/null)
        if [ -n "$DETECTED" ]; then
            export TZ="$DETECTED"
            echo "Detected timezone: $TZ"
        fi
    fi
fi

echo "Starting Astronomical Watch..."
python3 astronomical_watch_desktop.py