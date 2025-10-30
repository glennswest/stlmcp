# STL MCP Server

An MCP (Model Context Protocol) server that enables Claude to load, examine, and manipulate STL files with camera controls and visualization capabilities.

## Features

- Load single or multiple STL files
- Camera positioning and rotation controls
- Screenshot capture with customizable settings
- Model information and measurements
- Color and opacity adjustments
- Distance measurements

## Installation

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python server.py
```

## Available Tools

### Loading and Management

- **load_stl**: Load an STL file with an optional name
- **list_models**: List all currently loaded models
- **get_model_info**: Get detailed information about a specific model
- **remove_model**: Remove a model from the scene
- **clear_all_models**: Remove all loaded models

### Camera Controls

- **set_camera**: Set camera position, focal point, and view direction
- **rotate_camera**: Rotate camera by azimuth, elevation, or roll
- **reset_view**: Reset camera to default view

### Visualization

- **take_screenshot**: Render and save the current view as PNG
- **set_model_color**: Change a model's color
- **set_model_opacity**: Adjust a model's transparency

### Measurements

- **measure_distance**: Calculate distance between two 3D points

## Example Usage with Claude

Once the server is running and configured in your MCP client:

```
Load the file /path/to/model.stl and take a screenshot from above
```

```
Load model1.stl as "part1" and model2.stl as "part2", set part1 to blue and part2 to red with 0.5 opacity
```

```
Rotate the camera 45 degrees around the vertical axis and take a screenshot
```

## Configuration

To use this server with Claude Desktop or other MCP clients, add to your MCP configuration:

```json
{
  "mcpServers": {
    "stl-viewer": {
      "command": "python",
      "args": ["/path/to/stlmcp/server.py"],
      "env": {
        "PYTHONPATH": "/path/to/stlmcp/venv/lib/python3.X/site-packages"
      }
    }
  }
}
```

Or use uvx for easier setup:

```json
{
  "mcpServers": {
    "stl-viewer": {
      "command": "uvx",
      "args": ["--from", "/path/to/stlmcp", "python", "server.py"]
    }
  }
}
```

## Dependencies

- vedo: 3D visualization and STL handling
- numpy: Numerical computations
- mcp: Model Context Protocol SDK
- vtk: Visualization Toolkit (installed with vedo)

## Notes

- The plotter runs in offscreen mode (no window appears)
- Screenshots are saved at 1920x1080 resolution by default
- All measurements are in the units used by the STL file
- Multiple models can be loaded and viewed simultaneously
