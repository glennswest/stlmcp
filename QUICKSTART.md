# Quick Start Guide

## 1. Setup

```bash
# Activate virtual environment
source venv/bin/activate

# Generate test STL files
python test_stl_generator.py
```

## 2. Running the Server

```bash
python server.py
```

The server will start and be ready to accept MCP connections.

## 3. Configure in Claude Desktop

Add this to your Claude Desktop MCP configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "stl-viewer": {
      "command": "/Volumes/minihome/gwest/projects/stlmcp/venv/bin/python",
      "args": ["/Volumes/minihome/gwest/projects/stlmcp/server.py"]
    }
  }
}
```

## 4. Example Commands to Try with Claude

Once configured, you can ask Claude:

### Basic Loading
```
Load the file test_stls/cube.stl
```

### Multiple Models
```
Load test_stls/sphere.stl as "ball" and test_stls/cube.stl as "box"
```

### Visualization
```
Take a screenshot of all loaded models and save it to output.png
```

### Camera Control
```
Rotate the camera 45 degrees around the vertical axis and 30 degrees elevation, then take a screenshot
```

### Model Information
```
What are the dimensions of the cube model?
```

### Styling
```
Set the sphere to red color and the cube to blue with 0.5 opacity
```

### Measurements
```
Measure the distance from [0,0,0] to [10,10,10] in the cube model
```

## 5. Available Test Files

After running `test_stl_generator.py`, you'll have:
- `test_stls/cube.stl` - 10x10x10 cube
- `test_stls/sphere.stl` - Sphere with radius 5
- `test_stls/cylinder.stl` - Cylinder with radius 3, height 10
- `test_stls/torus.stl` - Torus with major radius 8, minor radius 2
- `test_stls/cone.stl` - Cone with radius 5, height 10

## Troubleshooting

### Server won't start
- Make sure the virtual environment is activated
- Check all dependencies are installed: `pip install -r requirements.txt`

### Can't see the server in Claude
- Verify the configuration file path is correct
- Restart Claude Desktop after adding the configuration
- Check the logs in Claude Desktop for any error messages

### Screenshots are blank
- Make sure you've loaded at least one STL file first
- Try using `reset_view` to reset the camera
