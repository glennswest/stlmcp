#!/usr/bin/env python3
"""Test if MCP server is working"""

import subprocess
import json
import sys

# Start the server
proc = subprocess.Popen(
    ["/Volumes/minihome/gwest/projects/stlmcp/venv/bin/python",
     "/Volumes/minihome/gwest/projects/stlmcp/server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Send an MCP initialize request
initialize_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {
            "name": "test-client",
            "version": "1.0.0"
        }
    }
}

try:
    # Send request
    request_str = json.dumps(initialize_request) + "\n"
    proc.stdin.write(request_str)
    proc.stdin.flush()

    # Try to read response
    import select
    import time
    time.sleep(1)

    if proc.poll() is not None:
        stderr = proc.stderr.read()
        print(f"Server exited with code {proc.returncode}")
        print(f"STDERR: {stderr}")
        sys.exit(1)

    # Read stdout
    output = proc.stdout.readline()
    if output:
        print("Server responded!")
        print(f"Response: {output}")
        response = json.loads(output)
        if "result" in response:
            print("✓ MCP server is working correctly")
            print(f"Server name: {response['result'].get('serverInfo', {}).get('name', 'Unknown')}")
        else:
            print("Response doesn't contain expected result")
    else:
        print("No response from server")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    proc.terminate()
    proc.wait()
