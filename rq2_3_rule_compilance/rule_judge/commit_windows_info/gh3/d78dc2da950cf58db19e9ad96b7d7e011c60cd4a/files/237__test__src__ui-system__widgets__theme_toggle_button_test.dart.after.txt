import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/widgets/theme_toggle_button.dart';
import 'package:gh3/src/ui-system/navigation/ui_system_app.dart';

void main() {
  group('ThemeToggleButton', () {
    testWidgets('should show light mode icon in dark theme', (tester) async {
      await tester.pumpWidget(
        ThemeProvider(
          themeMode: ThemeMode.dark,
          onThemeToggle: () {},
          child: MaterialApp(
            theme: ThemeData.light(),
            darkTheme: ThemeData.dark(),
            themeMode: ThemeMode.dark,
            home: const Scaffold(body: ThemeToggleButton()),
          ),
        ),
      );

      // In dark mode, should show light_mode icon
      expect(find.byIcon(Icons.light_mode), findsOneWidget);
      expect(find.byIcon(Icons.dark_mode), findsNothing);
    });

    testWidgets('should show dark mode icon in light theme', (tester) async {
      await tester.pumpWidget(
        ThemeProvider(
          themeMode: ThemeMode.light,
          onThemeToggle: () {},
          child: MaterialApp(
            theme: ThemeData.light(),
            darkTheme: ThemeData.dark(),
            themeMode: ThemeMode.light,
            home: const Scaffold(body: ThemeToggleButton()),
          ),
        ),
      );

      // In light mode, should show dark_mode icon
      expect(find.byIcon(Icons.dark_mode), findsOneWidget);
      expect(find.byIcon(Icons.light_mode), findsNothing);
    });

    testWidgets('should call onThemeToggle when pressed', (tester) async {
      bool toggleCalled = false;

      await tester.pumpWidget(
        ThemeProvider(
          themeMode: ThemeMode.light,
          onThemeToggle: () {
            toggleCalled = true;
          },
          child: MaterialApp(
            theme: ThemeData.light(),
            home: const Scaffold(body: ThemeToggleButton()),
          ),
        ),
      );

      // Tap the button
      await tester.tap(find.byType(IconButton));
      await tester.pumpAndSettle();

      expect(toggleCalled, isTrue);
    });

    testWidgets('should show appropriate tooltip', (tester) async {
      await tester.pumpWidget(
        ThemeProvider(
          themeMode: ThemeMode.light,
          onThemeToggle: () {},
          child: MaterialApp(
            theme: ThemeData.light(),
            home: const Scaffold(body: ThemeToggleButton()),
          ),
        ),
      );

      final IconButton button = tester.widget(find.byType(IconButton));
      expect(button.tooltip, 'Switch to Dark Mode');
    });

    testWidgets('should render empty widget when ThemeProvider not found', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(home: Scaffold(body: ThemeToggleButton())),
      );

      // Should render SizedBox.shrink() when no provider found
      expect(find.byType(SizedBox), findsOneWidget);
      expect(find.byType(IconButton), findsNothing);
    });

    testWidgets('should be accessible', (tester) async {
      await tester.pumpWidget(
        ThemeProvider(
          themeMode: ThemeMode.light,
          onThemeToggle: () {},
          child: MaterialApp(
            theme: ThemeData.light(),
            home: const Scaffold(body: ThemeToggleButton()),
          ),
        ),
      );

      // Check that the button has semantic properties
      final IconButton button = tester.widget(find.byType(IconButton));
      expect(button.tooltip, isNotNull);
      expect(button.tooltip, isNotEmpty);

      // Verify the button can be found by semantics
      expect(
        find.byWidgetPredicate(
          (widget) =>
              widget is IconButton &&
              widget.tooltip != null &&
              widget.tooltip!.isNotEmpty,
        ),
        findsOneWidget,
      );
    });
  });
}
