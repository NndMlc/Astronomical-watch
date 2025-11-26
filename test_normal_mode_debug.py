#!/usr/bin/env python3
"""
Debug test for Normal Mode functionality.
This script will test Normal Mode with detailed debug output.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_normal_mode():
    """Test Normal Mode creation with debug output."""
    print("🧪 NORMAL MODE DEBUG TEST")
    print("=" * 40)
    
    try:
        import tkinter as tk
        
        print("✅ Tkinter imported successfully")
        
        # Create root window
        root = tk.Tk()
        root.title("Debug Test")
        root.withdraw()  # Hide main window
        
        print("✅ Root window created")
        
        # Create toplevel for normal mode (like main.py does)
        toplevel = tk.Toplevel(root)
        toplevel.title("Normal Mode Test")
        
        print("✅ Toplevel window created")
        
        # Import our normal mode
        from astronomical_watch.ui.normal_mode import create_normal_mode
        
        print("✅ Normal mode module imported")
        
        # Create normal mode instance
        print("\n🚀 Creating Normal Mode...")
        print("-" * 30)
        
        normal_mode = create_normal_mode(toplevel)
        
        print("-" * 30)
        print("✅ Normal Mode created successfully!")
        
        # Test start_updates
        print("\n🔄 Testing start_updates...")
        normal_mode.start_updates()
        print("✅ start_updates completed")
        
        # Run for a short time to test updates
        print("\n⏱️ Running for 5 seconds to test updates...")
        
        def stop_test():
            print("\n🛑 Stopping test...")
            normal_mode.stop_updates()
            toplevel.destroy()
            root.quit()
            
        root.after(5000, stop_test)  # Stop after 5 seconds
        
        print("🎯 Normal Mode is running! Check for any error messages...")
        print("💡 This will auto-close in 5 seconds")
        
        # Start main loop
        root.mainloop()
        
        print("\n✅ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔬 NORMAL MODE FUNCTIONALITY TEST")
    print("=" * 50)
    print("This test will:")
    print("• Create a Normal Mode window")
    print("• Test initialization with debug output")
    print("• Test update cycle")
    print("• Auto-close after 5 seconds")
    print()
    
    success = test_normal_mode()
    
    if success:
        print("\n🎉 NORMAL MODE TEST PASSED!")
        print("Normal Mode is working correctly.")
    else:
        print("\n💥 NORMAL MODE TEST FAILED!")
        print("Check the error messages above for details.")
        sys.exit(1)