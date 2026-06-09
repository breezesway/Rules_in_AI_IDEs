import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/navigation/ui_system_app.dart';

void main() {
  group('UISystemApp', () {
    testWidgets('should initialize with light theme mode', (tester) async {
      await tester.pumpWidget(const UISystemApp());

      // Verify the app initializes
      expect(find.byType(MaterialApp), findsOneWidget);

      // Check that theme is initially light
      final MaterialApp app = tester.widget(find.byType(MaterialApp));
      expect(app.themeMode, ThemeMode.light);
    });

    testWidgets('should provide ThemeProvider in widget tree', (tester) async {
      await tester.pumpWidget(const UISystemApp());

      // Verify the app loads without errors
      expect(find.byType(MaterialApp), findsOneWidget);
    });
  });

  group('ThemeProvider', () {
    testWidgets('should provide theme mode and toggle function', (
      tester,
    ) async {
      ThemeMode? capturedThemeMode;
      VoidCallback? capturedToggle;

      await tester.pumpWidget(
        ThemeProvider(
          themeMode: ThemeMode.light,
          onThemeToggle: () {},
          child: MaterialApp(
            home: Builder(
              builder: (context) {
                final provider = ThemeProvider.of(context);
                capturedThemeMode = provider.themeMode;
                capturedToggle = provider.onThemeToggle;
                return const SizedBox();
              },
            ),
          ),
        ),
      );

      expect(capturedThemeMode, ThemeMode.light);
      expect(capturedToggle, isNotNull);
    });

    testWidgets('should throw assertion error when not found in context', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Builder(
            builder: (context) {
              expect(
                () => ThemeProvider.of(context),
                throwsA(isA<AssertionError>()),
              );
              return const SizedBox();
            },
          ),
        ),
      );
    });

    testWidgets('maybeOf should return null when not found', (tester) async {
      ThemeProvider? result;

      await tester.pumpWidget(
        MaterialApp(
          home: Builder(
            builder: (context) {
              result = ThemeProvider.maybeOf(context);
              return const SizedBox();
            },
          ),
        ),
      );

      expect(result, isNull);
    });

    testWidgets('should update when theme mode changes', (tester) async {
      ThemeMode themeMode = ThemeMode.light;

      Widget buildApp() {
        return ThemeProvider(
          themeMode: themeMode,
          onThemeToggle: () {},
          child: const MaterialApp(home: SizedBox()),
        );
      }

      await tester.pumpWidget(buildApp());

      final ThemeProvider initialProvider = tester.widget(
        find.byType(ThemeProvider),
      );
      expect(initialProvider.themeMode, ThemeMode.light);

      // Change theme mode
      themeMode = ThemeMode.dark;
      await tester.pumpWidget(buildApp());

      final ThemeProvider updatedProvider = tester.widget(
        find.byType(ThemeProvider),
      );
      expect(updatedProvider.themeMode, ThemeMode.dark);
    });
  });
}
