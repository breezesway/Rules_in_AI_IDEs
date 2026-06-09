# Widget Inspector Documentation

## Overview

The Widget Inspector is a powerful debugging tool that combines screenshot capture with Flutter's widget tree inspection capabilities, similar to the Flutter Inspector in IDEs but accessible programmatically through MCP (Model Context Protocol).

## Key Features

- **Screenshot + Widget Tree Integration**: Captures screenshots while simultaneously mapping widget boundaries and properties
- **Coordinate-Based Widget Discovery**: Find widgets at specific screen coordinates
- **Interactive Debugging**: Inspect widget properties, hierarchy, and render information
- **Data Export**: Save inspection results as JSON and image files for analysis

## MCP Tools

### 1. `inspect_widget_tree`
Captures a screenshot with complete widget tree analysis and coordinate mapping.

**Parameters:**
- `appId` (required): ID of the Flutter app
- `includeWidgetBounds` (optional): Include widget boundary information (default: true)
- `includeWidgetTree` (optional): Include full widget tree data (default: true)  
- `filename` (optional): Base filename for saving inspection data

**Returns:**
```json
{
  "success": true,
  "inspection": {
    "appId": "demo_app",
    "screenshotBase64": "iVBORw0KGgoAAAANSUhEUgAA...",
    "widgetTree": { ... },
    "widgets": [
      {
        "id": "widget_123",
        "type": "Container",
        "properties": { ... },
        "renderBox": {
          "x": 100.0,
          "y": 200.0,
          "width": 300.0,
          "height": 150.0
        }
      }
    ],
    "timestamp": "2024-01-01T12:00:00.000Z"
  },
  "widgetCount": 42
}
```

### 2. `get_widgets_at_position`
Finds all widgets at a specific screen coordinate, sorted by area (most specific first).

**Parameters:**
- `appId` (required): ID of the Flutter app
- `x` (required): X coordinate on screen
- `y` (required): Y coordinate on screen

**Returns:**
```json
{
  "success": true,
  "widgets": [
    {
      "id": "button_456",
      "type": "ElevatedButton",
      "properties": { ... },
      "renderBox": {
        "x": 95.0,
        "y": 195.0,
        "width": 110.0,
        "height": 40.0
      }
    }
  ],
  "position": {"x": 100.0, "y": 200.0},
  "count": 3
}
```

### 3. `create_annotated_screenshot`
Creates a screenshot with widget boundary overlays (future enhancement for visual debugging).

**Parameters:**
- `appId` (required): ID of the Flutter app
- `showWidgetBounds` (optional): Show widget boundary lines (default: true)
- `showWidgetLabels` (optional): Show widget type labels (default: false)
- `filename` (optional): Filename for annotated screenshot (default: annotated_screenshot.png)

## Usage Examples

### Basic Widget Inspection
```dart
import 'mcp_flutter_automation/lib/mcp_flutter_automation.dart';

final controller = FlutterController();
final inspector = WidgetInspector(controller);

// Perform full inspection
final result = await inspector.inspectWithScreenshot(
  'my_app',
  includeWidgetBounds: true,
  filename: 'debug_session_1'
);

print('Found ${result.widgets.length} widgets');
```

### Find Widgets at Touch Point
```dart
// Find what widgets are at coordinates (150, 300)
final widgets = await inspector.getWidgetsAtPosition('my_app', 150, 300);

for (final widget in widgets) {
  print('${widget.type} at ${widget.renderBox?.x}, ${widget.renderBox?.y}');
}
```

### Using MCP Server
```bash
# Launch app first
curl -X POST http://localhost:3000/tools/call \
  -d '{"name": "launch_app", "arguments": {"appId": "test", "projectPath": "/path/to/project"}}'

# Inspect widget tree
curl -X POST http://localhost:3000/tools/call \
  -d '{"name": "inspect_widget_tree", "arguments": {"appId": "test", "filename": "inspection1"}}'

# Find widgets at position
curl -X POST http://localhost:3000/tools/call \
  -d '{"name": "get_widgets_at_position", "arguments": {"appId": "test", "x": 200, "y": 400}}'
```

## Data Structures

### WidgetInspectionResult
Complete result of widget inspection including screenshot and widget data.

### WidgetInfo
Information about a specific widget:
- `id`: Unique widget identifier
- `type`: Widget class name (e.g., "Container", "Text")
- `properties`: Map of widget properties
- `renderBox`: Position and size information

### RenderBoxInfo
Widget positioning and size:
- `x`, `y`: Position coordinates
- `width`, `height`: Widget dimensions
- `containsPoint(x, y)`: Check if point is within widget bounds
- `area`: Widget area in pixels

## Integration with Existing Tools

The Widget Inspector works seamlessly with existing MCP Flutter automation tools:

1. **Screenshot Integration**: Uses the same screenshot system as `capture_screenshot`
2. **Widget Tree Data**: Leverages `get_widget_tree` functionality
3. **App Management**: Works with apps launched via `launch_app`

## Files Generated

When using the `filename` parameter, the inspector creates:
- `{filename}_screenshot.png`: Captured screenshot
- `{filename}_inspection.json`: Complete inspection data including widget tree and coordinates

## Debugging Workflow

1. **Launch App**: Start your Flutter app with `launch_app`
2. **Capture State**: Use `inspect_widget_tree` to get current screen state
3. **Interactive Exploration**: Use `get_widgets_at_position` to explore specific areas
4. **Analysis**: Review generated JSON files and screenshots

## Future Enhancements

- **Visual Overlays**: Draw widget boundaries directly on screenshots
- **Widget Highlighting**: Highlight specific widgets in screenshots
- **Performance Metrics**: Include render times and performance data
- **Interactive HTML Reports**: Generate interactive debugging reports

This widget inspector provides a programmatic alternative to IDE-based Flutter inspection tools, making it perfect for automated testing, debugging, and UI analysis workflows.