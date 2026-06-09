# MCP Flutter Automation - Claude Code Setup Guide

This guide will help you set up the MCP Flutter Automation server with **Claude Code** (the CLI tool you're currently using).

## What This MCP Server Does

The MCP Flutter Automation server allows Claude Code to:
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

2. **Claude Code** - Already installed (you're using it now!)

3. **This compiled MCP server** - Already compiled as `mcp_flutter_automation`

## Setup Instructions for Claude Code

### 1. Find Your Claude Code Configuration Directory

Claude Code stores its configuration in:

**macOS/Linux:**
```bash
~/.config/claude-code/
```

**Windows:**
```bash
%APPDATA%\claude-code\
```

### 2. Create/Edit MCP Configuration

Create or edit the MCP configuration file at `~/.config/claude-code/mcp_servers.json`:

```json
{
  "mcpServers": {
    "flutter-automation": {
      "command": "/path/to/project/mcp_flutter_automation/run_mcp_server.sh",
      "args": [],
      "env": {
        "LOG_LEVEL": "INFO"
      },
      "disabled": false
    }
  }
}
```

**⚠️ Important:** Replace the path `/path/to/project/mcp_flutter_automation/` with the actual path where you have this project.

### 3. Alternative: Use Direct Executable

If you prefer to use the executable directly:

```json
{
  "mcpServers": {
    "flutter-automation": {
      "command": "/path/to/project/mcp_flutter_automation/mcp_flutter_automation",
      "args": [],
      "env": {
        "LOG_LEVEL": "INFO"
      },
      "disabled": false
    }
  }
}
```

### 4. Set Permissions

Ensure the files have proper execution permissions:

```bash
chmod +x /path/to/project/mcp_flutter_automation/mcp_flutter_automation
chmod +x /path/to/project/mcp_flutter_automation/run_mcp_server.sh
```

### 5. Restart Claude Code Session

Exit your current Claude Code session and start a new one:

```bash
# Exit current session (Ctrl+C or quit)
# Then start a new session
claude-code
```

### 6. Verify Setup

Once Claude Code restarts, you should be able to use commands like:

- "List available Flutter devices"
- "Launch a Flutter app from /path/to/my/flutter/project"
- "Take a screenshot of the running Flutter app"
- "Hot reload the Flutter app"
- "Show me the Flutter app logs"

## Configuration Options

### Environment Variables

You can customize the server behavior through environment variables:

```json
{
  "mcpServers": {
    "flutter-automation": {
      "command": "/path/to/run_mcp_server.sh",
      "args": [],
      "env": {
        "LOG_LEVEL": "DEBUG",
        "FLUTTER_ROOT": "/path/to/flutter",
        "DART_SDK": "/path/to/dart-sdk"
      },
      "disabled": false
    }
  }
}
```

### Log Levels

- `ERROR`: Only error messages
- `WARN`: Warnings and errors
- `INFO`: General information (recommended)
- `DEBUG`: Detailed debugging information

## Available MCP Tools

| Tool | Description | Example Usage |
|------|-------------|---------------|
| `launch_app` | Launch Flutter app | "Launch app from ~/my_project" |
| `hot_reload` | Hot reload running app | "Hot reload my app" |
| `hot_restart` | Hot restart running app | "Hot restart the demo app" |
| `stop_app` | Stop running app | "Stop the mobile app" |
| `capture_screenshot` | Take app screenshot | "Take a screenshot of the app" |
| `get_logs` | Get app logs | "Show me the recent logs" |
| `get_widget_tree` | Get widget tree | "Show the widget tree structure" |
| `list_apps` | List managed apps | "List all running Flutter apps" |
| `get_app_info` | Get app details | "Show info for app 'demo'" |

## Available MCP Resources

| Resource | Description | Example Usage |
|----------|-------------|---------------|
| `devices://list` | Flutter devices | "List Flutter devices" |
| `flutter://doctor` | Flutter doctor | "Check Flutter doctor status" |

## Example Workflow with Claude Code

Here's a typical Flutter development session:

```bash
# 1. Start Claude Code in your Flutter project directory
cd ~/my_flutter_project
claude-code

# 2. In Claude Code, launch your app
"Launch a Flutter app from the current directory with app ID 'my-app'"

# 3. Develop and test
"Hot reload my-app and show any errors"
"Take a screenshot to see the current UI"

# 4. Debug issues
"Show me the recent logs for my-app"
"Get the widget tree to debug the layout"

# 5. Test on different devices
"List available Flutter devices"
"Launch my-app on device 'chrome' with app ID 'web-version'"

# 6. Clean up
"Stop all running Flutter apps"
```

## Integration with Development Workflow

### Project-Specific Setup

You can create a `.claude-code/mcp_config.json` file in your Flutter project:

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

### Automation Scripts

Create shell scripts that work with Claude Code:

```bash
#!/bin/bash
# start-flutter-dev.sh

echo "Starting Flutter development session with Claude Code..."

# Launch Claude Code with Flutter automation
claude-code --mcp-config /path/to/your/mcp_config.json

# Or if using global config
claude-code
```

## Troubleshooting

### 1. MCP Server Not Found

**Issue**: Claude Code can't find the MCP server
**Solution**: 
- Verify the path in your configuration is correct
- Check file permissions: `ls -la /path/to/mcp_flutter_automation`
- Test manually: `/path/to/run_mcp_server.sh`

### 2. Flutter Command Issues

**Issue**: Flutter commands fail
**Solution**:
- Verify Flutter is in PATH: `which flutter`
- Check Flutter doctor: `flutter doctor`
- Ensure you're in a valid Flutter project directory

### 3. Permission Denied

**Issue**: Permission denied when running server
**Solution**:
```bash
chmod +x /path/to/mcp_flutter_automation
chmod +x /path/to/run_mcp_server.sh
```

### 4. Port Conflicts

**Issue**: VM Service ports already in use
**Solution**: Use custom ports:
```
"Launch app with VM service port 9182 and DDS port 9181"
```

### 5. Debug Connection Issues

**Issue**: Can't capture screenshots or get widget tree
**Solution**:
- Ensure app was launched through this MCP server
- Check that Flutter Inspector is enabled in your app
- Verify VM service connection in logs

### 6. Configuration Not Loading

**Issue**: Changes to config not taking effect
**Solution**:
- Restart Claude Code completely
- Check config file syntax with `cat ~/.config/claude-code/mcp_servers.json | jq`
- Verify file is in correct location

## Advanced Usage

### Custom Flutter Commands

You can ask Claude Code to run custom Flutter commands:

```
"Launch app with target file lib/main_dev.dart"
"Launch app with additional dart defines: --dart-define=ENV=development"
"Launch app on specific device with custom VM service port"
```

### Multiple Project Management

```
"Launch app 'mobile' from ~/mobile_project and 'web' from ~/web_project"
"Hot reload only the mobile app"
"Get logs from both apps and compare"
```

### CI/CD Integration

The MCP server can be used in automated workflows:

```bash
# In your CI script
claude-code --session "Launch app and run automated tests"
```

## Performance Tips

1. **Use specific app IDs** for better management
2. **Stop unused apps** to free resources  
3. **Use custom ports** to avoid conflicts
4. **Set appropriate log levels** (INFO for development, ERROR for production)

## Next Steps

After setup:

1. **Test basic functionality**: "List Flutter devices"
2. **Launch a test app**: "Launch app from current directory"
3. **Try development workflow**: Hot reload, screenshots, logs
4. **Explore advanced features**: Widget trees, multi-app management

Your MCP Flutter Automation server is now ready to supercharge your Flutter development workflow with Claude Code! 🚀