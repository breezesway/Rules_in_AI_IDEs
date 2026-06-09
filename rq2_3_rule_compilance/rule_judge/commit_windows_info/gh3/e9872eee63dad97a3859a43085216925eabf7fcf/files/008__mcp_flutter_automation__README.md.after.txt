# MCP Flutter Automation Server

A Model Context Protocol (MCP) server for automating Flutter app operations including launching, debugging, screenshot capture, and inspection.

## Features

- **Launch Flutter Apps**: Start Flutter apps with debugging enabled
- **Hot Reload/Restart**: Trigger hot reload and hot restart
- **Log Capture**: Capture and stream app logs
- **Screenshot Capture**: Take screenshots via VM Service
- **Widget Inspector**: Access widget tree information
- **Device Management**: List available devices
- **Multi-app Support**: Manage multiple Flutter apps simultaneously

## Installation

```bash
cd mcp_flutter_automation
dart pub get
dart compile exe bin/mcp_flutter_automation.dart -o mcp_flutter_automation
```

## Configuration

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "flutter-automation": {
      "command": "/path/to/mcp_flutter_automation",
      "args": [],
      "env": {}
    }
  }
}
```

## Usage

### Available Tools

1. **launch_app**: Launch a Flutter app
   ```
   Parameters:
   - appId: Unique identifier for the app
   - projectPath: Path to Flutter project
   - targetFile: (optional) Target file to run
   - deviceId: (optional) Device to run on
   - vmServicePort: (optional) VM service port
   - ddsPort: (optional) DDS port
   ```

2. **hot_reload**: Perform hot reload
   ```
   Parameters:
   - appId: App identifier
   ```

3. **hot_restart**: Perform hot restart
   ```
   Parameters:
   - appId: App identifier
   ```

4. **stop_app**: Stop a running app
   ```
   Parameters:
   - appId: App identifier
   ```

5. **capture_screenshot**: Take a screenshot
   ```
   Parameters:
   - appId: App identifier
   ```

6. **get_logs**: Retrieve app logs
   ```
   Parameters:
   - appId: App identifier
   - count: (optional) Number of recent lines
   ```

7. **get_widget_tree**: Get widget tree information
   ```
   Parameters:
   - appId: App identifier
   ```

8. **list_apps**: List all managed apps

9. **get_app_info**: Get detailed app information
   ```
   Parameters:
   - appId: App identifier
   ```

### Available Resources

- `devices://list`: List available Flutter devices
- `flutter://doctor`: Flutter environment information

## Example Usage in Claude

```
User: Launch my Flutter app at /Users/me/my_app