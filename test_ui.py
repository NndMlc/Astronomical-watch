import pytest

@pytest.mark.ui
def test_normal_mode_smoke():
    """
    Lightweight UI smoke test.

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
