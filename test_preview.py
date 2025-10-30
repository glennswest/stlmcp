#!/usr/bin/env python3
"""
Test script for the preview window functionality
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import (
    load_stl, toggle_preview, set_camera, rotate_camera,
    set_model_color, reset_view, state
)
import time

def test_preview():
    """Test the preview window with a simple STL file"""

    print("Testing STL Preview Window")
    print("=" * 50)

    # First, we need an STL file to test with
    print("\n1. Checking for test STL files...")
    test_files = [
        "test.stl",
        "sample.stl",
        "model.stl",
    ]

    stl_file = None
    for test_file in test_files:
        if os.path.exists(test_file):
            stl_file = test_file
            break

    if not stl_file:
        print("No test STL file found. Creating a simple cube...")
        # Create a simple cube STL for testing
        import vedo
        cube = vedo.Cube(side=10)
        stl_file = "test_cube.stl"
        cube.write(stl_file)
        print(f"Created {stl_file}")

    # Load the STL
    print(f"\n2. Loading STL file: {stl_file}")
    result = load_stl(stl_file, "test_model")
    print(result)

    # Enable preview window
    print("\n3. Enabling preview window...")
    result = toggle_preview(True)
    print(result)
    print("   Preview window should now be visible!")

    # Wait a bit for user to see the window
    time.sleep(2)

    # Test camera rotations
    print("\n4. Testing camera rotations...")
    for i in range(8):
        print(f"   Rotation {i+1}/8: Azimuth +45°")
        rotate_camera(azimuth=45)
        time.sleep(0.5)

    # Reset view
    print("\n5. Resetting view...")
    reset_view()
    time.sleep(1)

    # Test color changes
    print("\n6. Testing color changes...")
    colors = ["red", "green", "blue", "yellow", "cyan", "magenta"]
    for color in colors:
        print(f"   Setting color to {color}")
        set_model_color("test_model", color)
        time.sleep(0.5)

    # Reset to original color
    set_model_color("test_model", "lightgray")

    # Test camera positions
    print("\n7. Testing different camera views...")
    views = [
        {"name": "Front", "position": [0, -50, 0], "focal_point": [0, 0, 0]},
        {"name": "Top", "position": [0, 0, 50], "focal_point": [0, 0, 0]},
        {"name": "Side", "position": [50, 0, 0], "focal_point": [0, 0, 0]},
        {"name": "Isometric", "position": [30, -30, 30], "focal_point": [0, 0, 0]},
    ]

    for view in views:
        print(f"   Setting view to {view['name']}")
        set_camera(position=view['position'], focal_point=view['focal_point'])
        time.sleep(1)

    print("\n" + "=" * 50)
    print("Test complete! The preview window should still be open.")
    print("Close the window manually or press Ctrl+C to exit.")
    print("=" * 50)

    # Keep the script running so the window stays open
    try:
        while state["preview_enabled"]:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        toggle_preview(False)

if __name__ == "__main__":
    test_preview()
