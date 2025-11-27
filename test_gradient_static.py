#!/usr/bin/env python3
"""
Static test of Normal Mode gradient display.
"""

import os
import sys
import tkinter as tk
from datetime import datetime, timezone

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from astronomical_watch.ui.gradient import get_sky_theme, create_gradient_colors

def test_static_gradient():
    print("🚀 Testing static gradient display...")
    
    # Create root window
    root = tk.Tk()
    root.title("Gradient Test")
    root.geometry("600x400")
    
    # Get theme
    theme = get_sky_theme()
    print(f"🎨 Theme: {theme.top_color} → {theme.bottom_color}")
    
    # Create canvas with explicit dark background
    canvas = tk.Canvas(root, bg=theme.bottom_color, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    def draw_gradient():
        # Clear canvas
        canvas.delete("all")
        
        # Get canvas dimensions
        canvas.update_idletasks()
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            root.after(100, draw_gradient)  # Try again
            return
            
        print(f"📐 Drawing gradient: {width}x{height}")
        
        # Create gradient
        colors = create_gradient_colors(theme, steps=height)
        
        # Draw gradient strips
        for i, color in enumerate(colors):
            y = i * height // len(colors)
            y_next = (i + 1) * height // len(colors)
            
            canvas.create_rectangle(
                0, y, width, y_next,
                fill=color, outline=color, width=0
            )
            
        print(f"✅ Gradient drawn with {len(colors)} strips")
        
        # Add test text
        canvas.create_text(
            width//2, height//2,
            text="GRADIENT TEST\\nTEMANO PLAVA → SVETLO SIVA",
            fill=theme.text_color,
            font=("Arial", 16, "bold"),
            justify=tk.CENTER
        )
    
    # Draw gradient after window is ready
    root.after(500, draw_gradient)
    
    # Bind resize
    canvas.bind('<Configure>', lambda e: draw_gradient())
    
    print("🔄 Starting main loop...")
    root.mainloop()
    print("🏁 Test completed")

if __name__ == "__main__":
    test_static_gradient()