#!/usr/bin/env python3
"""
Generate simple test STL files for testing the MCP server
"""

import vedo
import os


def create_test_stls(output_dir="test_stls"):
    """Create a few simple STL files for testing"""

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # 1. Cube
    cube = vedo.Cube(side=10)
    cube.write(os.path.join(output_dir, "cube.stl"))
    print(f"Created: {output_dir}/cube.stl")

    # 2. Sphere
    sphere = vedo.Sphere(r=5)
    sphere.write(os.path.join(output_dir, "sphere.stl"))
    print(f"Created: {output_dir}/sphere.stl")

    # 3. Cylinder
    cylinder = vedo.Cylinder(r=3, height=10)
    cylinder.write(os.path.join(output_dir, "cylinder.stl"))
    print(f"Created: {output_dir}/cylinder.stl")

    # 4. Torus
    torus = vedo.Torus(r1=8, r2=2)
    torus.write(os.path.join(output_dir, "torus.stl"))
    print(f"Created: {output_dir}/torus.stl")

    # 5. Cone
    cone = vedo.Cone(r=5, height=10)
    cone.write(os.path.join(output_dir, "cone.stl"))
    print(f"Created: {output_dir}/cone.stl")

    print(f"\nAll test STL files created in '{output_dir}/' directory")
    print(f"You can now test the server with these files!")


if __name__ == "__main__":
    create_test_stls()
