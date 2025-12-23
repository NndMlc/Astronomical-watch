"""
Main application demonstrating Widget and Normal Mode integration.
Shows full click activation and consistent gradient backgrounds.
"""
from __future__ import annotations
import tkinter as tk
import os
from .widget import create_widget
from .normal_mode import create_normal_mode
from .theme_manager import update_shared_theme


class AstronomicalWatchApp:
    """Main application managing Widget and Normal Mode windows."""
    
    def __init__(self, enable_ntp_sync: bool = True):
        # Initialize shared theme immediately
        update_shared_theme()
        
        # Start NTP time synchronization (optional, runs in background)
        if enable_ntp_sync:
            self._start_time_sync()
        
        self.widget_root = None
        self.normal_root = None
        self.widget = None
        self.normal_mode = None
        self.current_language = "en"
    
    def _start_time_sync(self):
        """Initialize NTP time synchronization."""
        try:
            from astronomical_watch.net.time_sync import update_time_sync, start_periodic_sync
            
            # Do initial sync
            print("🕐 Initializing NTP time synchronization...")
            if update_time_sync(force=True):
                # Start periodic sync every 60 minutes
                start_periodic_sync(interval_minutes=60)
            else:
                print("⚠️  Initial NTP sync failed, will retry automatically")
                # Still start periodic sync - it will retry
                start_periodic_sync(interval_minutes=60)
        except ImportError:
            print("⚠️  NTP sync module not available")
        except Exception as e:
            print(f"⚠️  Could not start NTP sync: {e}")
    
    def _set_icon(self, window):
        """Set application icon for a window."""
        try:
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))
            icon_path = os.path.join(project_root, "icons", "astronomical_watch.ico")
            
            if os.path.exists(icon_path):
                window.iconbitmap(icon_path)
            else:
                # Try PNG format
                png_path = os.path.join(project_root, "icons", "astronomical_watch.png")
                if os.path.exists(png_path):
                    img = tk.PhotoImage(file=png_path)
                    window.iconphoto(True, img)
                    # Keep reference to prevent garbage collection
                    if not hasattr(self, '_icon_images'):
                        self._icon_images = []
                    self._icon_images.append(img)
        except Exception:
            pass
    
    def show_widget(self):
        """Show the widget window."""
        if self.widget_root is None:
            self.widget_root = tk.Tk()
            self.widget_root.title("Astronomical Watch")
            self.widget_root.protocol("WM_DELETE_WINDOW", self.on_widget_close)
            
            # Set icon
            self._set_icon(self.widget_root)
            
            # Create widget with click handler to open normal mode
            self.widget = create_widget(self.widget_root, self.open_normal_mode)
            self.widget.start_updates()
            
            print("✅ Widget started")
            print("🖱️  Double-click widget to open Normal Mode")
            print("🖱️  Right-click widget for context menu")
    
    def open_normal_mode(self):
        """Open Normal Mode window (triggered by widget click)."""
        print("🔄 Opening Normal Mode...")
        
        if self.normal_root is None:
            self.normal_root = tk.Toplevel()
            self.normal_root.title("Astronomical Watch - Normal Mode")
            self.normal_root.protocol("WM_DELETE_WINDOW", self.on_normal_close)
            
            # Set icon
            self._set_icon(self.normal_root)
            
            # Create normal mode with language sync and widget reference
            self.normal_mode = create_normal_mode(
                self.normal_root, 
                on_back=self.close_normal_mode,
                on_language=self.on_language_change,
                widget_ref=self.widget  # Pass widget reference
            )
            self.normal_mode.start_updates()
            
            print("✅ Normal Mode opened")
        else:
            # Bring to front if already open
            try:
                # Check if window still exists
                self.normal_root.winfo_exists()
                self.normal_root.deiconify()
                self.normal_root.lift()
                self.normal_root.focus_force()
                print("📱 Normal Mode brought to front")
            except tk.TclError:
                # Window was destroyed, clean up and reopen
                print("🔄 Previous window destroyed, creating new one...")
                self.normal_root = None
                self.normal_mode = None
                self.open_normal_mode()  # Recursive call to create new window
    
    def close_normal_mode(self):
        """Close normal mode and return to widget."""
        if self.normal_root:
            self.normal_root.destroy()
            self.normal_root = None
            self.normal_mode = None
            print("📴 Normal Mode closed")
    
    def on_language_change(self, new_language):
        """Handle language change from normal mode."""
        self.current_language = new_language
        if self.widget:
            self.widget.set_language(new_language)
        print(f"🌍 Language changed to: {new_language}")
    
    def on_widget_close(self):
        """Handle widget window close."""
        if self.widget:
            self.widget.stop_updates()
            
        if self.normal_root:
            self.normal_root.destroy()
            self.normal_root = None
            self.normal_mode = None
        
        self.widget_root.destroy()
        self.widget_root = None
        self.widget = None
        print("👋 Application closed")
    
    def on_normal_close(self):
        """Handle normal mode window close."""
        if self.normal_mode:
            self.normal_mode.stop_updates()
            
        # Don't call destroy here - let the window manager handle it
        # Just clean up our references so it can be reopened
        self.normal_root = None
        self.normal_mode = None
        print("📴 Normal Mode closed")
    
    def run(self):
        """Start the application."""
        print("=" * 50)
        print(" ASTRONOMICAL WATCH APPLICATION")
        print("=" * 50)
        print("Starting integrated astronomical timekeeping system...")
        print()
        
        self.show_widget()
        
        if self.widget_root:
            try:
                self.widget_root.mainloop()
            except KeyboardInterrupt:
                print("\n👋 Application interrupted by user")
                self.on_widget_close()


def main():
    """Main entry point."""
    try:
        app = AstronomicalWatchApp()
        app.run()
    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    exit(main())