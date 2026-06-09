# MCP Flutter Automation - Claude Desktop Setup Guide

This guide will help you set up the MCP Flutter Automation server with Claude Desktop for automated Flutter app management.

## What This MCP Server Does

The MCP Flutter Automation server allows Claude to:
- **Launch Flutter apps** with custom configurations
- **Capture screenshots** of running Flutter apps
- **Hot reload/restart** apps during development
- **Get app logs** and debugging information
- **Inspect widget trees** for UI debugging
- **Manage multiple Flutter apps** simultaneously
- **List Flutter devices** and check Flutter doctor status

## Prerequisites

1. **Flutter SDK** - Must be installed and in your PATH
   ```bash
   flutter --version  # Should show Flutter version
   ```

2. **Claude Desktop** - Latest version installed

3. **This compiled MCP server** - Already compiled as `mcp_flutter_automation`

## Setup Instructions

### 1. Find Your Claude Desktop Configuration

**On macOS:**
```bash
# Open the config directory
open ~/Library/Application\ Support/Claude/
```

**On Windows:**
```bash
# Navigate to
%APPDATA%\Claude\
```

**On Linux:**
```bash
# Navigate to
~/.config/Claude/
```

### 2. Edit Claude Desktop Configuration

Open or create the file `claude_desktop_config.json` in the config directory and add this MCP server configuration:

```json
{
  "mcpServers": {
    "flutter-automation": {
      "command": "/path/to/project/mcp_flutter_automation/run_mcp_server.sh",
      "args": [],
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**⚠️ Important:** Replace the path `/path/to/project/mcp_flutter_automation/` with the actual path where you have this project.

### 3. Alternative Direct Executable Configuration

If you prefer to use the executable directly (without the shell script):

```json
{
  "mcpServers": {
    "flutter-automation": {
      "command": "/path/to/project/mcp_flutter_automation/mcp_flutter_automation",
      "args": [],
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### 4. Restart Claude Desktop

After saving the configuration file, completely quit and restart Claude Desktop for the changes to take effect.

### 5. Verify Setup

Once Claude Desktop restarts, you should be able to use commands like:

- "Launch a Flutter app from /path/to/my/flutter/project"
- "Take a screenshot of the running Flutter app"
- "Hot reload the Flutter app"
- "Show me the Flutter app logs"
- "List available Flutter devices"

## Available MCP Tools

The server provides these tools to Claude:

| Tool | Description |
|------|-------------|
| `launch_app` | Launch a Flutter app with custom settings |
| `hot_reload` | Perform hot reload on a running app |
| `hot_restart` | Perform hot restart on a running app |
| `stop_app` | Stop a running Flutter app |
| `capture_screenshot` | Take a screenshot of the app UI |
| `get_logs` | Retrieve app logs with optional count limit |
| `get_widget_tree` | Get the Flutter widget tree for debugging |
| `list_apps` | List all managed Flutter apps |
| `get_app_info` | Get detailed information about a specific app |

## Available MCP Resources

| Resource | Description |
|----------|-------------|
| `devices://list` | List all available Flutter devices |
| `flutter://doctor` | Get Flutter doctor diagnostic information |

## Example Usage with Claude

Here are some example commands you can try:

### Launch a Flutter App
```
"Launch a Flutter app from the project at /path/to/my/flutter/project with app ID 'my-demo-app'"
```

### Development Workflow
```
"Hot reload the app 'my-demo-app' and then take a screenshot"
```

### Debugging
```
"Show me the recent logs for app 'my-demo-app' and get the widget tree"
```

### Device Management
```
"List all available Flutter devices and show Flutter doctor status"
```

## Troubleshooting

### 1. MCP Server Not Starting
- Check that the path in `claude_desktop_config.json` is correct
- Ensure the executable has proper permissions: `chmod +x mcp_flutter_automation`
- Verify Flutter is in your PATH: `flutter --version`

### 2. App Launch Issues
- Make sure you're providing valid Flutter project paths
- Ensure no other Flutter processes are using the same ports
- Check that your Flutter project has a valid `pubspec.yaml`

### 3. Screenshot/Widget Tree Issues
- These features require the Flutter app to be running with VM service enabled
- The app must be launched through this MCP server (not separately)
- Ensure the Flutter app includes the Flutter Inspector

### 4. Log Output
To see detailed logs from the MCP server, you can set the log level:

```json
{
  "mcpServers": {
    "flutter-automation": {
      "command": "/path/to/run_mcp_server.sh",
      "args": [],
      "env": {
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

### 5. Port Conflicts
If you need to use custom ports (default: VM Service 8182, DDS 8181):

```
"Launch app 'my-app' from /path/to/project with VM service port 9182 and DDS port 9181"
```

## Server Architecture

- **Language**: Dart (compiled to native executable)
- **Protocol**: Model Context Protocol (MCP)
- **Flutter Integration**: VM Service API for debugging and inspection
- **Process Management**: Direct Flutter CLI process control
- **Concurrency**: Supports multiple simultaneous Flutter apps

## Development

If you want to modify the server:

1. Edit the Dart source code in this project
2. Run tests: `dart test`
3. Recompile: `dart compile exe bin/mcp_flutter_automation.dart -o mcp_flutter_automation`
4. Restart Claude Desktop to use the updated server

## Support

This MCP server provides comprehensive Flutter automation capabilities for Claude Desktop, enabling seamless Flutter development workflows through natural language commands.