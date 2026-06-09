#!/bin/bash

# MCP Flutter Automation Server Runner
# This script starts the MCP server with proper configuration

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXECUTABLE="$SCRIPT_DIR/mcp_flutter_automation"

# Check if the executable exists
if [ ! -f "$EXECUTABLE" ]; then
    echo "Error: mcp_flutter_automation executable not found at $EXECUTABLE"
    echo "Please compile it first with: dart compile exe bin/mcp_flutter_automation.dart -o mcp_flutter_automation"
    exit 1
fi

# Check if Flutter is available
if ! command -v flutter &> /dev/null; then
    echo "Warning: Flutter is not in PATH. The server will still work but some commands may fail."
fi

# Set up logging
export LOG_LEVEL="${LOG_LEVEL:-INFO}"

echo "Starting MCP Flutter Automation Server..."
echo "Executable: $EXECUTABLE"
echo "Log Level: $LOG_LEVEL"
echo "Working Directory: $(pwd)"
echo "----------------------------------------"

# Run the server
exec "$EXECUTABLE" "$@"