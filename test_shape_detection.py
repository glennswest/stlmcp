#!/usr/bin/env python3
"""
Test shape detection on known geometric shapes
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import load_stl, scan_shapes, export_openscad
import vedo

print("Creating test shapes...")

# Test 1: Simple cube
print("\n=== Test 1: Cube ===")
cube = vedo.Cube(side=10)
cube_file = "test_cube_shape.stl"
cube.write(cube_file)

result = load_stl(cube_file, "cube")
print(result)

scan_result = scan_shapes("cube", tolerance=0.5)
print("\nScan results:")
print(scan_result)

# Export to OpenSCAD
export_openscad("cube", "test_cube.scad")
print("\n✓ Exported to test_cube.scad")

# Test 2: Cylinder
print("\n\n=== Test 2: Cylinder ===")
cylinder = vedo.Cylinder(r=5, height=20)
cyl_file = "test_cylinder_shape.stl"
cylinder.write(cyl_file)

result = load_stl(cyl_file, "cylinder")
print(result)

scan_result = scan_shapes("cylinder", tolerance=0.5)
print("\nScan results:")
print(scan_result)

export_openscad("cylinder", "test_cylinder.scad")
print("\n✓ Exported to test_cylinder.scad")

# Test 3: Sphere
print("\n\n=== Test 3: Sphere ===")
sphere = vedo.Sphere(r=8)
sphere_file = "test_sphere_shape.stl"
sphere.write(sphere_file)

result = load_stl(sphere_file, "sphere")
print(result)

scan_result = scan_shapes("sphere", tolerance=0.5)
print("\nScan results:")
print(scan_result)

export_openscad("sphere", "test_sphere.scad")
print("\n✓ Exported to test_sphere.scad")

# Test 4: Cube with cylindrical hole (difference operation)
print("\n\n=== Test 4: Cube with hole ===")
cube_base = vedo.Cube(side=20)
hole = vedo.Cylinder(r=3, height=25).rotate_x(90)
cube_with_hole = cube_base.boolean("-", hole)
hole_file = "test_cube_with_hole.stl"
cube_with_hole.write(hole_file)

result = load_stl(hole_file, "cube_with_hole")
print(result)

scan_result = scan_shapes("cube_with_hole", tolerance=0.3)
print("\nScan results:")
print(scan_result)

export_openscad("cube_with_hole", "test_cube_with_hole.scad")
print("\n✓ Exported to test_cube_with_hole.scad")

print("\n\n" + "="*60)
print("Testing complete!")
print("="*60)
print("\nGenerated files:")
print("  - test_cube.scad")
print("  - test_cylinder.scad")
print("  - test_sphere.scad")
print("  - test_cube_with_hole.scad")
print("\nYou can open these in OpenSCAD to verify the detection.")

# Cleanup STL files
import time
time.sleep(2)
os.unlink(cube_file)
os.unlink(cyl_file)
os.unlink(sphere_file)
os.unlink(hole_file)
