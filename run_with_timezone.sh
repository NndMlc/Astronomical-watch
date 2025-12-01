#!/bin/bash
# Startup script for Astronomical Watch with timezone detection
#
# This script automatically detects or sets the timezone before launching the application.
# You can override the timezone by passing it as an argument:
#   ./run_with_timezone.sh Europe/Belgrade

# Try to detect system timezone if not provided
if [ -z "$1" ]; then
    # Try to read from /etc/timezone (Debian/Ubuntu)
    if [ -f /etc/timezone ]; then
        DETECTED_TZ=$(cat /etc/timezone)
        echo "📍 Detected timezone from /etc/timezone: $DETECTED_TZ"
        export TZ="$DETECTED_TZ"
    # Try timedatectl (systemd systems)
    elif command -v timedatectl &> /dev/null; then
        DETECTED_TZ=$(timedatectl show --property=Timezone --value 2>/dev/null)
        if [ -n "$DETECTED_TZ" ]; then
            echo "📍 Detected timezone from timedatectl: $DETECTED_TZ"
            export TZ="$DETECTED_TZ"
        fi
    # Fallback: use UTC
    else
        echo "⚠️  Could not detect timezone, using UTC"
        export TZ="UTC"
    fi
else
    # Use provided timezone
    export TZ="$1"
    echo "📍 Using specified timezone: $TZ"
fi

# Show current time with timezone
echo "🕐 Current time: $(date '+%Y-%m-%d %H:%M:%S %Z') ($TZ)"
echo ""

# Launch application
if [ -n "$DISPLAY" ]; then
    echo "🚀 Starting Astronomical Watch..."
    python astronomical_watch_desktop.py
else
    echo "❌ Error: DISPLAY not set. Are you in a graphical environment?"
    exit 1
fi
