import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/examples/design_tokens_screen.dart';

void main() {
  group('DesignTokensScreen', () {
    testWidgets('should display screen title', (tester) async {
      await tester.pumpWidget(const MaterialApp(home: DesignTokensScreen()));

      expect(find.text('Design Tokens'), findsOneWidget);
    });

    testWidgets('should display theme toggle button', (tester) async {
      await tester.pumpWidget(const MaterialApp(home: DesignTokensScreen()));

      expect(find.byIcon(Icons.dark_mode), findsOneWidget);
    });

    testWidgets('should toggle theme when theme button is pressed', (
      tester,
    ) async {
      await tester.pumpWidget(const MaterialApp(home: DesignTokensScreen()));

      // Initially should show dark mode icon (light theme active)
      expect(find.byIcon(Icons.dark_mode), findsOneWidget);
      expect(find.byIcon(Icons.light_mode), findsNothing);

      // Tap the theme toggle button
      await tester.tap(find.byIcon(Icons.dark_mode));
      await tester.pump();

      // Should now show light mode icon (dark theme active)
      expect(find.byIcon(Icons.light_mode), findsOneWidget);
      expect(find.byIcon(Icons.dark_mode), findsNothing);
    });

    testWidgets('should display all section headers', (tester) async {
      await tester.pumpWidget(const MaterialApp(home: DesignTokensScreen()));

      expect(find.text('GitHub Brand Colors'), findsOneWidget);
      expect(find.text('GitHub Semantic Colors'), findsOneWidget);
      expect(find.text('Typography Scale'), findsOneWidget);
      expect(find.text('Spacing System'), findsOneWidget);
      expect(find.text('Programming Language Colors'), findsOneWidget);
      expect(find.text('Border Radius & Elevation'), findsOneWidget);
    });

    testWidgets('should display brand color cards', (tester) async {
      await tester.pumpWidget(const MaterialApp(home: DesignTokensScreen()));

      expect(find.text('Primary'), findsOneWidget);
      expect(find.text('On Primary'), findsOneWidget);
      expect(find.text('Primary Container'), findsOneWidget);
      expect(find.text('On Primary Container'), findsOneWidget);
    });

    testWidgets('should display semantic color cards', (tester) async {
      await tester.pumpWidget(const MaterialApp(home: DesignTokensScreen()));

      expect(find.text('Success'), findsOneWidget);
      expect(find.text('Warning'), findsOneWidget);
      expect(find.text('Error'), findsOneWidget);
      expect(find.text('Merged'), findsOneWidget);
      expect(find.text('Draft'), findsOneWidget);
    });

    testWidgets('should display typography styles', (tester) async {
      await tester.pumpWidget(const MaterialApp(home: DesignTokensScreen()));

      expect(find.text('Headline Large'), findsOneWidget);
      expect(find.text('Headline Medium'), findsOneWidget);
      expect(find.text('Title Large'), findsOneWidget);
      expect(find.text('Title Medium'), findsOneWidget);
      expect(find.text('Body Large'), findsOneWidget);
      expect(find.text('Body Medium'), findsOneWidget);
      expect(find.text('Label Large'), findsOneWidget);
      expect(find.text('Label Medium'), findsOneWidget);
    });

    testWidgets('should display typography specimens', (tester) async {
      await tester.pumpWidget(const MaterialApp(home: DesignTokensScreen()));

      // Should find multiple instances of the typography specimen text
      expect(
        find.text('The quick brown fox jumps over the lazy dog'),
        findsWidgets,
      );
    });

    testWidgets('should display spacing system', (tester) async {
      await tester.pumpWidget(const MaterialApp(home: DesignTokensScreen()));

      expect(find.text('spacing4 (4dp)'), findsOneWidget);
      expect(find.text('spacing8 (8dp)'), findsOneWidget);
      expect(find.text('spacing12 (12dp)'), findsOneWidget);
      expect(find.text('spacing16 (16dp)'), findsOneWidget);
      expect(find.text('spacing20 (20dp)'), findsOneWidget);
      expect(find.text('spacing24 (24dp)'), findsOneWidget);
      expect(find.text('spacing32 (32dp)'), findsOneWidget);
    });

    testWidgets('should display programming language colors', (tester) async {
      await tester.pumpWidget(const MaterialApp(home: DesignTokensScreen()));

      // Should find some popular programming languages
      expect(find.text('JavaScript'), findsOneWidget);
      expect(find.text('Dart'), findsOneWidget);
      expect(find.text('Python'), findsOneWidget);
      expect(find.text('Swift'), findsOneWidget);
    });

    testWidgets('should display border radius examples', (tester) async {
      await tester.pumpWidget(const MaterialApp(home: DesignTokensScreen()));

      expect(find.text('Border Radius'), findsOneWidget);
      expect(find.text('radius4'), findsOneWidget);
      expect(find.text('radius8'), findsOneWidget);
      expect(find.text('radius12'), findsOneWidget);
      expect(find.text('radius16'), findsOneWidget);
    });

    testWidgets('should display elevation examples', (tester) async {
      await tester.pumpWidget(const MaterialApp(home: DesignTokensScreen()));

      expect(find.text('Elevation'), findsOneWidget);
      expect(find.text('elevation0'), findsOneWidget);
      expect(find.text('elevation1'), findsOneWidget);
      expect(find.text('elevation3'), findsOneWidget);
      expect(find.text('elevation8'), findsOneWidget);
    });

    testWidgets('should be scrollable', (tester) async {
      await tester.pumpWidget(const MaterialApp(home: DesignTokensScreen()));

      expect(find.byType(SingleChildScrollView), findsOneWidget);
    });

    testWidgets('should display hex color values', (tester) async {
      await tester.pumpWidget(const MaterialApp(home: DesignTokensScreen()));

      // Should find hex color values (starting with #)
      expect(find.textContaining('#'), findsWidgets);
    });

    testWidgets('should have proper tooltip for theme toggle', (tester) async {
      await tester.pumpWidget(const MaterialApp(home: DesignTokensScreen()));

      final themeButton = find.byIcon(Icons.dark_mode);
      expect(themeButton, findsOneWidget);

      // Long press to show tooltip
      await tester.longPress(themeButton);
      await tester.pump();

      expect(find.text('Switch to Dark Mode'), findsOneWidget);
    });
  });
}
