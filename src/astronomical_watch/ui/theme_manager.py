"""
Centralized theme management to ensure consistent colors across all windows.
All UI components should use get_shared_theme() instead of calling get_sky_theme() directly.
"""
from datetime import datetime
from .gradient import get_sky_theme, SkyTheme

# Global shared theme state
_shared_theme: SkyTheme = None
_shared_theme_time: datetime = None
_theme_update_interval = 60  # Update theme every 60 seconds


def update_shared_theme():
    """Update the shared theme based on local system time."""
    global _shared_theme, _shared_theme_time
    now = datetime.now()  # Use local time
    _shared_theme_time = now
    _shared_theme = get_sky_theme(now)
    return _shared_theme


def get_shared_theme() -> SkyTheme:
    """
    Get the current shared theme.
    All UI components should use this instead of get_sky_theme() directly
    to ensure consistent colors across all windows.
    """
    global _shared_theme
    if _shared_theme is None:
        update_shared_theme()
    return _shared_theme


def get_shared_theme_time() -> datetime:
    """Get the timestamp when the shared theme was last updated."""
    global _shared_theme_time
    return _shared_theme_time
