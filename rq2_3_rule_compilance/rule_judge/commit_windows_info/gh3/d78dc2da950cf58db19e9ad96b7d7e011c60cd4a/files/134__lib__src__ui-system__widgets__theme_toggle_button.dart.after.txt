import 'package:flutter/material.dart';
import '../navigation/ui_system_app.dart';

/// A theme toggle button that uses the app-level theme provider
class ThemeToggleButton extends StatelessWidget {
  const ThemeToggleButton({super.key});

  @override
  Widget build(BuildContext context) {
    final themeProvider = ThemeProvider.maybeOf(context);
    if (themeProvider == null) {
      // Fallback if no theme provider is found
      return const SizedBox.shrink();
    }

    final isDarkMode = Theme.of(context).brightness == Brightness.dark;

    return IconButton(
      icon: Icon(isDarkMode ? Icons.light_mode : Icons.dark_mode),
      onPressed: themeProvider.onThemeToggle,
      tooltip: isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode',
    );
  }
}
