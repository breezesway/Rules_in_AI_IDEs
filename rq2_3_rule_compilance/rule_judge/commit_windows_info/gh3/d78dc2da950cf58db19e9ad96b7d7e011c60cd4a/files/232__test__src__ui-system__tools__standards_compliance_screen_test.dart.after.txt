import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/tools/standards_compliance_screen.dart';
import 'package:gh3/src/ui-system/theme/gh_theme.dart';

void main() {
  group('StandardsComplianceScreen', () {
    testWidgets('displays screen title correctly', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const StandardsComplianceScreen(syncAuditForTesting: true),
        ),
      );

      expect(find.text('Standards Compliance'), findsOneWidget);
    });

    testWidgets('shows audit header section', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const StandardsComplianceScreen(syncAuditForTesting: true),
        ),
      );

      expect(find.text('Design System Compliance Audit'), findsOneWidget);
      expect(
        find.text(
          'Comprehensive validation of navigation patterns, spacing standards, component usage, and accessibility compliance across all example screens.',
        ),
        findsOneWidget,
      );
    });

    testWidgets('shows initial state before audit', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const StandardsComplianceScreen(syncAuditForTesting: true),
        ),
      );

      expect(find.text('Ready to Run Audit'), findsOneWidget);
      expect(
        find.text(
          'Click the button above to start a comprehensive compliance audit.',
        ),
        findsOneWidget,
      );
    });

    testWidgets('shows loading state during audit', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const StandardsComplianceScreen(
            syncAuditForTesting: false,
          ), // Use async for this test
        ),
      );

      // Trigger audit manually
      await tester.tap(find.text('Run New Audit'));
      await tester.pump();

      // Should show loading state in progress card
      expect(find.text('Running Compliance Audit...'), findsOneWidget);
      expect(
        find.text(
          'Analyzing navigation patterns, spacing, components, and accessibility.',
        ),
        findsOneWidget,
      );
      expect(find.byType(CircularProgressIndicator), findsAtLeastNWidgets(1));

      // Wait for audit to complete
      await tester.pump(const Duration(milliseconds: 200));
    });

    testWidgets('shows audit results after completion', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const StandardsComplianceScreen(syncAuditForTesting: true),
        ),
      );

      // Trigger audit manually
      await tester.tap(find.text('Run New Audit'));
      await tester.pump();

      // Wait for audit to complete (synchronous in tests)
      await tester.pump();

      expect(find.text('Overall Compliance Score'), findsOneWidget);
      expect(find.text('Navigation Patterns'), findsOneWidget);
      expect(find.text('Spacing Standards'), findsOneWidget);
      expect(find.text('Component Usage'), findsOneWidget);
      expect(find.text('Touch Targets'), findsOneWidget);
    });

    testWidgets('can manually trigger audit', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const StandardsComplianceScreen(syncAuditForTesting: true),
        ),
      );

      // Find and tap the run audit button
      final runButton = find.text('Run New Audit');
      expect(runButton, findsOneWidget);

      await tester.tap(runButton);
      await tester.pump();

      // After synchronous audit, should show results
      expect(find.text('Overall Compliance Score'), findsOneWidget);
    });

    testWidgets('has refresh button in app bar', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const StandardsComplianceScreen(syncAuditForTesting: true),
        ),
      );

      expect(find.byIcon(Icons.refresh), findsOneWidget);
    });

    testWidgets('refresh button triggers new audit', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const StandardsComplianceScreen(syncAuditForTesting: true),
        ),
      );

      // Tap refresh button
      await tester.tap(find.byIcon(Icons.refresh));
      await tester.pump();

      // After synchronous audit, should show results
      expect(find.text('Overall Compliance Score'), findsOneWidget);
    });

    testWidgets('displays compliance percentages', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const StandardsComplianceScreen(syncAuditForTesting: true),
        ),
      );

      // Trigger audit manually
      await tester.tap(find.text('Run New Audit'));
      await tester.pump();

      // Wait for audit to complete (synchronous in tests)
      await tester.pump();

      // Should show percentage values (ending with %)
      expect(
        find.textContaining('%'),
        findsAtLeastNWidgets(4),
      ); // Overall + 4 categories
    });

    testWidgets('shows compliance chips for each category', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const StandardsComplianceScreen(syncAuditForTesting: true),
        ),
      );

      // Trigger audit manually
      await tester.tap(find.text('Run New Audit'));
      await tester.pump();

      // Wait for audit to complete (synchronous in tests)
      await tester.pump();

      // Should show compliance status chips
      expect(find.text('Compliant'), findsAtLeastNWidgets(1));
      expect(find.textContaining('issues'), findsAtLeastNWidgets(1));
    });

    testWidgets('displays recommendations when present', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const StandardsComplianceScreen(syncAuditForTesting: true),
        ),
      );

      // Trigger audit manually
      await tester.tap(find.text('Run New Audit'));
      await tester.pump();

      // Wait for audit to complete (synchronous in tests)
      await tester.pump();

      // Should show recommendations sections
      expect(find.text('Recommendations:'), findsAtLeastNWidgets(1));
      expect(find.byIcon(Icons.lightbulb_outline), findsAtLeastNWidgets(1));
    });

    testWidgets('displays issues when found', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const StandardsComplianceScreen(syncAuditForTesting: true),
        ),
      );

      // Trigger audit manually
      await tester.tap(find.text('Run New Audit'));
      await tester.pump();

      // Wait for audit to complete (synchronous in tests)
      await tester.pump();

      // Should show issues sections
      expect(find.text('Issues Found:'), findsAtLeastNWidgets(1));
      expect(find.byIcon(Icons.warning), findsAtLeastNWidgets(1));
    });

    testWidgets('shows category icons', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const StandardsComplianceScreen(syncAuditForTesting: true),
        ),
      );

      // Trigger audit manually
      await tester.tap(find.text('Run New Audit'));
      await tester.pump();

      // Wait for audit to complete (synchronous in tests)
      await tester.pump();

      // Should show category-specific icons
      expect(find.byIcon(Icons.navigation), findsOneWidget);
      expect(find.byIcon(Icons.straighten), findsOneWidget);
      expect(find.byIcon(Icons.widgets), findsOneWidget);
      expect(find.byIcon(Icons.touch_app), findsOneWidget);
    });

    testWidgets('is scrollable', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const StandardsComplianceScreen(syncAuditForTesting: true),
        ),
      );

      expect(find.byType(SingleChildScrollView), findsOneWidget);
    });

    testWidgets('button is disabled during audit', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const StandardsComplianceScreen(
            syncAuditForTesting: false,
          ), // Use async to test loading state
        ),
      );

      // Trigger audit manually
      await tester.tap(find.text('Run New Audit'));
      await tester.pump();

      // Button should be disabled (showing "Running Audit..." text)
      expect(find.text('Running Audit...'), findsOneWidget);

      // Wait for the audit to complete
      await tester.pump(const Duration(milliseconds: 200));
    });
  });
}
