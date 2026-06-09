import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/tools/measurement_validation_screen.dart';
import 'package:gh3/src/ui-system/theme/gh_theme.dart';

void main() {
  group('MeasurementValidationScreen', () {
    testWidgets('displays screen title correctly', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MeasurementValidationScreen(),
        ),
      );

      expect(find.text('Measurement & Validation Tools'), findsOneWidget);
    });

    testWidgets('shows developer tools section', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MeasurementValidationScreen(),
        ),
      );

      expect(find.text('Developer Tools'), findsOneWidget);
      expect(
        find.text(
          'Select a tool to inspect and validate design system implementation.',
        ),
        findsOneWidget,
      );
    });

    testWidgets('displays all tool options', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MeasurementValidationScreen(),
        ),
      );

      expect(find.text('Spacing Measurements'), findsOneWidget);
      expect(find.text('4dp Grid Lines'), findsOneWidget);
      expect(find.text('Touch Targets'), findsOneWidget);
      expect(find.text('Standards Compliance'), findsOneWidget);
    });

    testWidgets('defaults to spacing tool', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MeasurementValidationScreen(),
        ),
      );

      expect(find.text('Spacing Measurement Tool'), findsOneWidget);
      expect(
        find.text(
          'Show visual measurements of spacing between elements to verify 4dp grid compliance.',
        ),
        findsOneWidget,
      );
      expect(find.text('Show Measurements'), findsOneWidget);
    });

    testWidgets('can switch to grid tool', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MeasurementValidationScreen(),
        ),
      );

      // Switch to grid tool
      await tester.tap(find.text('4dp Grid Lines'));
      await tester.pump();

      expect(
        find.text('4dp Grid Lines'),
        findsNWidgets(2),
      ); // One in selector, one as title
      expect(
        find.text(
          'Display 4dp grid lines to visualize alignment and spacing consistency.',
        ),
        findsOneWidget,
      );
      expect(find.text('Show Grid'), findsOneWidget);
    });

    testWidgets('can switch to touch tool', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MeasurementValidationScreen(),
        ),
      );

      // Switch to touch tool
      await tester.tap(find.text('Touch Targets'));
      await tester.pump();

      expect(find.text('Touch Target Validation'), findsOneWidget);
      expect(
        find.text(
          'Highlight touch targets to ensure minimum 48dp accessibility compliance.',
        ),
        findsOneWidget,
      );
      expect(find.text('Show Touch Targets'), findsOneWidget);
    });

    testWidgets('can switch to compliance tool', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MeasurementValidationScreen(),
        ),
      );

      // Switch to compliance tool
      await tester.tap(find.text('Standards Compliance'));
      await tester.pump();

      expect(find.text('Standards Compliance Checker'), findsOneWidget);
      expect(
        find.text(
          'Automatically detect and highlight elements that don\'t follow design system standards.',
        ),
        findsOneWidget,
      );
      expect(find.text('Check Compliance'), findsOneWidget);
    });

    testWidgets('can toggle spacing measurements', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MeasurementValidationScreen(),
        ),
      );

      // Initially shows "Show Measurements"
      expect(find.text('Show Measurements'), findsOneWidget);

      // Tap to show measurements
      await tester.tap(find.text('Show Measurements'));
      await tester.pump();

      // Should change to "Hide Measurements" and show info
      expect(find.text('Hide Measurements'), findsOneWidget);
      expect(
        find.text(
          'Spacing overlay active. Red measurements indicate non-compliant spacing.',
        ),
        findsOneWidget,
      );
    });

    testWidgets('can toggle grid lines', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MeasurementValidationScreen(),
        ),
      );

      // Switch to grid tool first
      await tester.tap(find.text('4dp Grid Lines'));
      await tester.pump();

      // Initially shows "Show Grid"
      expect(find.text('Show Grid'), findsOneWidget);

      // Tap to show grid
      await tester.tap(find.text('Show Grid'));
      await tester.pump();

      // Should change to "Hide Grid" and show info
      expect(find.text('Hide Grid'), findsOneWidget);
      expect(
        find.text(
          'Grid overlay active. Elements should align to 4dp grid lines.',
        ),
        findsOneWidget,
      );
    });

    testWidgets('can toggle touch targets', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MeasurementValidationScreen(),
        ),
      );

      // Switch to touch tool first
      await tester.tap(find.text('Touch Targets'));
      await tester.pump();

      // Initially shows "Show Touch Targets"
      expect(find.text('Show Touch Targets'), findsOneWidget);

      // Tap to show touch targets
      await tester.tap(find.text('Show Touch Targets'));
      await tester.pump();

      // Should change to "Hide Touch Targets" and show info
      expect(find.text('Hide Touch Targets'), findsOneWidget);
      expect(
        find.text(
          'Touch target overlay active. Red highlights indicate touch targets smaller than 48dp.',
        ),
        findsOneWidget,
      );
    });

    testWidgets('can toggle compliance checking', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MeasurementValidationScreen(),
        ),
      );

      // Switch to compliance tool first
      await tester.tap(find.text('Standards Compliance'));
      await tester.pump();

      // Initially shows "Check Compliance"
      expect(find.text('Check Compliance'), findsOneWidget);

      // Tap to check compliance
      await tester.tap(find.text('Check Compliance'));
      await tester.pump();

      // Should change to "Hide Issues" and show compliance issues
      expect(find.text('Hide Issues'), findsOneWidget);
      expect(find.text('Compliance Issues Found'), findsOneWidget);
    });

    testWidgets('displays sample content for testing', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MeasurementValidationScreen(),
        ),
      );

      expect(find.text('Sample Content for Testing'), findsOneWidget);
      expect(find.text('Standard Card'), findsOneWidget);
      expect(find.text('Non-Compliant Card'), findsOneWidget);
      expect(find.text('Grid Test 1'), findsOneWidget);
      expect(find.text('Grid Test 2'), findsOneWidget);
    });

    testWidgets('resets overlays when switching tools', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MeasurementValidationScreen(),
        ),
      );

      // Enable spacing overlay
      await tester.tap(find.text('Show Measurements'));
      await tester.pump();
      expect(find.text('Hide Measurements'), findsOneWidget);

      // Switch to grid tool
      await tester.tap(find.text('4dp Grid Lines'));
      await tester.pump();

      // Should show "Show Grid" (overlay reset)
      expect(find.text('Show Grid'), findsOneWidget);
      expect(find.text('Hide Measurements'), findsNothing);
    });

    testWidgets('shows appropriate button labels for active overlays', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MeasurementValidationScreen(),
        ),
      );

      // Should initially show "Show Measurements"
      expect(find.text('Show Measurements'), findsOneWidget);
      expect(find.text('Hide Measurements'), findsNothing);

      // Activate overlay
      await tester.tap(find.text('Show Measurements'));
      await tester.pump();

      // Should now show "Hide Measurements"
      expect(find.text('Hide Measurements'), findsOneWidget);
      expect(find.text('Show Measurements'), findsNothing);
    });

    testWidgets('shows tool descriptions correctly', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MeasurementValidationScreen(),
        ),
      );

      const expectedDescriptions = [
        'Show visual measurements of spacing between elements to verify 4dp grid compliance.',
        'Display 4dp grid lines to visualize alignment and spacing consistency.',
        'Highlight touch targets to ensure minimum 48dp accessibility compliance.',
        'Automatically detect and highlight elements that don\'t follow design system standards.',
      ];

      final tools = [
        'Spacing Measurements',
        '4dp Grid Lines',
        'Touch Targets',
        'Standards Compliance',
      ];

      for (int i = 0; i < tools.length; i++) {
        // Switch to tool
        await tester.tap(find.text(tools[i]));
        await tester.pump();

        // Check description
        expect(find.text(expectedDescriptions[i]), findsOneWidget);
      }
    });
  });
}
