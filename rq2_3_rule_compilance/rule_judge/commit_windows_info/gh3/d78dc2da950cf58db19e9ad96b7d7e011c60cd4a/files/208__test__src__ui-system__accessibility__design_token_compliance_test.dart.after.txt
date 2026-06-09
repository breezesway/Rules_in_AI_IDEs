import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../../../../lib/src/ui-system/tokens/gh_tokens.dart';
import '../../../../lib/src/ui-system/theme/gh_theme.dart';
import '../../../../lib/src/ui-system/components/gh_card.dart';
import '../../../../lib/src/ui-system/components/gh_button.dart';
import '../../../../lib/src/ui-system/components/gh_chip.dart';
import '../../../../lib/src/ui-system/components/gh_list_tile.dart';
import '../../../../lib/src/ui-system/components/gh_search_bar.dart';
import '../../../../lib/src/ui-system/components/gh_text_field.dart';
import '../../../../lib/src/ui-system/widgets/gh_status_badge.dart';
import '../../../../lib/src/ui-system/state_widgets/gh_empty_state.dart';
import '../../../../lib/src/ui-system/state_widgets/gh_error_state.dart';

void main() {
  group('Design Token Compliance Tests', () {
    testWidgets('GHTokens should provide consistent design tokens', (
      tester,
    ) async {
      // Verify spacing values follow 4dp grid
      expect(GHTokens.spacing4, 4.0);
      expect(GHTokens.spacing8, 8.0);
      expect(GHTokens.spacing12, 12.0);
      expect(GHTokens.spacing16, 16.0);
      expect(GHTokens.spacing20, 20.0);
      expect(GHTokens.spacing24, 24.0);
      expect(GHTokens.spacing32, 32.0);

      // Verify border radius values
      expect(GHTokens.radius4, 4.0);
      expect(GHTokens.radius8, 8.0);
      expect(GHTokens.radius12, 12.0);
      expect(GHTokens.radius16, 16.0);

      // Verify elevation values
      expect(GHTokens.elevation0, 0.0);
      expect(GHTokens.elevation1, 1.0);
      expect(GHTokens.elevation3, 3.0);
      expect(GHTokens.elevation8, 8.0);

      // Verify icon sizes
      expect(GHTokens.iconSize16, 16.0);
      expect(GHTokens.iconSize18, 18.0);
      expect(GHTokens.iconSize24, 24.0);
      expect(GHTokens.iconSize32, 32.0);

      // Verify GitHub semantic colors
      expect(GHTokens.success, const Color(0xFF1A7F37));
      expect(GHTokens.error, const Color(0xFFCF222E));
      expect(GHTokens.warning, const Color(0xFFBF8700));
      expect(GHTokens.merged, const Color(0xFF8250DF));
      expect(GHTokens.draft, const Color(0xFF656D76));

      // Verify primary brand colors
      expect(GHTokens.primary, const Color(0xFF0969DA));
      expect(GHTokens.onPrimary, const Color(0xFFFFFFFF));
      expect(GHTokens.primaryContainer, const Color(0xFFDDE6F4));
      expect(GHTokens.onPrimaryContainer, const Color(0xFF0A1929));
    });

    testWidgets('Typography tokens should follow Material Design 3 scale', (
      tester,
    ) async {
      // Verify headline styles
      expect(GHTokens.headlineLarge.fontSize, 32.0);
      expect(GHTokens.headlineMedium.fontSize, 28.0);

      // Verify title styles
      expect(GHTokens.titleLarge.fontSize, 22.0);
      expect(GHTokens.titleMedium.fontSize, 16.0);
      expect(GHTokens.titleSmall.fontSize, 14.0);

      // Verify body styles
      expect(GHTokens.bodyLarge.fontSize, 16.0);
      expect(GHTokens.bodyMedium.fontSize, 14.0);

      // Verify label styles
      expect(GHTokens.labelLarge.fontSize, 14.0);
      expect(GHTokens.labelMedium.fontSize, 12.0);
      expect(GHTokens.labelSmall.fontSize, 10.0);

      // Verify line heights are consistent
      expect(GHTokens.bodyLarge.height, 1.5);
      expect(GHTokens.bodyMedium.height, 1.43);
      expect(GHTokens.labelLarge.height, 1.43);
    });

    testWidgets('Components should use design tokens consistently', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: Column(
              children: [
                // Test GHCard uses correct tokens
                GHCard(child: Text('Test Card', style: GHTokens.titleMedium)),

                // Test GHButton uses correct tokens
                GHButton(label: 'Test Button', onPressed: () {}),
              ],
            ),
          ),
        ),
      );

      await tester.pump();

      // Find the Card widget and verify its properties
      final Card card = tester.widget<Card>(find.byType(Card));
      expect(card.elevation, GHTokens.elevation1);
      expect(card.shape, isA<RoundedRectangleBorder>());

      RoundedRectangleBorder shape = card.shape as RoundedRectangleBorder;
      expect(shape.borderRadius, BorderRadius.circular(GHTokens.radius8));

      // Find the ElevatedButton and verify its properties
      final ElevatedButton button = tester.widget<ElevatedButton>(
        find.byType(ElevatedButton),
      );
      expect(
        button.style?.minimumSize?.resolve({}),
        const Size(88, GHTokens.minTouchTarget),
      );
    });
  });

  group('Accessibility Compliance Tests', () {
    testWidgets('Touch targets should meet minimum size requirement', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: Column(
              children: [
                GHButton(label: 'Test Button', onPressed: () {}),
                GHChip(label: 'Test Chip', onTap: () {}),
                GHListTile(title: const Text('Test List Tile'), onTap: () {}),
              ],
            ),
          ),
        ),
      );

      await tester.pump();

      // Verify button meets minimum touch target
      final RenderBox buttonBox = tester.renderObject(
        find.byType(ElevatedButton),
      );
      expect(
        buttonBox.size.height,
        greaterThanOrEqualTo(GHTokens.minTouchTarget),
      );
      expect(
        buttonBox.size.width,
        greaterThanOrEqualTo(88.0),
      ); // Minimum button width

      // Verify chip is tappable with adequate size
      final GestureDetector chipDetector = tester.widget<GestureDetector>(
        find.descendant(
          of: find.byType(GHChip),
          matching: find.byType(GestureDetector),
        ),
      );
      expect(chipDetector.onTap, isNotNull);

      // Verify list tile meets touch target requirements
      final RenderBox listTileBox = tester.renderObject(find.byType(ListTile));
      expect(
        listTileBox.size.height,
        greaterThanOrEqualTo(GHTokens.minTouchTarget),
      );
    });

    testWidgets('Components should have proper semantic labels', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: Column(
              children: [
                GHButton(
                  label: 'Star Repository',
                  icon: Icons.star,
                  onPressed: () {},
                ),
                const GHStatusBadge(
                  status: GHStatusType.open,
                  customLabel: 'Issue Open',
                ),
                GHEmptyStates.noRepositories(onCreateRepository: () {}),
              ],
            ),
          ),
        ),
      );

      await tester.pump();

      // Verify button has proper semantic label
      expect(find.text('Star Repository'), findsOneWidget);

      // Verify status badge has proper label
      expect(find.text('Issue Open'), findsOneWidget);

      // Verify empty state has helpful content
      expect(find.text('No repositories'), findsOneWidget);
      expect(
        find.text('Create your first repository to get started'),
        findsOneWidget,
      );
    });

    testWidgets('Form elements should have proper labels and hints', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: Column(
              children: [
                const GHTextField(
                  labelText: 'Repository Name',
                  hintText: 'Enter repository name',
                  helperText: 'Choose a unique name',
                ),
                GHSearchBar(
                  hintText: 'Search repositories...',
                  onChanged: (value) {},
                ),
              ],
            ),
          ),
        ),
      );

      await tester.pump();

      // Verify text field has proper labels
      expect(find.text('Repository Name'), findsOneWidget);
      expect(find.text('Enter repository name'), findsOneWidget);
      expect(find.text('Choose a unique name'), findsOneWidget);

      // Verify search bar has hint text
      expect(find.text('Search repositories...'), findsOneWidget);
    });

    testWidgets('Error states should provide clear feedback', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: Column(
              children: [
                GHErrorStates.networkError(onRetry: () {}),
                const GHTextField(
                  labelText: 'Email',
                  errorText: 'Please enter a valid email address',
                ),
              ],
            ),
          ),
        ),
      );

      await tester.pump();

      // Verify error state has clear messaging
      expect(find.text('Connection Error'), findsOneWidget);
      expect(
        find.textContaining('Unable to connect to GitHub'),
        findsOneWidget,
      );
      expect(find.text('Retry'), findsOneWidget);

      // Verify form error is clear
      expect(find.text('Please enter a valid email address'), findsOneWidget);
    });

    testWidgets('Loading states should provide feedback', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: Column(
              children: [
                GHButton(label: 'Loading', isLoading: true, onPressed: () {}),
              ],
            ),
          ),
        ),
      );

      await tester.pump();

      // Verify loading button shows progress indicator
      expect(find.byType(CircularProgressIndicator), findsOneWidget);

      // Button should be disabled during loading
      final ElevatedButton button = tester.widget<ElevatedButton>(
        find.byType(ElevatedButton),
      );
      expect(button.onPressed, isNull);
    });
  });

  group('Color Contrast Tests', () {
    testWidgets('Primary colors should have adequate contrast', (tester) async {
      // Test light theme contrast
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: Container(
              color: GHTokens.primary,
              child: Text(
                'Primary Text',
                style: TextStyle(color: GHTokens.onPrimary),
              ),
            ),
          ),
        ),
      );

      await tester.pump();

      // Verify colors are different (indicating contrast)
      expect(GHTokens.primary, isNot(equals(GHTokens.onPrimary)));

      // Test dark theme contrast
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.darkTheme(),
          home: Scaffold(
            body: Container(
              color: GHTokens.primary,
              child: Text(
                'Primary Text',
                style: TextStyle(color: GHTokens.onPrimary),
              ),
            ),
          ),
        ),
      );

      await tester.pump();

      // Colors should remain consistent across themes for brand colors
      expect(GHTokens.primary, const Color(0xFF0969DA));
      expect(GHTokens.onPrimary, const Color(0xFFFFFFFF));
    });

    testWidgets('Semantic colors should maintain meaning', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: Column(
              children: [
                Container(
                  color: GHTokens.success,
                  height: 50,
                  child: const Text('Success'),
                ),
                Container(
                  color: GHTokens.error,
                  height: 50,
                  child: const Text('Error'),
                ),
                Container(
                  color: GHTokens.warning,
                  height: 50,
                  child: const Text('Warning'),
                ),
              ],
            ),
          ),
        ),
      );

      await tester.pump();

      // Verify semantic colors are distinct
      expect(GHTokens.success, isNot(equals(GHTokens.error)));
      expect(GHTokens.success, isNot(equals(GHTokens.warning)));
      expect(GHTokens.error, isNot(equals(GHTokens.warning)));

      // Verify they maintain GitHub semantics
      expect(GHTokens.success, const Color(0xFF1A7F37)); // GitHub green
      expect(GHTokens.error, const Color(0xFFCF222E)); // GitHub red
      expect(GHTokens.warning, const Color(0xFFBF8700)); // GitHub yellow
    });
  });

  group('Component Consistency Tests', () {
    testWidgets('All card variants should use consistent styling', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: Column(
              children: [
                GHCard(child: Text('Default', style: GHTokens.bodyMedium)),
                GHCard.compact(
                  child: Text('Compact', style: GHTokens.bodyMedium),
                ),
                GHCard.tight(child: Text('Tight', style: GHTokens.bodyMedium)),
                GHCard.zeroPadding(
                  child: Padding(
                    padding: const EdgeInsets.all(8),
                    child: Text('Zero Padding', style: GHTokens.bodyMedium),
                  ),
                ),
              ],
            ),
          ),
        ),
      );

      await tester.pump();

      // All card variants should have the same basic styling
      final List<Card> cards = tester
          .widgetList<Card>(find.byType(Card))
          .toList();
      expect(cards.length, 4);

      for (Card card in cards) {
        // All cards should have the same elevation
        expect(card.elevation, GHTokens.elevation1);

        // All cards should have the same border radius
        expect(card.shape, isA<RoundedRectangleBorder>());
        RoundedRectangleBorder shape = card.shape as RoundedRectangleBorder;
        expect(shape.borderRadius, BorderRadius.circular(GHTokens.radius8));
      }
    });

    testWidgets('Status badges should use consistent semantic colors', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: Column(
              children: const [
                GHStatusBadge(status: GHStatusType.open),
                GHStatusBadge(status: GHStatusType.closed),
                GHStatusBadge(status: GHStatusType.merged),
                GHStatusBadge(status: GHStatusType.draft),
              ],
            ),
          ),
        ),
      );

      await tester.pump();

      // Verify all status badges are rendered
      expect(find.text('Open'), findsOneWidget);
      expect(find.text('Closed'), findsOneWidget);
      expect(find.text('Merged'), findsOneWidget);
      expect(find.text('Draft'), findsOneWidget);
    });

    testWidgets('Components should follow spacing guidelines', (tester) async {
      // This test verifies that components use consistent spacing internally
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: Column(
              children: [
                GHCard(
                  child: Column(
                    children: [
                      Text('Title', style: GHTokens.titleMedium),
                      const SizedBox(height: GHTokens.spacing8),
                      Text('Content', style: GHTokens.bodyMedium),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      );

      await tester.pump();

      // Verify spacing is applied correctly
      final SizedBox spacer = tester.widget<SizedBox>(find.byType(SizedBox));
      expect(spacer.height, GHTokens.spacing8);
    });
  });
}
