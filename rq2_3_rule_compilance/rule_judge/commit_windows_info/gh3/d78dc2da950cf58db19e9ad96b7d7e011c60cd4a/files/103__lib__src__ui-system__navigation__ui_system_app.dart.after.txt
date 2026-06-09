import 'package:flutter/material.dart';
import '../theme/gh_theme.dart';
import 'navigation_service.dart';

/// Main UI System demo application
class UISystemApp extends StatefulWidget {
  const UISystemApp({super.key});

  @override
  State<UISystemApp> createState() => _UISystemAppState();
}

class _UISystemAppState extends State<UISystemApp> {
  ThemeMode _themeMode = ThemeMode.light;

  void _toggleTheme() {
    setState(() {
      _themeMode = _themeMode == ThemeMode.light
          ? ThemeMode.dark
          : ThemeMode.light;
    });
  }

  @override
  Widget build(BuildContext context) {
    return ThemeProvider(
      themeMode: _themeMode,
      onThemeToggle: _toggleTheme,
      child: MaterialApp.router(
        title: 'GitHub UI System Demo - Phase 4',
        theme: GHTheme.lightTheme(),
        darkTheme: GHTheme.darkTheme(),
        themeMode: _themeMode,
        routerConfig: NavigationService.router,
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}

/// Theme provider for accessing theme state throughout the app
class ThemeProvider extends InheritedWidget {
  final ThemeMode themeMode;
  final VoidCallback onThemeToggle;

  const ThemeProvider({
    super.key,
    required this.themeMode,
    required this.onThemeToggle,
    required super.child,
  });

  static ThemeProvider? maybeOf(BuildContext context) {
    return context.dependOnInheritedWidgetOfExactType<ThemeProvider>();
  }

  static ThemeProvider of(BuildContext context) {
    final ThemeProvider? result = maybeOf(context);
    assert(result != null, 'No ThemeProvider found in context');
    return result!;
  }

  @override
  bool updateShouldNotify(ThemeProvider oldWidget) {
    return themeMode != oldWidget.themeMode;
  }
}
