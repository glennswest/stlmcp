#!/usr/bin/env python3
"""
Example script demonstrating direct usage of the STL viewer functionality
(without MCP - for testing purposes)
"""

import os
import vedo

def main():
    """Demonstrate STL loading and visualization"""

    # Create test STLs if they don't exist
    if not os.path.exists("test_stls"):
        print("Creating test STL files...")
        from test_stl_generator import create_test_stls
        create_test_stls()

    print("\n=== STL Viewer Demo ===\n")

    # Load STL files
    print("Loading STL files...")
    cube = vedo.Mesh("test_stls/cube.stl")
    sphere = vedo.Mesh("test_stls/sphere.stl")

    # Get information
    print(f"\nCube info:")
    print(f"  Vertices: {cube.npoints}")
    print(f"  Faces: {cube.ncells}")
    print(f"  Volume: {cube.volume():.2f}")
    print(f"  Center: {cube.center_of_mass()}")

    print(f"\nSphere info:")
    print(f"  Vertices: {sphere.npoints}")
    print(f"  Faces: {sphere.ncells}")
    print(f"  Volume: {sphere.volume():.2f}")
    print(f"  Center: {sphere.center_of_mass()}")

    # Style the meshes
    cube.color("blue").alpha(0.8)
    sphere.color("red").alpha(0.9)

    # Position them side by side
    sphere.pos(15, 0, 0)

    # Create plotter
    print("\nCreating visualization...")
    plt = vedo.Plotter(offscreen=True, size=(1920, 1080))

    # Add objects
    plt.add(cube, sphere)

    # Add axes
    axes = vedo.Axes(cube, xtitle='X', ytitle='Y', ztitle='Z')
    plt.add(axes)

    # Set background
    plt.background('white')

    # Render
    plt.show(interactive=False)

    # Save screenshot
    output_file = "example_output.png"
    plt.screenshot(output_file)
    print(f"\nScreenshot saved to: {output_file}")

    # Different view - top down
    plt.camera.SetPosition(0, 0, 50)
    plt.camera.SetFocalPoint(7.5, 0, 0)
    plt.camera.SetViewUp(0, 1, 0)

    plt.show(interactive=False)
    plt.screenshot("example_output_topview.png")
    print(f"Top view saved to: example_output_topview.png")

    print("\n=== Demo Complete ===")
    print("Check the output PNG files to see the results!")


if __name__ == "__main__":
    main()
