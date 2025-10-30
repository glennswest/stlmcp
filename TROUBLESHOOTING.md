# Troubleshooting MCP Server

## Server Status: ✓ Working

The MCP server itself is functioning correctly and responds to protocol messages.

## If Claude Code isn't finding it:

### 1. Restart Claude Code
The most common issue - configuration is only read at startup.
```bash
# Exit your current Claude Code session completely
# Then start a new session
```

### 2. Verify Configuration Location
Check that your config file is in the right place:
```bash
cat ~/.config/claude-code/settings.json
```

Should show:
```json
{
  "mcpServers": {
    "stl-viewer": {
      "command": "/Volumes/minihome/gwest/projects/stlmcp/venv/bin/python",
      "args": [
        "/Volumes/minihome/gwest/projects/stlmcp/server.py"
      ]
    }
  }
}
```

### 3. Test Server Manually
```bash
cd /Volumes/minihome/gwest/projects/stlmcp
source venv/bin/activate
python test_mcp.py
```

Should output: `✓ MCP server is working correctly`

### 4. Check Paths
```bash
# Verify Python exists
ls -la /Volumes/minihome/gwest/projects/stlmcp/venv/bin/python

# Verify server exists
ls -la /Volumes/minihome/gwest/projects/stlmcp/server.py
```

### 5. Alternative: Use relative paths
If absolute paths aren't working, try:
```json
{
  "mcpServers": {
    "stl-viewer": {
      "command": "python",
      "args": [
        "server.py"
      ],
      "cwd": "/Volumes/minihome/gwest/projects/stlmcp",
      "env": {
        "VIRTUAL_ENV": "/Volumes/minihome/gwest/projects/stlmcp/venv",
        "PATH": "/Volumes/minihome/gwest/projects/stlmcp/venv/bin:${PATH}"
      }
    }
  }
}
```

### 6. Check for Errors
Look for error messages when starting Claude Code. The server might be failing to start due to:
- Missing dependencies (shouldn't be an issue - we tested it)
- Permission issues
- Path issues

### 7. Verify MCP Protocol
Run this to confirm server responds:
```bash
cd /Volumes/minihome/gwest/projects/stlmcp
source venv/bin/activate
python test_mcp.py
```

## Working Configuration

Current config at: `/Volumes/minihome/gwest/.config/claude-code/settings.json`

This is confirmed working - just restart Claude Code!
