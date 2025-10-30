#!/usr/bin/env python3
"""
STL MCP Server - Load and examine STL files with camera controls
"""

import json
import os
from typing import Any
import vedo
import numpy as np
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("STL Viewer")

# Global state to store loaded meshes and plotter
state = {
    "meshes": {},  # name -> vedo.Mesh
    "plotter": None,
    "camera_position": None,
    "camera_focal_point": None,
    "camera_view_up": None,
}


def ensure_plotter():
    """Ensure plotter is initialized"""
    if state["plotter"] is None:
        state["plotter"] = vedo.Plotter(offscreen=True, size=(1920, 1080))
    return state["plotter"]


@mcp.tool()
def load_stl(file_path: str, name: str = None) -> str:
    """
    Load an STL file for viewing and analysis.

    Args:
        file_path: Path to the STL file
        name: Optional name for the loaded mesh (defaults to filename)

    Returns:
        Information about the loaded mesh
    """
    if not os.path.exists(file_path):
        return f"Error: File not found: {file_path}"

    if not file_path.lower().endswith('.stl'):
        return f"Error: File must be an STL file: {file_path}"

    # Use filename if no name provided
    if name is None:
        name = os.path.basename(file_path).replace('.stl', '')

    try:
        # Load the STL file
        mesh = vedo.Mesh(file_path)
        state["meshes"][name] = mesh

        # Get mesh information
        bounds = mesh.bounds()
        center = mesh.center_of_mass()
        n_points = mesh.npoints
        n_cells = mesh.ncells
        volume = mesh.volume()

        info = {
            "name": name,
            "file": file_path,
            "vertices": n_points,
            "faces": n_cells,
            "volume": float(volume),
            "center_of_mass": [float(x) for x in center],
            "bounds": {
                "x": [float(bounds[0]), float(bounds[1])],
                "y": [float(bounds[2]), float(bounds[3])],
                "z": [float(bounds[4]), float(bounds[5])],
            }
        }

        return f"Successfully loaded '{name}':\n{json.dumps(info, indent=2)}"

    except Exception as e:
        return f"Error loading STL file: {str(e)}"


@mcp.tool()
def list_models() -> str:
    """
    List all currently loaded models.

    Returns:
        List of loaded model names
    """
    if not state["meshes"]:
        return "No models currently loaded."

    models = []
    for name, mesh in state["meshes"].items():
        models.append({
            "name": name,
            "vertices": mesh.npoints,
            "faces": mesh.ncells,
            "volume": float(mesh.volume())
        })

    return json.dumps(models, indent=2)


@mcp.tool()
def get_model_info(name: str) -> str:
    """
    Get detailed information about a loaded model.

    Args:
        name: Name of the model

    Returns:
        Detailed information about the model
    """
    if name not in state["meshes"]:
        return f"Error: Model '{name}' not found. Available models: {list(state['meshes'].keys())}"

    mesh = state["meshes"][name]
    bounds = mesh.bounds()
    center = mesh.center_of_mass()

    info = {
        "name": name,
        "vertices": mesh.npoints,
        "faces": mesh.ncells,
        "volume": float(mesh.volume()),
        "center_of_mass": [float(x) for x in center],
        "bounds": {
            "x": [float(bounds[0]), float(bounds[1])],
            "y": [float(bounds[2]), float(bounds[3])],
            "z": [float(bounds[4]), float(bounds[5])],
        },
        "diagonal_length": float(mesh.diagonal_size()),
    }

    return json.dumps(info, indent=2)


@mcp.tool()
def set_camera(
    position: list[float] = None,
    focal_point: list[float] = None,
    view_up: list[float] = None,
    zoom: float = None
) -> str:
    """
    Set camera position and orientation.

    Args:
        position: Camera position [x, y, z]
        focal_point: Point the camera is looking at [x, y, z]
        view_up: Camera up direction [x, y, z]
        zoom: Zoom factor (default: 1.0)

    Returns:
        Confirmation message
    """
    plt = ensure_plotter()

    if position:
        state["camera_position"] = position
    if focal_point:
        state["camera_focal_point"] = focal_point
    if view_up:
        state["camera_view_up"] = view_up

    camera = plt.camera
    if position:
        camera.SetPosition(*position)
    if focal_point:
        camera.SetFocalPoint(*focal_point)
    if view_up:
        camera.SetViewUp(*view_up)
    if zoom:
        camera.Zoom(zoom)

    return f"Camera updated: position={position}, focal_point={focal_point}, view_up={view_up}, zoom={zoom}"


@mcp.tool()
def rotate_camera(azimuth: float = 0, elevation: float = 0, roll: float = 0) -> str:
    """
    Rotate the camera by specified angles.

    Args:
        azimuth: Rotation around the vertical axis (degrees)
        elevation: Rotation around the horizontal axis (degrees)
        roll: Roll rotation (degrees)

    Returns:
        Confirmation message
    """
    plt = ensure_plotter()

    if azimuth != 0:
        plt.camera.Azimuth(azimuth)
    if elevation != 0:
        plt.camera.Elevation(elevation)
    if roll != 0:
        plt.camera.Roll(roll)

    return f"Camera rotated: azimuth={azimuth}°, elevation={elevation}°, roll={roll}°"


@mcp.tool()
def take_screenshot(output_path: str, show_axes: bool = True, background_color: str = "white") -> str:
    """
    Render the current scene and save a screenshot.

    Args:
        output_path: Path where to save the screenshot (PNG format)
        show_axes: Whether to show coordinate axes
        background_color: Background color (e.g., 'white', 'black', 'gray')

    Returns:
        Path to saved screenshot
    """
    if not state["meshes"]:
        return "Error: No models loaded. Load an STL file first."

    plt = ensure_plotter()
    plt.clear()

    # Add all meshes to the plotter
    meshes_to_show = list(state["meshes"].values())

    # Set background
    plt.background(background_color)

    # Add meshes
    for mesh in meshes_to_show:
        plt.add(mesh)

    # Add axes if requested
    if show_axes:
        axes = vedo.Axes(
            list(state["meshes"].values())[0],
            xtitle='X', ytitle='Y', ztitle='Z'
        )
        plt.add(axes)

    # Restore camera settings if they exist
    if state["camera_position"]:
        plt.camera.SetPosition(*state["camera_position"])
    if state["camera_focal_point"]:
        plt.camera.SetFocalPoint(*state["camera_focal_point"])
    if state["camera_view_up"]:
        plt.camera.SetViewUp(*state["camera_view_up"])

    # Render and save
    try:
        plt.show(interactive=False)
        plt.screenshot(output_path)
        return f"Screenshot saved to: {output_path}"
    except Exception as e:
        return f"Error saving screenshot: {str(e)}"


@mcp.tool()
def measure_distance(model_name: str, point1: list[float], point2: list[float]) -> str:
    """
    Measure the distance between two points.

    Args:
        model_name: Name of the model (for reference)
        point1: First point [x, y, z]
        point2: Second point [x, y, z]

    Returns:
        Distance between the points
    """
    if model_name not in state["meshes"]:
        return f"Error: Model '{model_name}' not found"

    p1 = np.array(point1)
    p2 = np.array(point2)
    distance = np.linalg.norm(p2 - p1)

    return f"Distance between {point1} and {point2}: {float(distance):.4f} units"


@mcp.tool()
def reset_view() -> str:
    """
    Reset the camera to default view showing all models.

    Returns:
        Confirmation message
    """
    if not state["meshes"]:
        return "Error: No models loaded"

    plt = ensure_plotter()
    plt.clear()

    # Add all meshes
    for mesh in state["meshes"].values():
        plt.add(mesh)

    # Reset camera
    plt.reset_camera()

    # Clear camera state
    state["camera_position"] = None
    state["camera_focal_point"] = None
    state["camera_view_up"] = None

    return "View reset to default"


@mcp.tool()
def remove_model(name: str) -> str:
    """
    Remove a loaded model from the scene.

    Args:
        name: Name of the model to remove

    Returns:
        Confirmation message
    """
    if name not in state["meshes"]:
        return f"Error: Model '{name}' not found. Available models: {list(state['meshes'].keys())}"

    del state["meshes"][name]
    return f"Model '{name}' removed. Remaining models: {list(state['meshes'].keys())}"


@mcp.tool()
def clear_all_models() -> str:
    """
    Remove all loaded models.

    Returns:
        Confirmation message
    """
    count = len(state["meshes"])
    state["meshes"].clear()
    if state["plotter"]:
        state["plotter"].clear()

    return f"Cleared {count} model(s)"


@mcp.tool()
def set_model_color(name: str, color: str) -> str:
    """
    Set the color of a model.

    Args:
        name: Name of the model
        color: Color name (e.g., 'red', 'blue', 'green') or hex code

    Returns:
        Confirmation message
    """
    if name not in state["meshes"]:
        return f"Error: Model '{name}' not found"

    mesh = state["meshes"][name]
    mesh.color(color)

    return f"Model '{name}' color set to '{color}'"


@mcp.tool()
def set_model_opacity(name: str, opacity: float) -> str:
    """
    Set the opacity of a model.

    Args:
        name: Name of the model
        opacity: Opacity value between 0.0 (transparent) and 1.0 (opaque)

    Returns:
        Confirmation message
    """
    if name not in state["meshes"]:
        return f"Error: Model '{name}' not found"

    if not 0.0 <= opacity <= 1.0:
        return "Error: Opacity must be between 0.0 and 1.0"

    mesh = state["meshes"][name]
    mesh.alpha(opacity)

    return f"Model '{name}' opacity set to {opacity}"


if __name__ == "__main__":
    # Run the server
    mcp.run()
