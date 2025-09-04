import pytest

@pytest.mark.ui
def test_normal_mode_smoke():
    """
    Lightweight UI smoke test.


def test_widget():
    """Test the widget UI."""
    print("Testing Widget UI...")
    from ui.widget import create_widget
    import tkinter as tk
    
    root = tk.Tk()
    root.title("Widget Test")
    root.geometry("250x120")
    
    def click_handler():
        print("Widget clicked! This would open Normal Mode.")
        # Test by showing current theme
        from ui.gradient import get_sky_theme
        theme = get_sky_theme()
        print(f"Current theme: {theme.top_color} -> {theme.bottom_color}")
    
    widget = create_widget(root, click_handler)
    widget.start_updates()
    
    # Run for a few seconds then close
    root.after(3000, lambda: root.quit())  # Close after 3 seconds
    
    Runs a minimal Tkinter loop to ensure normal mode constructs without exceptions.

    Skipped automatically if Tkinter is unavailable (headless CI environment).
    CI should normally exclude this with -k 'not ui'.
    """

    try:
        import tkinter as tk  # noqa: F401
    except Exception:
        import pytest
        pytest.skip("Tkinter not available")

    import tkinter as tk
    from ui.normal_mode import create_normal_mode

    root = tk.Tk()
    root.withdraw()  # do not show real window during smoke test
    normal_mode = create_normal_mode(root)
    normal_mode.start_updates()

    # Allow scheduled callbacks to run briefly.
    root.after(200, root.quit)
    root.mainloop()

    assert True  # If no exception occurred, test passes.
