# Astronomical Watch UI Components

This directory contains the user interface components for the Astronomical Watch application.

## Components

### `gradient.py` - Dynamic Sky Gradient Helper
- Computes sky themes based on solar altitude using VSOP87 astronomical data
- Generates smooth color gradients for backgrounds
- Provides adaptive text colors for readability
- 5 different theme types: bright day, moderate day, dawn/dusk, twilight, night

### `widget.py` - Compact Widget Mode
- Small, always-on widget display
- Dynamic gradient background that updates with solar position
- Full-area click activation - any click opens Normal Mode
- Real-time astronomical time display in format `2024eq:123.456`
- Progress bars showing day and year completion

### `normal_mode.py` - Full-Featured Normal Mode  
- Detailed astronomical time interface
- Same gradient background logic as widget mode
- Tabbed interface for current time and settings
- Extended information display including solar altitude
- Auto-updating themes and time displays

### `main.py` - Application Integration
- Manages widget and normal mode windows
- Handles click activation from widget to normal mode
- Demonstrates proper window lifecycle management

## Key Features Implemented

1. **Full Click Activation**: Widget responds to clicks on any area (background, labels, progress bars)
2. **Consistent Gradients**: Both widget and normal mode use identical gradient drawing logic
3. **Astronomical Integration**: Themes driven by real solar position calculations from VSOP87
4. **Adaptive Colors**: Text color automatically adjusts based on background brightness
5. **Real-time Updates**: Both interfaces update automatically to reflect current time and sky conditions

## Usage

```python
# Create and run widget
from ui.widget import create_widget
import tkinter as tk

root = tk.Tk()
widget = create_widget(root, on_click=lambda: print("Opening Normal Mode"))
widget.start_updates()
root.mainloop()

# Create and run normal mode
from ui.normal_mode import create_normal_mode
normal = create_normal_mode()
normal.start_updates()
```

## Testing

Run the gradient logic tests:
```bash
python -m pytest tests/test_ui_gradient.py -v
```

Run the implementation demonstration:
```bash
python demo_implementation.py
```

## Architecture

- **Separation of Concerns**: Gradient logic is separated into `gradient.py` helper
- **Consistent APIs**: Both widget and normal mode have similar `update_*()` and `start_updates()` methods
- **Astronomical Integration**: Uses existing `core.solar` module for calculations
- **Minimal Dependencies**: Only uses tkinter for GUI, integrates with existing astronomical calculations