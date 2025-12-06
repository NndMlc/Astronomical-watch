# Astronomical Watch UI Components

This directory contains the user interface components for the Astronomical Watch application.

## Components

### `gradient.py` - Dynamic Sky Gradient Helper
- Computes sky themes based on solar altitude using VSOP87 astronomical data
- Generates smooth color gradients for backgrounds
- Provides adaptive text colors for readability
- 5 different theme types: bright day, moderate day, dawn/dusk, twilight, night

### `widget.py` - Enhanced Borderless Widget Mode (2025)
- **180×110 borderless floating overlay** (`overrideredirect(True)`)
- **Double-click activation** - prevents accidental Normal Mode opening
- **Drag support** - move widget by dragging anywhere (no title bar)
- **White text with black outline** - optimal visibility on any background
- **86ms update interval** - ultra-fast refresh (1 mikroDies precision)
- **Format**: `DDD.mmm` (Dies.miliDies) with separated labels below
- **Localized title** - changes with language selection
- **Visual progress bar** - mikroDies indicator (YellowGreen color, no text counter)

### `normal_mode.py` - Full-Featured Normal Mode  
- Detailed astronomical time interface with explanation system
- Same gradient background logic as widget mode
- **28-language support** with scrollable language menu
- **Explanation button** - loads content from `translate/` folder
- Extended information display including solar altitude
- Auto-updating themes and time displays

### `main.py` - Application Integration
- Manages widget and normal mode windows
- Handles double-click activation from widget to normal mode
- Demonstrates proper window lifecycle management

## Key Features (Latest 2025)

1. **Borderless Widget**: No title bar, perfect floating overlay
2. **Double-Click Activation**: Smart interaction - drag to move, double-click to activate
3. **Outline Text Rendering**: Canvas-based text with black outline for visibility
4. **Ultra-Fast Updates**: 86ms intervals matching astronomical precision
5. **Multilingual Explanations**: Dynamic content loading from 28 language files
6. **Drag Support**: Full widget repositioning without title bar

## Usage

```python
# Create and run enhanced widget
from ui.widget import create_widget
import tkinter as tk

root = tk.Tk()
widget = create_widget(root, on_click=lambda: print("Opening Normal Mode"))
widget.start_updates()  # 86ms interval updates
root.mainloop()

# Create normal mode with explanation system
from ui.normal_mode import create_normal_mode
normal = create_normal_mode()
normal.start_updates()
```

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