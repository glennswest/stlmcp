# Claude Code Setup

## For Claude Code CLI

To use this MCP server with Claude Code, configure it in your MCP settings.

### Configuration File Location

Claude Code typically stores MCP configuration in:
- **macOS/Linux**: `~/.config/claude/mcp_settings.json`
- **Or check**: `claude mcp list` to see current servers

### Add the Server

Create or edit your MCP configuration file:

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

### Alternative: Use in Current Session

You can also start the server manually and connect to it:

```bash
# In one terminal:
cd /Volumes/minihome/gwest/projects/stlmcp
source venv/bin/activate
python server.py
```

Then in Claude Code, the MCP tools should be available if the server is running.

### Quick Test

Once configured, you can test with:

```
Load the STL file test_stls/cube.stl and show me its info
```

### Available Tools

The server exposes these 12 tools to Claude:
- `load_stl` - Load STL files
- `list_models` - List all loaded models
- `get_model_info` - Get model details
- `remove_model` - Remove a model
- `clear_all_models` - Clear all models
- `set_camera` - Position camera
- `rotate_camera` - Rotate camera
- `reset_view` - Reset view
- `take_screenshot` - Save PNG screenshot
- `set_model_color` - Change color
- `set_model_opacity` - Set transparency
- `measure_distance` - Measure distances

All test STL files are in: `/Volumes/minihome/gwest/projects/stlmcp/test_stls/`
