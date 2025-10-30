#!/usr/bin/env python3
"""
Shape detection module for identifying geometric primitives in STL meshes.
Detects boxes, cylinders, spheres, rounded rectangles, and other common shapes.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
import vedo


class Shape:
    """Base class for detected shapes"""

    def __init__(self, shape_type: str, position: np.ndarray, params: Dict[str, Any], is_negative: bool = False):
        self.type = shape_type
        self.position = position
        self.params = params
        self.is_negative = is_negative
        self.confidence = 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert shape to dictionary representation"""
        return {
            "type": str(self.type),
            "position": self.position.tolist(),
            "params": self.params,
            "is_negative": bool(self.is_negative),
            "confidence": float(self.confidence)
        }

    def to_openscad(self) -> str:
        """Generate OpenSCAD code for this shape"""
        raise NotImplementedError("Subclasses must implement to_openscad()")


class Cylinder(Shape):
    """Cylindrical shape (can be hole or solid)"""

    def __init__(self, position: np.ndarray, radius: float, height: float,
                 axis: np.ndarray, is_negative: bool = False):
        params = {
            "radius": float(radius),
            "height": float(height),
            "axis": axis.tolist()
        }
        super().__init__("cylinder", position, params, is_negative)

    def to_openscad(self) -> str:
        """Generate OpenSCAD code"""
        r = self.params["radius"]
        h = self.params["height"]
        pos = self.position
        axis = np.array(self.params["axis"])

        # Calculate rotation from Z axis to desired axis
        z_axis = np.array([0, 0, 1])
        if not np.allclose(axis, z_axis):
            rotation = self._axis_to_rotation(axis)
            rot_str = f"rotate({rotation})"
        else:
            rot_str = ""

        code = f"translate([{pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}])\n"
        if rot_str:
            code += f"  {rot_str}\n"
        code += f"  cylinder(r={r:.3f}, h={h:.3f}, center=true);"

        return code

    def _axis_to_rotation(self, axis: np.ndarray) -> str:
        """Convert axis vector to OpenSCAD rotation"""
        # Simplified rotation calculation
        axis = axis / np.linalg.norm(axis)
        z_axis = np.array([0, 0, 1])

        # Cross product gives rotation axis
        rot_axis = np.cross(z_axis, axis)
        if np.linalg.norm(rot_axis) < 1e-6:
            return "[0, 0, 0]"

        rot_axis = rot_axis / np.linalg.norm(rot_axis)

        # Dot product gives angle
        angle = np.arccos(np.clip(np.dot(z_axis, axis), -1, 1))
        angle_deg = np.degrees(angle)

        return f"[{rot_axis[0]*angle_deg:.3f}, {rot_axis[1]*angle_deg:.3f}, {rot_axis[2]*angle_deg:.3f}]"


class Box(Shape):
    """Rectangular box shape"""

    def __init__(self, position: np.ndarray, dimensions: np.ndarray,
                 rotation: np.ndarray = None, is_negative: bool = False):
        params = {
            "dimensions": dimensions.tolist(),
            "rotation": rotation.tolist() if rotation is not None else [0, 0, 0]
        }
        super().__init__("box", position, params, is_negative)

    def to_openscad(self) -> str:
        """Generate OpenSCAD code"""
        pos = self.position
        dims = self.params["dimensions"]
        rot = self.params["rotation"]

        code = f"translate([{pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}])\n"
        if not np.allclose(rot, [0, 0, 0]):
            code += f"  rotate([{rot[0]:.3f}, {rot[1]:.3f}, {rot[2]:.3f}])\n"
        code += f"  cube([{dims[0]:.3f}, {dims[1]:.3f}, {dims[2]:.3f}], center=true);"

        return code


class RoundedBox(Shape):
    """Box with rounded corners"""

    def __init__(self, position: np.ndarray, dimensions: np.ndarray,
                 corner_radius: float, rotation: np.ndarray = None, is_negative: bool = False):
        params = {
            "dimensions": dimensions.tolist(),
            "corner_radius": float(corner_radius),
            "rotation": rotation.tolist() if rotation is not None else [0, 0, 0]
        }
        super().__init__("rounded_box", position, params, is_negative)

    def to_openscad(self) -> str:
        """Generate OpenSCAD code"""
        pos = self.position
        dims = self.params["dimensions"]
        r = self.params["corner_radius"]
        rot = self.params["rotation"]

        code = f"translate([{pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}])\n"
        if not np.allclose(rot, [0, 0, 0]):
            code += f"  rotate([{rot[0]:.3f}, {rot[1]:.3f}, {rot[2]:.3f}])\n"
        code += f"  minkowski() {{\n"
        code += f"    cube([{dims[0]-2*r:.3f}, {dims[1]-2*r:.3f}, {dims[2]-2*r:.3f}], center=true);\n"
        code += f"    sphere(r={r:.3f});\n"
        code += f"  }}"

        return code


class Sphere(Shape):
    """Spherical shape"""

    def __init__(self, position: np.ndarray, radius: float, is_negative: bool = False):
        params = {"radius": float(radius)}
        super().__init__("sphere", position, params, is_negative)

    def to_openscad(self) -> str:
        """Generate OpenSCAD code"""
        pos = self.position
        r = self.params["radius"]

        return f"translate([{pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}])\n  sphere(r={r:.3f});"


class ShapeDetector:
    """Detects geometric primitives in STL meshes"""

    def __init__(self, mesh: vedo.Mesh, tolerance: float = 0.1):
        self.mesh = mesh
        self.tolerance = tolerance
        self.detected_shapes: List[Shape] = []

    def detect_all(self) -> List[Shape]:
        """Run all detection algorithms"""
        self.detected_shapes = []

        # Detect different shape types
        self.detect_cylinders()
        self.detect_boxes()
        self.detect_spheres()

        return self.detected_shapes

    def detect_cylinders(self) -> List[Cylinder]:
        """Detect cylindrical features (holes and solids)"""
        cylinders = []

        # Get mesh data
        points = self.mesh.points
        if callable(points):
            points = points()
        points = np.array(points)

        # Try to detect cylinders along each axis
        for axis_idx, axis_name in enumerate(['X', 'Y', 'Z']):
            axis = np.zeros(3)
            axis[axis_idx] = 1.0

            # Project points onto plane perpendicular to axis
            other_axes = [i for i in range(3) if i != axis_idx]
            projected = points[:, other_axes]

            # Find circular patterns
            if len(projected) < 10:
                continue

            # Compute center of projected points
            center_2d = np.mean(projected, axis=0)

            # Compute distances from center
            distances = np.linalg.norm(projected - center_2d, axis=1)

            # Check if distances are relatively uniform (indicating a cylinder)
            mean_dist = np.mean(distances)
            std_dist = np.std(distances)

            if std_dist < self.tolerance * mean_dist and mean_dist > 0.1:
                # Found a potential cylinder
                radius = mean_dist

                # Find height along axis
                axis_coords = points[:, axis_idx]
                height = np.max(axis_coords) - np.min(axis_coords)

                # Compute center position
                center_3d = np.mean(points, axis=0)

                # Check if this is a hole (negative space) by checking if it's inside the mesh
                is_negative = self._is_hole(center_3d, radius)

                cyl = Cylinder(center_3d, radius, height, axis, is_negative)
                cylinders.append(cyl)

        self.detected_shapes.extend(cylinders)
        return cylinders

    def detect_boxes(self) -> List[Box]:
        """Detect box-shaped features"""
        boxes = []

        # Get bounding box
        bounds = self.mesh.bounds()

        # Check if the mesh itself is box-like
        if self._is_box_shaped():
            dimensions = np.array([
                bounds[1] - bounds[0],  # X
                bounds[3] - bounds[2],  # Y
                bounds[5] - bounds[4],  # Z
            ])
            center = np.array([
                (bounds[0] + bounds[1]) / 2,
                (bounds[2] + bounds[3]) / 2,
                (bounds[4] + bounds[5]) / 2,
            ])

            box = Box(center, dimensions)
            boxes.append(box)

        self.detected_shapes.extend(boxes)
        return boxes

    def detect_spheres(self) -> List[Sphere]:
        """Detect spherical features"""
        spheres = []

        points = self.mesh.points
        if callable(points):
            points = points()
        points = np.array(points)

        if len(points) == 0:
            return spheres

        center = np.mean(points, axis=0)

        # Compute distances from center
        distances = np.linalg.norm(points - center, axis=1)
        mean_dist = np.mean(distances)
        std_dist = np.std(distances)

        # If most points are equidistant from center, it's a sphere
        if std_dist < self.tolerance * mean_dist:
            sphere = Sphere(center, mean_dist)
            spheres.append(sphere)

        self.detected_shapes.extend(spheres)
        return spheres

    def _is_box_shaped(self) -> bool:
        """Check if mesh is approximately box-shaped"""
        # Get vertices and check if they cluster around 8 corners
        points = self.mesh.points
        if callable(points):
            points = points()
        points = np.array(points)

        if len(points) == 0:
            return False

        bounds = self.mesh.bounds()

        # Generate 8 corner positions
        corners = np.array([
            [bounds[0], bounds[2], bounds[4]],
            [bounds[1], bounds[2], bounds[4]],
            [bounds[0], bounds[3], bounds[4]],
            [bounds[1], bounds[3], bounds[4]],
            [bounds[0], bounds[2], bounds[5]],
            [bounds[1], bounds[2], bounds[5]],
            [bounds[0], bounds[3], bounds[5]],
            [bounds[1], bounds[3], bounds[5]],
        ])

        # Check how many vertices are near corners
        near_corner_count = 0
        for point in points:
            min_dist = min(np.linalg.norm(point - corner) for corner in corners)
            if min_dist < self.tolerance:
                near_corner_count += 1

        # If significant portion of vertices are near corners, it's box-like
        return near_corner_count / len(points) > 0.3

    def _is_hole(self, center: np.ndarray, radius: float) -> bool:
        """
        Determine if a cylindrical feature is a hole (negative space)
        by checking if the center is inside the mesh
        """
        # Simple heuristic: check if center point is very close to mesh surface
        # If it's inside a hole, it should be far from the surface
        try:
            closest_point = self.mesh.closest_point(center)
            if callable(closest_point):
                closest_point = closest_point()
            closest_point = np.array(closest_point)
            distance = np.linalg.norm(center - closest_point)
        except:
            # If we can't determine, assume it's not a hole
            return False

        # If the center is more than radius away from surface, likely a hole
        return distance > radius * 0.5

    def generate_openscad(self) -> str:
        """Generate OpenSCAD code for all detected shapes"""
        if not self.detected_shapes:
            return "// No shapes detected"

        code = "// Generated by STL Shape Detector\n\n"

        # Separate positive and negative shapes
        positive = [s for s in self.detected_shapes if not s.is_negative]
        negative = [s for s in self.detected_shapes if s.is_negative]

        if positive and negative:
            code += "difference() {\n"
            code += "  union() {\n"
            for shape in positive:
                code += "    " + shape.to_openscad().replace("\n", "\n    ") + "\n"
            code += "  }\n"
            code += "  union() {\n"
            for shape in negative:
                code += "    " + shape.to_openscad().replace("\n", "\n    ") + "\n"
            code += "  }\n"
            code += "}\n"
        elif positive:
            code += "union() {\n"
            for shape in positive:
                code += "  " + shape.to_openscad().replace("\n", "\n  ") + "\n"
            code += "}\n"
        else:
            # Only negative shapes (unusual)
            for shape in negative:
                code += shape.to_openscad() + "\n"

        return code
