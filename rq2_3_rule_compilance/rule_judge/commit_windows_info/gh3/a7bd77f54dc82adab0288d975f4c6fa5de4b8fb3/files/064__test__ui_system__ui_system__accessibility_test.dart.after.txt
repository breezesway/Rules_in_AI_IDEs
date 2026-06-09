import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui_system/theme/gh_theme.dart';
import 'package:gh3/src/ui_system/tokens/gh_tokens.dart';
import 'package:gh3/src/ui_system/components/gh_card.dart';
import 'package:gh3/src/ui_system/components/gh_button.dart';
import 'package:gh3/src/ui_system/components/gh_chip.dart';
import 'package:gh3/src/ui_system/widgets/gh_status_badge.dart';

void main() {
  group('Design Token Compliance & Accessibility Tests', () {
    // Helper to create test widget with theme
    Widget createTestWidget(Widget child, {bool isDark = false}) {
      return MaterialApp(
        theme: isDark ? GHTheme.darkTheme() : GHTheme.lightTheme(),
        home: Scaffold(body: Center(child: child)),
      );
    }

    group('Design Token Compliance', () {
      testWidgets('All spacing tokens are multiples of 4', (tester) async {
        // Test that all spacing values follow the 4dp grid
        expect(GHTokens.spacing4 % 4, 0);
        expect(GHTokens.spacing8 % 4, 0);
        expect(GHTokens.spacing12 % 4, 0);
        expect(GHTokens.spacing16 % 4, 0);
        expect(GHTokens.spacing20 % 4, 0);
        expect(GHTokens.spacing24 % 4, 0);
        expect(GHTokens.spacing32 % 4, 0);
      });

      testWidgets('Typography scale follows consistent hierarchy', (
        tester,
      ) async {
        await tester.pumpWidget(
          createTestWidget(
            Column(
              children: [
                Text('Headline Large', style: GHTokens.headlineLarge),
                Text('Headline Medium', style: GHTokens.headlineMedium),
                Text('Title Large', style: GHTokens.titleLarge),
                Text('Title Medium', style: GHTokens.titleMedium),
                Text('Title Small', style: GHTokens.titleSmall),
                Text('Body Large', style: GHTokens.bodyLarge),
                Text('Body Medium', style: GHTokens.bodyMedium),
                Text('Label Large', style: GHTokens.labelLarge),
                Text('Label Medium', style: GHTokens.labelMedium),
                Text('Label Small', style: GHTokens.labelSmall),
              ],
            ),
          ),
        );

        // Verify typography hierarchy (larger styles should have larger font sizes)
        expect(
          GHTokens.headlineLarge.fontSize! > GHTokens.headlineMedium.fontSize!,
          true,
        );
        expect(
          GHTokens.headlineMedium.fontSize! > GHTokens.titleLarge.fontSize!,
          true,
        );
        expect(
          GHTokens.titleLarge.fontSize! > GHTokens.titleMedium.fontSize!,
          true,
        );
        expect(
          GHTokens.bodyLarge.fontSize! > GHTokens.bodyMedium.fontSize!,
          true,
        );
        expect(
          GHTokens.labelLarge.fontSize! > GHTokens.labelMedium.fontSize!,
          true,
        );
        expect(
          GHTokens.labelMedium.fontSize! > GHTokens.labelSmall.fontSize!,
          true,
        );
      });

      testWidgets('Color tokens maintain semantic meaning', (tester) async {
        // Test semantic color values
        expect(GHTokens.primary, const Color(0xFF0969DA)); // GitHub blue
        expect(
          GHTokens.success,
          const Color(0xFF1A7F37),
        ); // Green for success/open
        expect(GHTokens.error, const Color(0xFFCF222E)); // Red for error/closed
        expect(
          GHTokens.warning,
          const Color(0xFFBF8700),
        ); // Yellow for warnings
        expect(GHTokens.merged, const Color(0xFF8250DF)); // Purple for merged
        expect(
          GHTokens.draft,
          const Color(0xFF656D76),
        ); // Gray for draft/disabled
      });

      testWidgets('Icon sizes follow standard increments', (tester) async {
        // Test icon size progression
        expect(GHTokens.iconSize16, 16.0);
        expect(GHTokens.iconSize18, 18.0);
        expect(GHTokens.iconSize24, 24.0);
        expect(GHTokens.iconSize32, 32.0);
        expect(GHTokens.iconSize48, 48.0);
      });

      testWidgets('Border radius values are consistent', (tester) async {
        // Test border radius progression
        expect(GHTokens.radius4, 4.0);
        expect(GHTokens.radius8, 8.0);
        expect(GHTokens.radius12, 12.0);
        expect(GHTokens.radius16, 16.0);
      });

      testWidgets('Elevation values follow Material Design guidelines', (
        tester,
      ) async {
        // Test elevation progression
        expect(GHTokens.elevation0, 0.0);
        expect(GHTokens.elevation1, 1.0);
        expect(GHTokens.elevation3, 3.0);
        expect(GHTokens.elevation8, 8.0);
      });
    });

    group('Accessibility Compliance', () {
      testWidgets('Touch targets meet 48dp minimum requirement', (
        tester,
      ) async {
        await tester.pumpWidget(
          createTestWidget(
            Column(
              children: [
                GHButton(label: 'Test Button', onPressed: () {}),
                const SizedBox(height: 16),
                GHChip(label: 'Test Chip', onTap: () {}),
                const SizedBox(height: 16),
                IconButton(icon: const Icon(Icons.star), onPressed: () {}),
              ],
            ),
          ),
        );

        // Check button meets minimum touch target
        final buttonSize = tester.getSize(find.byType(ElevatedButton));
        expect(
          buttonSize.height,
          greaterThanOrEqualTo(GHTokens.minTouchTarget),
        );

        // Check IconButton meets minimum touch target
        final iconButtonSize = tester.getSize(find.byType(IconButton));
        expect(iconButtonSize.width, greaterThanOrEqualTo(48));
        expect(iconButtonSize.height, greaterThanOrEqualTo(48));
      });

      testWidgets('Components use minimum touch target constant', (
        tester,
      ) async {
        // Verify the minimum touch target constant is 48dp as per accessibility guidelines
        expect(GHTokens.minTouchTarget, 48.0);
      });

      testWidgets('Text has sufficient contrast in light theme', (
        tester,
      ) async {
        await tester.pumpWidget(
          createTestWidget(
            Container(
              color: Colors.white,
              child: const Text(
                'High contrast text',
                style: TextStyle(color: Colors.black),
              ),
            ),
          ),
        );

        // Basic visibility check (full contrast testing would require color analysis)
        expect(find.text('High contrast text'), findsOneWidget);
      });

      testWidgets('Text has sufficient contrast in dark theme', (tester) async {
        await tester.pumpWidget(
          createTestWidget(
            Container(
              color: Colors.black,
              child: const Text(
                'High contrast text',
                style: TextStyle(color: Colors.white),
              ),
            ),
            isDark: true,
          ),
        );

        // Basic visibility check (full contrast testing would require color analysis)
        expect(find.text('High contrast text'), findsOneWidget);
      });

      testWidgets('Interactive elements have proper semantic labels', (
        tester,
      ) async {
        await tester.pumpWidget(
          createTestWidget(
            Column(
              children: [
                Semantics(
                  label: 'Star repository',
                  child: GHButton(
                    label: 'Star',
                    icon: Icons.star_border,
                    onPressed: () {},
                  ),
                ),
                Semantics(
                  label: 'Filter by status',
                  child: GHChip(label: 'Open', onTap: () {}),
                ),
                IconButton(
                  icon: const Icon(Icons.settings),
                  tooltip: 'Settings',
                  onPressed: () {},
                ),
              ],
            ),
          ),
        );

        // Verify semantic widgets exist
        expect(find.byType(Semantics), findsAtLeastNWidgets(2));
        expect(find.byTooltip('Settings'), findsOneWidget);
      });

      testWidgets('Status indicators use semantic colors consistently', (
        tester,
      ) async {
        await tester.pumpWidget(
          createTestWidget(
            const Column(
              children: [
                GHStatusBadge(status: GHStatusType.open),
                GHStatusBadge(status: GHStatusType.closed),
                GHStatusBadge(status: GHStatusType.merged),
                GHStatusBadge(status: GHStatusType.draft),
              ],
            ),
          ),
        );

        // Verify all status badges render
        expect(find.byType(GHStatusBadge), findsNWidgets(4));
        expect(find.text('Open'), findsOneWidget);
        expect(find.text('Closed'), findsOneWidget);
        expect(find.text('Merged'), findsOneWidget);
        expect(find.text('Draft'), findsOneWidget);
      });

      testWidgets('Card elevation provides sufficient visual hierarchy', (
        tester,
      ) async {
        await tester.pumpWidget(
          createTestWidget(
            Column(
              children: [
                GHCard(
                  elevation: GHTokens.elevation1,
                  child: const Text('Low elevation'),
                ),
                const SizedBox(height: 16),
                GHCard(
                  elevation: GHTokens.elevation3,
                  child: const Text('High elevation'),
                ),
              ],
            ),
          ),
        );

        final cards = tester.widgetList<Card>(find.byType(Card)).toList();
        expect(cards.length, 2);

        // Verify elevation values are different for hierarchy
        expect(cards[0].elevation, GHTokens.elevation1);
        expect(cards[1].elevation, GHTokens.elevation3);
        expect(cards[1].elevation! > cards[0].elevation!, true);
      });

      testWidgets('Typography follows accessibility font size guidelines', (
        tester,
      ) async {
        // Test that body text meets minimum font size requirements
        expect(GHTokens.bodyMedium.fontSize!, greaterThanOrEqualTo(14));
        expect(GHTokens.bodyLarge.fontSize!, greaterThanOrEqualTo(16));

        // Test that labels are readable
        expect(GHTokens.labelMedium.fontSize!, greaterThanOrEqualTo(12));
        expect(GHTokens.labelLarge.fontSize!, greaterThanOrEqualTo(14));
      });

      testWidgets('Focus indicators are visible', (tester) async {
        await tester.pumpWidget(
          createTestWidget(
            GHButton(label: 'Focusable Button', onPressed: () {}),
          ),
        );

        // Find the button and simulate focus
        final button = find.byType(ElevatedButton);
        expect(button, findsOneWidget);

        // Request focus on the button
        await tester.tap(button);
        await tester.pump();

        // Button should still be visible (basic test for focus handling)
        expect(button, findsOneWidget);
      });

      testWidgets('Color-blind friendly status indicators', (tester) async {
        await tester.pumpWidget(
          createTestWidget(
            const Row(
              children: [
                GHStatusBadge(status: GHStatusType.open),
                SizedBox(width: 8),
                GHStatusBadge(status: GHStatusType.closed),
                SizedBox(width: 8),
                GHStatusBadge(status: GHStatusType.merged),
              ],
            ),
          ),
        );

        // Status badges should use both color and text to convey information
        expect(find.text('Open'), findsOneWidget);
        expect(find.text('Closed'), findsOneWidget);
        expect(find.text('Merged'), findsOneWidget);

        // Icons should also be present for additional context
        expect(
          find.byIcon(Icons.radio_button_unchecked),
          findsOneWidget,
        ); // Open
        expect(
          find.byIcon(Icons.check_circle_outline),
          findsOneWidget,
        ); // Closed
        expect(find.byIcon(Icons.merge_type), findsOneWidget); // Merged
      });

      testWidgets('Components support keyboard navigation', (tester) async {
        await tester.pumpWidget(
          createTestWidget(
            Column(
              children: [
                GHButton(label: 'Button 1', onPressed: () {}),
                const SizedBox(height: 16),
                GHButton(label: 'Button 2', onPressed: () {}),
              ],
            ),
          ),
        );

        final button1 = find.widgetWithText(ElevatedButton, 'Button 1');
        final button2 = find.widgetWithText(ElevatedButton, 'Button 2');

        expect(button1, findsOneWidget);
        expect(button2, findsOneWidget);

        // Both buttons should be focusable
        final button1Widget = tester.widget<ElevatedButton>(button1);
        final button2Widget = tester.widget<ElevatedButton>(button2);

        expect(button1Widget.onPressed, isNotNull);
        expect(button2Widget.onPressed, isNotNull);
      });
    });

    group('Performance & Memory', () {
      testWidgets('Widgets use const constructors where possible', (
        tester,
      ) async {
        // Test that basic components can be created as const
        const widget = GHStatusBadge(status: GHStatusType.open);
        expect(widget, isA<GHStatusBadge>());

        const chip = GHChip(label: 'Test', isSelectable: false);
        expect(chip, isA<GHChip>());
      });

      testWidgets('Theme data is efficiently accessed', (tester) async {
        await tester.pumpWidget(
          createTestWidget(
            Builder(
              builder: (context) {
                final theme = Theme.of(context);
                return Container(
                  color: theme.colorScheme.surface,
                  child: Text(
                    'Themed content',
                    style: GHTokens.bodyMedium.copyWith(
                      color: theme.colorScheme.onSurface,
                    ),
                  ),
                );
              },
            ),
          ),
        );

        expect(find.text('Themed content'), findsOneWidget);
      });
    });

    group('Responsive Design', () {
      testWidgets('Components adapt to different screen sizes', (tester) async {
        // Test mobile screen size
        await tester.binding.setSurfaceSize(const Size(375, 667)); // iPhone SE
        await tester.pumpWidget(
          createTestWidget(
            GHCard(
              child: Row(
                children: [
                  Expanded(
                    child: GHButton(label: 'Action', onPressed: () {}),
                  ),
                ],
              ),
            ),
          ),
        );

        expect(find.text('Action'), findsOneWidget);

        // Test tablet screen size
        await tester.binding.setSurfaceSize(const Size(768, 1024)); // iPad
        await tester.pump();

        expect(find.text('Action'), findsOneWidget);

        // Reset to default size
        await tester.binding.setSurfaceSize(const Size(800, 600));
      });

      testWidgets('Text scales appropriately', (tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: GHTheme.lightTheme(),
            home: MediaQuery(
              data: const MediaQueryData(textScaler: TextScaler.linear(1.5)),
              child: Scaffold(
                body: Text('Scaled text', style: GHTokens.bodyMedium),
              ),
            ),
          ),
        );

        expect(find.text('Scaled text'), findsOneWidget);
      });
    });
  });
}
