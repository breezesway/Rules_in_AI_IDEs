import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../layouts/gh_screen_template.dart';
import '../components/gh_card.dart';
import '../components/gh_button.dart';
import '../data/fake_data_service.dart';
import '../widgets/gh_file_tree_item.dart';
import '../tokens/gh_tokens.dart';
import '../navigation/navigation_service.dart';
import '../utils/date_formatter.dart';
import '../state_widgets/gh_loading_indicator.dart';

/// Repository file example screen showing file content with syntax highlighting
/// and file metadata.
class RepositoryFileExample extends StatefulWidget {
  /// Repository owner
  final String owner;

  /// Repository name
  final String name;

  /// File path within the repository
  final String filePath;

  const RepositoryFileExample({
    super.key,
    required this.owner,
    required this.name,
    required this.filePath,
  });

  @override
  State<RepositoryFileExample> createState() => _RepositoryFileExampleState();
}

class _RepositoryFileExampleState extends State<RepositoryFileExample> {
  late FakeFile _file;
  bool _isLoading = true;
  String? _error;
  bool _showLineNumbers = true;
  bool _wrapLines = false;

  @override
  void initState() {
    super.initState();
    _loadFileData();
  }

  Future<void> _loadFileData() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      // Simulate network delay
      await Future.delayed(const Duration(milliseconds: 800));

      // Simulate potential errors for demonstration
      if (widget.filePath.contains('nonexistent') ||
          widget.filePath.contains('404')) {
        throw Exception('File not found');
      }

      if (widget.filePath.contains('permission') ||
          widget.filePath.contains('private')) {
        throw Exception('Access denied');
      }

      if (widget.filePath.contains('large') &&
          widget.filePath.contains('binary')) {
        throw Exception('File too large to display');
      }

      // Load file content
      _file = _generateFileContent(widget.filePath);

      setState(() {
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
        _error = _getErrorMessage(e.toString());
      });
    }
  }

  String _getErrorMessage(String error) {
    if (error.contains('not found') || error.contains('404')) {
      return 'File not found. It may have been moved or deleted.';
    } else if (error.contains('Access denied') ||
        error.contains('permission')) {
      return 'Access denied. You don\'t have permission to view this file.';
    } else if (error.contains('too large')) {
      return 'File is too large to display in the viewer.';
    } else if (error.contains('timeout')) {
      return 'Request timed out. Please try again.';
    } else if (error.contains('network')) {
      return 'Network error. Please check your connection and try again.';
    } else {
      return 'Failed to load file content. Please try again.';
    }
  }

  IconData _getErrorIcon() {
    if (_error!.contains('not found')) {
      return Icons.search_off;
    } else if (_error!.contains('Access denied')) {
      return Icons.lock;
    } else if (_error!.contains('too large')) {
      return Icons.warning;
    } else if (_error!.contains('timeout') || _error!.contains('network')) {
      return Icons.wifi_off;
    } else {
      return Icons.error_outline;
    }
  }

  FakeFile _generateFileContent(String filePath) {
    final fileName = filePath.split('/').last;
    final extension = fileName.contains('.')
        ? fileName.split('.').last.toLowerCase()
        : '';

    String content;
    GHFileType type;

    switch (extension) {
      case 'dart':
        type = GHFileType.code;
        content = _generateDartContent(fileName);
        break;
      case 'js':
      case 'ts':
        type = GHFileType.code;
        content = _generateJavaScriptContent();
        break;
      case 'py':
        type = GHFileType.code;
        content = _generatePythonContent();
        break;
      case 'md':
        type = GHFileType.markdown;
        content = _generateMarkdownContent(fileName);
        break;
      case 'json':
        type = GHFileType.data;
        content = _generateJsonContent();
        break;
      case 'yaml':
      case 'yml':
        type = GHFileType.config;
        content = _generateYamlContent();
        break;
      default:
        type = GHFileType.file;
        content = _generateGenericContent(fileName);
        break;
    }

    return FakeFile(
      name: fileName,
      type: type,
      content: content,
      size: content.length,
      lastCommitMessage: 'Update $fileName implementation',
      author: 'developer',
      lastModified: DateTime.now().subtract(
        Duration(days: 1 + (fileName.hashCode % 30)),
      ),
      path: filePath,
    );
  }

  String _generateDartContent(String fileName) {
    final className = _toPascalCase(fileName.replaceAll('.dart', ''));
    return '''import 'package:flutter/material.dart';

/// Example $className widget
class $className extends StatefulWidget {
  /// Creates a new instance
  const $className({super.key});

  @override
  State<$className> createState() => _${className}State();
}

class _${className}State extends State<$className> {
  bool _isLoading = false;
  String _message = 'Hello, World!';

  @override
  void initState() {
    super.initState();
    _initializeData();
  }

  Future<void> _initializeData() async {
    setState(() {
      _isLoading = true;
    });

    // Simulate async operation
    await Future.delayed(const Duration(milliseconds: 500));

    setState(() {
      _isLoading = false;
      _message = 'Data loaded successfully!';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('$className'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (_isLoading) ..[
              const GHLoadingIndicator.medium(
                label: 'Loading...',
              ),
            ] else ...[
              const Icon(
                Icons.check_circle,
                color: Colors.green,
                size: 64,
              ),
              const SizedBox(height: 16),
              Text(
                _message,
                style: Theme.of(context).textTheme.headlineSmall,
              ),
            ],
          ],
        ),
      ),
    );
  }
}''';
  }

  String _generateJavaScriptContent() {
    return '''/**
 * Data management utilities
 */

import { useState, useEffect } from 'react';

interface DataItem {
  id: number;
  name: string;
  value: string;
  timestamp: Date;
}

export const useDataManager = () => {
  const [data, setData] = useState<DataItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/data');
      if (!response.ok) {
        throw new Error('Failed to load data');
      }
      
      const result = await response.json();
      setData(result.data || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  };

  const addItem = (item: Omit<DataItem, 'id' | 'timestamp'>) => {
    const newItem: DataItem = {
      ...item,
      id: Date.now(),
      timestamp: new Date()
    };
    
    setData(prev => [...prev, newItem]);
  };

  return { data, isLoading, error, loadData, addItem };
};

export default useDataManager;''';
  }

  String _generatePythonContent() {
    return '''"""
Data processing module
"""

import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class DataItem:
    """Represents a single data item."""
    
    id: int
    name: str
    value: str
    timestamp: datetime
    metadata: Optional[Dict] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata or {}
        }

class DataProcessor:
    """Handles data processing operations."""
    
    def __init__(self):
        self.items: List[DataItem] = []
    
    def add_item(self, name: str, value: str) -> DataItem:
        """Add a new data item."""
        item = DataItem(
            id=len(self.items) + 1,
            name=name,
            value=value,
            timestamp=datetime.now()
        )
        
        self.items.append(item)
        logger.info(f"Added item: {item.name}")
        return item
    
    def get_items(self, limit: Optional[int] = None) -> List[DataItem]:
        """Get all items, optionally limited."""
        items = self.items
        if limit:
            items = items[-limit:]
        return items
    
    def export_to_json(self, filename: str) -> None:
        """Export items to JSON file."""
        data = [item.to_dict() for item in self.items]
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Exported {len(self.items)} items to {filename}")

def main():
    """Example usage."""
    processor = DataProcessor()
    processor.add_item("Sample Item", "Test Value")
    processor.export_to_json("data_export.json")

if __name__ == "__main__":
    main()''';
  }

  String _generateMarkdownContent(String fileName) {
    final title = fileName.replaceAll('.md', '').replaceAll('_', ' ');
    return '''# ${title.split(' ').map((word) => word[0].toUpperCase() + word.substring(1)).join(' ')}

Welcome to this comprehensive guide. This document provides detailed information about the implementation and usage.

## Overview

This module provides essential functionality for the application ecosystem.

### Key Features

- **High Performance**: Optimized for fast processing
- **Scalability**: Handles large datasets efficiently  
- **Reliability**: Comprehensive error handling
- **Maintainability**: Clean, documented code

## Installation

```bash
git clone https://github.com/example/project.git
cd project
npm install
npm start
```

## Usage

### Basic Example

```javascript
import { DataProcessor } from './data-processor';

const processor = new DataProcessor();
processor.configure({
  maxItems: 1000,
  enableCaching: true
});

const result = await processor.process(inputData);
console.log('Processing completed:', result);
```

## API Reference

### Core Methods

#### process(data: any[]): Promise<ProcessResult>

Processes an array of data items.

**Parameters:**
- data - Array of items to process

**Returns:**
- Promise resolving to ProcessResult

## Best Practices

1. **Performance**: Process data in batches
2. **Error Handling**: Implement proper error handling
3. **Testing**: Write comprehensive tests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests
4. Submit a pull request

## License

This project is licensed under the MIT License.''';
  }

  String _generateJsonContent() {
    return '''{
  "name": "example-project",
  "version": "1.0.0",
  "description": "Example configuration file",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest",
    "build": "webpack --mode production"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "helmet": "^7.0.0",
    "morgan": "^1.10.0",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "jest": "^29.6.2",
    "eslint": "^8.47.0"
  },
  "keywords": [
    "nodejs",
    "express",
    "api"
  ],
  "author": "Development Team",
  "license": "MIT"
}''';
  }

  String _generateYamlContent() {
    return '''# Application configuration
app:
  name: "Example Application"
  version: "1.0.0"
  environment: "development"
  debug: true
  
server:
  host: "0.0.0.0"
  port: 8080
  timeout: 30
  
database:
  type: "postgresql"
  host: "localhost"
  port: 5432
  name: "app_db"
  
logging:
  level: "info"
  format: "json"
  outputs:
    - type: "console"
      enabled: true
    - type: "file"
      enabled: true
      path: "./logs/app.log"
      
security:
  jwt:
    secret: "your-secret-key"
    expires_in: "24h"
  cors:
    enabled: true
    origins:
      - "http://localhost:3000"
    methods:
      - "GET"
      - "POST"
      - "PUT"
      - "DELETE"''';
  }

  String _generateGenericContent(String fileName) {
    return '''This is a sample file: $fileName

File Contents:
==============

This file contains information related to the project.
It demonstrates how different file types are handled
within the repository browser and file viewer.

Key Information:
- File name: $fileName
- Created: ${DateTime.now().toIso8601String().split('T')[0]}
- Purpose: Demonstration and testing
- Encoding: UTF-8

The file viewer supports multiple file types including:
- Source code files (Dart, JavaScript, Python)
- Configuration files (YAML, JSON)
- Documentation files (Markdown, Text)

Features:
1. Syntax highlighting for supported languages
2. Line numbering for code navigation
3. Copy-to-clipboard functionality
4. File metadata display
5. Responsive design

For more information, refer to the README.md file.

---
End of file content''';
  }

  String _toPascalCase(String input) {
    return input
        .split('_')
        .map(
          (word) =>
              word.isEmpty ? '' : word[0].toUpperCase() + word.substring(1),
        )
        .join('');
  }

  Future<void> _copyToClipboard() async {
    if (_file.content != null) {
      await Clipboard.setData(ClipboardData(text: _file.content!));
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('File content copied to clipboard')),
        );
      }
    }
  }

  Future<void> _downloadFile() async {
    try {
      // Simulate download process
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Downloading ${_file.name}...'),
          duration: const Duration(seconds: 1),
        ),
      );

      // Simulate download delay
      await Future.delayed(const Duration(milliseconds: 1500));

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(
              children: [
                const Icon(Icons.check_circle, color: Colors.green),
                const SizedBox(width: 8),
                Expanded(child: Text('${_file.name} downloaded successfully')),
              ],
            ),
            action: SnackBarAction(
              label: 'Open',
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Opening ${_file.name}...')),
                );
              },
            ),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to download ${_file.name}'),
            backgroundColor: Theme.of(context).colorScheme.error,
          ),
        );
      }
    }
  }

  Future<void> _shareFile() async {
    try {
      // Simulate share functionality
      final shareUrl =
          'https://github.com/${widget.owner}/${widget.name}/blob/main/${widget.filePath}';

      await Clipboard.setData(ClipboardData(text: shareUrl));

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: const Text('File URL copied to clipboard'),
            action: SnackBarAction(
              label: 'View URL',
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: const Text('Share File'),
                    content: Column(
                      mainAxisSize: MainAxisSize.min,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('File: ${_file.name}'),
                        const SizedBox(height: 8),
                        Text('URL: $shareUrl'),
                      ],
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.of(context).pop(),
                        child: const Text('Close'),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(const SnackBar(content: Text('Failed to share file')));
      }
    }
  }

  void _viewRawFile() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Raw ${_file.name}'),
        content: SizedBox(
          width: double.maxFinite,
          height: 400,
          child: SingleChildScrollView(
            child: SelectableText(
              _file.content ?? 'No content available',
              style: GHTokens.bodyMedium.copyWith(fontFamily: 'monospace'),
            ),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () async {
              await Clipboard.setData(ClipboardData(text: _file.content ?? ''));
              if (context.mounted) {
                Navigator.of(context).pop();
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Raw content copied to clipboard'),
                  ),
                );
              }
            },
            child: const Text('Copy'),
          ),
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }

  void _viewBlame() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Blame for ${_file.name}'),
        content: SizedBox(
          width: double.maxFinite,
          height: 300,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'This feature shows who last modified each line of the file.',
                style: GHTokens.bodyMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
              const SizedBox(height: 16),
              Expanded(
                child: Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Theme.of(
                      context,
                    ).colorScheme.surfaceContainerHighest,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    'Blame information:\n\n'
                    'Line 1-10: developer (2 days ago)\n'
                    'Line 11-25: ui-team (1 week ago)\n'
                    'Line 26-40: architect (2 weeks ago)\n\n'
                    'This is a simulated blame view for demonstration.',
                    style: GHTokens.bodyMedium.copyWith(
                      fontFamily: 'monospace',
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }

  void _viewHistory() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('History for ${_file.name}'),
        content: SizedBox(
          width: double.maxFinite,
          height: 300,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Recent commits that modified this file:',
                style: GHTokens.bodyMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
              const SizedBox(height: 16),
              Expanded(
                child: ListView(
                  children: [
                    _buildHistoryItem(
                      'Update ${_file.name} implementation',
                      'developer',
                      '2 days ago',
                      'a1b2c3d',
                    ),
                    _buildHistoryItem(
                      'Refactor code structure',
                      'architect',
                      '1 week ago',
                      'e4f5g6h',
                    ),
                    _buildHistoryItem(
                      'Add comprehensive documentation',
                      'docs-team',
                      '2 weeks ago',
                      'i7j8k9l',
                    ),
                    _buildHistoryItem(
                      'Initial implementation',
                      'developer',
                      '1 month ago',
                      'm0n1o2p',
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }

  Widget _buildHistoryItem(
    String message,
    String author,
    String time,
    String hash,
  ) {
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            message,
            style: GHTokens.bodyMedium.copyWith(fontWeight: FontWeight.w500),
          ),
          const SizedBox(height: 4),
          Row(
            children: [
              Text(
                author,
                style: GHTokens.bodyMedium.copyWith(
                  color: Theme.of(context).colorScheme.primary,
                ),
              ),
              Text(
                ' • $time • ',
                style: GHTokens.bodyMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
              Text(
                hash,
                style: GHTokens.bodyMedium.copyWith(
                  fontFamily: 'monospace',
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(title: Text(widget.filePath)),
        body: const GHLoadingIndicator.large(
          label: 'Loading file...',
          centered: true,
        ),
      );
    }

    if (_error != null) {
      return Scaffold(
        appBar: AppBar(title: Text('${widget.owner}/${widget.name}')),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(GHTokens.spacing24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  _getErrorIcon(),
                  size: 64,
                  color: Theme.of(context).colorScheme.error,
                ),
                const SizedBox(height: GHTokens.spacing16),
                Text(
                  _error!,
                  style: GHTokens.titleMedium,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: GHTokens.spacing8),
                Text(
                  'File: ${widget.filePath}',
                  style: GHTokens.bodyMedium.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: GHTokens.spacing24),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    ElevatedButton.icon(
                      onPressed: _loadFileData,
                      icon: const Icon(Icons.refresh),
                      label: const Text('Retry'),
                    ),
                    const SizedBox(width: GHTokens.spacing12),
                    OutlinedButton.icon(
                      onPressed: () {
                        final directory = widget.filePath.contains('/')
                            ? widget.filePath.substring(
                                0,
                                widget.filePath.lastIndexOf('/'),
                              )
                            : '';
                        NavigationService.navigateToRepositoryTree(
                          widget.owner,
                          widget.name,
                          path: directory,
                        );
                      },
                      icon: const Icon(Icons.folder_open),
                      label: const Text('Browse Directory'),
                    ),
                  ],
                ),
                const SizedBox(height: GHTokens.spacing12),
                TextButton.icon(
                  onPressed: () {
                    NavigationService.navigateToRepository(
                      widget.owner,
                      widget.name,
                    );
                  },
                  icon: const Icon(Icons.home),
                  label: const Text('Back to Repository'),
                ),
              ],
            ),
          ),
        ),
      );
    }

    return GHScreenTemplate(
      title: _file.name,
      actions: [
        IconButton(
          icon: const Icon(Icons.copy),
          onPressed: _copyToClipboard,
          tooltip: 'Copy to clipboard',
        ),
        IconButton(
          icon: const Icon(Icons.download_outlined),
          onPressed: _downloadFile,
          tooltip: 'Download file',
        ),
        IconButton(
          icon: const Icon(Icons.share),
          onPressed: _shareFile,
          tooltip: 'Share file',
        ),
        PopupMenuButton<String>(
          onSelected: (value) {
            switch (value) {
              case 'line_numbers':
                setState(() {
                  _showLineNumbers = !_showLineNumbers;
                });
                break;
              case 'wrap_lines':
                setState(() {
                  _wrapLines = !_wrapLines;
                });
                break;
              case 'raw':
                _viewRawFile();
                break;
              case 'blame':
                _viewBlame();
                break;
              case 'history':
                _viewHistory();
                break;
            }
          },
          itemBuilder: (context) => [
            PopupMenuItem(
              value: 'line_numbers',
              child: Row(
                children: [
                  Icon(
                    _showLineNumbers
                        ? Icons.check_box
                        : Icons.check_box_outline_blank,
                  ),
                  const SizedBox(width: 8),
                  const Text('Line numbers'),
                ],
              ),
            ),
            PopupMenuItem(
              value: 'wrap_lines',
              child: Row(
                children: [
                  Icon(
                    _wrapLines
                        ? Icons.check_box
                        : Icons.check_box_outline_blank,
                  ),
                  const SizedBox(width: 8),
                  const Text('Wrap lines'),
                ],
              ),
            ),
            const PopupMenuItem(value: 'raw', child: Text('View raw')),
            const PopupMenuItem(value: 'blame', child: Text('View blame')),
            const PopupMenuItem(value: 'history', child: Text('View history')),
          ],
        ),
      ],
      body: Column(
        children: [
          // File metadata header
          _buildFileHeader(),

          // Code content
          Expanded(child: _buildCodeContent()),
        ],
      ),
    );
  }

  Widget _buildFileHeader() {
    final pathSegments = widget.filePath.split('/');
    final directory = pathSegments.length > 1
        ? pathSegments.take(pathSegments.length - 1).join('/')
        : '';

    return GHCard(
      margin: const EdgeInsets.all(GHTokens.spacing16),
      child: Padding(
        padding: const EdgeInsets.all(GHTokens.spacing16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Breadcrumb navigation
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  GestureDetector(
                    onTap: () => NavigationService.navigateToRepository(
                      widget.owner,
                      widget.name,
                    ),
                    child: Text(
                      '${widget.owner}/${widget.name}',
                      style: GHTokens.bodyMedium.copyWith(
                        color: Theme.of(context).colorScheme.primary,
                        decoration: TextDecoration.underline,
                      ),
                    ),
                  ),
                  if (directory.isNotEmpty) ...[
                    const Icon(Icons.chevron_right, size: 16),
                    GestureDetector(
                      onTap: () => NavigationService.navigateToRepositoryTree(
                        widget.owner,
                        widget.name,
                        path: directory,
                      ),
                      child: Text(
                        directory,
                        style: GHTokens.bodyMedium.copyWith(
                          color: Theme.of(context).colorScheme.primary,
                          decoration: TextDecoration.underline,
                        ),
                      ),
                    ),
                    const Icon(Icons.chevron_right, size: 16),
                  ] else ...[
                    const Icon(Icons.chevron_right, size: 16),
                  ],
                  Text(
                    _file.name,
                    style: GHTokens.bodyMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurface,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: GHTokens.spacing12),

            // File metadata
            Wrap(
              spacing: GHTokens.spacing12,
              runSpacing: GHTokens.spacing8,
              children: [
                _buildMetadataChip(
                  Icons.data_object,
                  '${(_file.size ?? 0)} bytes',
                ),
                _buildMetadataChip(
                  Icons.code,
                  _getLanguageFromExtension(_file.name),
                ),
                _buildMetadataChip(
                  Icons.schedule,
                  DateFormatter.formatRelative(_file.lastModified),
                ),
                if (_file.author.isNotEmpty)
                  _buildMetadataChip(Icons.person, _file.author),
              ],
            ),

            const SizedBox(height: GHTokens.spacing12),

            // Action buttons
            Row(
              children: [
                Expanded(
                  child: GHButton(
                    label: 'Edit file',
                    icon: Icons.edit,
                    style: GHButtonStyle.secondary,
                    onPressed: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Edit ${_file.name}')),
                      );
                    },
                  ),
                ),
                const SizedBox(width: GHTokens.spacing8),
                Expanded(
                  child: GHButton(
                    label: 'View history',
                    icon: Icons.history,
                    style: GHButtonStyle.secondary,
                    onPressed: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('View history of ${_file.name}'),
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMetadataChip(IconData icon, String text) {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: GHTokens.spacing8,
        vertical: GHTokens.spacing4,
      ),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(GHTokens.radius12),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            icon,
            size: 14,
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
          const SizedBox(width: GHTokens.spacing4),
          Text(
            text,
            style: GHTokens.labelMedium.copyWith(
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCodeContent() {
    if (_file.content == null || _file.content!.isEmpty) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(GHTokens.spacing24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.description_outlined, size: 64, color: Colors.grey),
              SizedBox(height: GHTokens.spacing16),
              Text(
                'This file is empty',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w500),
              ),
              SizedBox(height: GHTokens.spacing8),
              Text(
                'The file has no content to display',
                style: TextStyle(color: Colors.grey),
              ),
            ],
          ),
        ),
      );
    }

    final lines = _file.content!.split('\n');
    final lineNumberWidth = lines.length.toString().length * 8.0 + 16;

    return GHCard(
      margin: const EdgeInsets.fromLTRB(
        GHTokens.spacing16,
        0,
        GHTokens.spacing16,
        GHTokens.spacing16,
      ),
      child: Container(
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.surfaceContainerHighest,
          borderRadius: BorderRadius.circular(GHTokens.radius8),
        ),
        child: SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: SizedBox(
            width: MediaQuery.of(context).size.width - 32,
            child: ListView.builder(
              itemCount: lines.length,
              itemBuilder: (context, index) {
                final lineNumber = index + 1;
                final lineContent = lines[index];

                return Container(
                  decoration: BoxDecoration(
                    border: index > 0
                        ? Border(
                            top: BorderSide(
                              color: Theme.of(
                                context,
                              ).colorScheme.outline.withValues(alpha: 0.1),
                              width: 1,
                            ),
                          )
                        : null,
                  ),
                  child: IntrinsicHeight(
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        // Line numbers
                        if (_showLineNumbers)
                          Container(
                            width: lineNumberWidth,
                            padding: const EdgeInsets.symmetric(
                              horizontal: GHTokens.spacing8,
                              vertical: GHTokens.spacing4,
                            ),
                            decoration: BoxDecoration(
                              color: Theme.of(
                                context,
                              ).colorScheme.surfaceContainer,
                              border: Border(
                                right: BorderSide(
                                  color: Theme.of(
                                    context,
                                  ).colorScheme.outline.withValues(alpha: 0.2),
                                  width: 1,
                                ),
                              ),
                            ),
                            child: Text(
                              lineNumber.toString(),
                              style: GHTokens.bodyMedium.copyWith(
                                color: Theme.of(
                                  context,
                                ).colorScheme.onSurfaceVariant,
                                fontFamily: 'monospace',
                              ),
                              textAlign: TextAlign.right,
                            ),
                          ),

                        // Code content
                        Expanded(
                          child: Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: GHTokens.spacing12,
                              vertical: GHTokens.spacing4,
                            ),
                            child: Text(
                              lineContent,
                              style: GHTokens.bodyMedium.copyWith(
                                fontFamily: 'monospace',
                                color: _getSyntaxColor(lineContent),
                              ),
                              softWrap: _wrapLines,
                              overflow: _wrapLines
                                  ? TextOverflow.visible
                                  : TextOverflow.ellipsis,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ),
      ),
    );
  }

  String _getLanguageFromExtension(String fileName) {
    final extension = fileName.contains('.')
        ? fileName.split('.').last.toLowerCase()
        : '';

    switch (extension) {
      case 'dart':
        return 'Dart';
      case 'js':
        return 'JavaScript';
      case 'ts':
        return 'TypeScript';
      case 'py':
        return 'Python';
      case 'java':
        return 'Java';
      case 'kt':
        return 'Kotlin';
      case 'swift':
        return 'Swift';
      case 'rs':
        return 'Rust';
      case 'go':
        return 'Go';
      case 'cpp':
      case 'cxx':
      case 'cc':
        return 'C++';
      case 'c':
        return 'C';
      case 'cs':
        return 'C#';
      case 'php':
        return 'PHP';
      case 'rb':
        return 'Ruby';
      case 'md':
        return 'Markdown';
      case 'json':
        return 'JSON';
      case 'xml':
        return 'XML';
      case 'yaml':
      case 'yml':
        return 'YAML';
      case 'sql':
        return 'SQL';
      case 'sh':
        return 'Shell';
      case 'html':
        return 'HTML';
      case 'css':
        return 'CSS';
      case 'scss':
        return 'SCSS';
      default:
        return 'Text';
    }
  }

  Color _getSyntaxColor(String line) {
    final trimmed = line.trim();
    final colorScheme = Theme.of(context).colorScheme;

    // Comments
    if (trimmed.startsWith('//') ||
        trimmed.startsWith('#') ||
        trimmed.startsWith('/*') ||
        trimmed.startsWith('*')) {
      return colorScheme.onSurfaceVariant.withValues(alpha: 0.7);
    }

    // Keywords
    if (trimmed.contains('class') ||
        trimmed.contains('function') ||
        trimmed.contains('def') ||
        trimmed.contains('import') ||
        trimmed.contains('if') ||
        trimmed.contains('else') ||
        trimmed.contains('for') ||
        trimmed.contains('while') ||
        trimmed.contains('return') ||
        trimmed.contains('const') ||
        trimmed.contains('let') ||
        trimmed.contains('var') ||
        trimmed.contains('final')) {
      return colorScheme.primary;
    }

    // Strings (basic detection)
    if ((trimmed.contains('"') &&
            trimmed.indexOf('"') != trimmed.lastIndexOf('"')) ||
        (trimmed.contains("'") &&
            trimmed.indexOf("'") != trimmed.lastIndexOf("'"))) {
      return Colors.green.shade700;
    }

    // Numbers (basic detection)
    if (RegExp(r'\b\d+\b').hasMatch(trimmed)) {
      return Colors.blue.shade700;
    }

    return colorScheme.onSurface;
  }
}
