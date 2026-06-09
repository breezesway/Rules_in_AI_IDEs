import 'package:flutter/material.dart';
import '../src/ui-system/navigation/ui_system_app.dart';

/// Entry point for the standalone UI system demo application
void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const UISystemApp());
}
