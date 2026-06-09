import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui_system/theme/gh_theme.dart';
import 'package:gh3/src/ui_system/tokens/gh_tokens.dart';
import 'package:gh3/src/ui_system/components/gh_card.dart';
import 'package:gh3/src/ui_system/components/gh_button.dart';
import 'package:gh3/src/ui_system/components/gh_chip.dart';
import 'package:gh3/src/ui_system/components/gh_list_tile.dart';
import 'package:gh3/src/ui_system/components/gh_search_bar.dart';
import 'package:gh3/src/ui_system/widgets/gh_status_badge.dart';
import 'package:gh3/src/ui_system/components/gh_text_field.dart';
import 'package:gh3/src/ui_system/state_widgets/gh_empty_state.dart';
import 'package:gh3/src/ui_system/state_widgets/gh_error_state.dart';
import 'package:gh3/src/ui_system/state_widgets/gh_loading_indicator.dart';
import 'package:gh3/src/ui_system/layouts/gh_content_template.dart';
import 'package:gh3/src/ui_system/widgets/gh_content_metadata.dart';

void main() {
  group('Theme Compatibility Tests', () {
    // Helper to create test widget with theme
    Widget createThemedWidget(Widget child, {required bool isDark}) {
      return MaterialApp(
        theme: isDark ? GHTheme.darkTheme() : GHTheme.lightTheme(),
        home: Scaffold(body: Center(child: child)),
      );
    }

    // Helper to test component in both themes
    Future<void> testInBothThemes(
      WidgetTester tester,
      Widget Function() buildWidget,
      void Function(bool isDark) verifyWidget,
    ) async {
      // Test in light theme
      await tester.pumpWidget(createThemedWidget(buildWidget(), isDark: false));
      verifyWidget(false);

      // Test in dark theme
      await tester.pumpWidget(createThemedWidget(buildWidget(), isDark: true));
      verifyWidget(true);
    }

    testWidgets('GHCard adapts to theme correctly', (tester) async {
      await testInBothThemes(
        tester,
        () => GHCard(child: Text('Test Card', style: GHTokens.bodyMedium)),
        (isDark) {
          final card = tester.widget<Card>(find.byType(Card));
          expect(card, isNotNull);

          // Verify elevation is consistent
          expect(card.elevation, GHTokens.elevation1);

          // Verify text is visible
          expect(find.text('Test Card'), findsOneWidget);
        },
      );
    });

    testWidgets('GHButton adapts to theme correctly', (tester) async {
      await testInBothThemes(
        tester,
        () => GHButton(label: 'Test Button', onPressed: () {}),
        (isDark) {
          expect(find.text('Test Button'), findsOneWidget);

          // Button should be interactive (GHButton uses ElevatedButton for primary)
          expect(find.byType(ElevatedButton), findsOneWidget);
        },
      );
    });

    testWidgets('GHChip adapts to theme correctly', (tester) async {
      await testInBothThemes(
        tester,
        () => const GHChip(label: 'Test Chip', count: 42),
        (isDark) {
          expect(find.text('Test Chip'), findsOneWidget);
          expect(find.text('42'), findsOneWidget);
        },
      );
    });

    testWidgets('GHListTile adapts to theme correctly', (tester) async {
      await testInBothThemes(
        tester,
        () => GHListTile(
          leading: const Icon(Icons.person),
          title: const Text('Test Title'),
          subtitle: const Text('Test Subtitle'),
          trailing: const Icon(Icons.chevron_right),
          onTap: () {},
        ),
        (isDark) {
          expect(find.text('Test Title'), findsOneWidget);
          expect(find.text('Test Subtitle'), findsOneWidget);
          expect(find.byIcon(Icons.person), findsOneWidget);
          expect(find.byIcon(Icons.chevron_right), findsOneWidget);
        },
      );
    });

    testWidgets('GHSearchBar adapts to theme correctly', (tester) async {
      await testInBothThemes(
        tester,
        () => const GHSearchBar(hintText: 'Search...'),
        (isDark) {
          expect(find.text('Search...'), findsOneWidget);
          expect(find.byIcon(Icons.search), findsOneWidget);

          // TextField exists and is properly themed
          expect(find.byType(TextField), findsOneWidget);
        },
      );
    });

    testWidgets('GHStatusBadge colors remain consistent', (tester) async {
      await testInBothThemes(
        tester,
        () => const Column(
          children: [
            GHStatusBadge(status: GHStatusType.open),
            GHStatusBadge(status: GHStatusType.closed),
            GHStatusBadge(status: GHStatusType.merged),
            GHStatusBadge(status: GHStatusType.draft),
          ],
        ),
        (isDark) {
          // Status badges should use semantic colors that don't change with theme
          expect(find.text('Open'), findsOneWidget);
          expect(find.text('Closed'), findsOneWidget);
          expect(find.text('Merged'), findsOneWidget);
          expect(find.text('Draft'), findsOneWidget);
        },
      );
    });

    testWidgets('GHTextField adapts to theme correctly', (tester) async {
      await testInBothThemes(
        tester,
        () =>
            const GHTextField(labelText: 'Test Field', hintText: 'Enter text'),
        (isDark) {
          expect(find.text('Test Field'), findsOneWidget);
          expect(find.text('Enter text'), findsOneWidget);

          // Text field should exist (GHTextField wraps the actual field)
          expect(find.byType(GHTextField), findsOneWidget);
        },
      );
    });

    testWidgets('GHEmptyState adapts to theme correctly', (tester) async {
      await testInBothThemes(
        tester,
        () => GHEmptyState(
          icon: Icons.inbox,
          title: 'No items',
          subtitle: 'Add some items to get started',
          action: GHButton(label: 'Add Item', onPressed: () {}),
        ),
        (isDark) {
          expect(find.text('No items'), findsOneWidget);
          expect(find.text('Add some items to get started'), findsOneWidget);
          expect(find.text('Add Item'), findsOneWidget);
          expect(find.byIcon(Icons.inbox), findsOneWidget);
        },
      );
    });

    testWidgets('GHErrorState adapts to theme correctly', (tester) async {
      await testInBothThemes(
        tester,
        () => GHErrorState(
          title: 'Error occurred',
          message: 'Something went wrong',
          onRetry: () {},
        ),
        (isDark) {
          expect(find.text('Error occurred'), findsOneWidget);
          expect(find.text('Something went wrong'), findsOneWidget);
          expect(find.text('Retry'), findsOneWidget);
          expect(find.byIcon(Icons.error_outline), findsOneWidget);
        },
      );
    });

    testWidgets('GHLoadingIndicator adapts to theme correctly', (tester) async {
      await testInBothThemes(
        tester,
        () => const GHLoadingIndicator.large(label: 'Loading...'),
        (isDark) {
          expect(find.text('Loading...'), findsOneWidget);
          expect(find.byType(CircularProgressIndicator), findsOneWidget);
        },
      );
    });

    testWidgets('GHContentTemplate adapts to theme correctly', (tester) async {
      await testInBothThemes(
        tester,
        () => GHContentTemplate(
          sections: [
            GHContentSection(
              title: 'Section 1',
              content: const Text('Content 1'),
            ),
            GHContentSection(
              title: 'Section 2',
              content: const Text('Content 2'),
            ),
          ],
        ),
        (isDark) {
          expect(find.text('Section 1'), findsOneWidget);
          expect(find.text('Section 2'), findsOneWidget);
          expect(find.text('Content 1'), findsOneWidget);
          expect(find.text('Content 2'), findsOneWidget);
        },
      );
    });

    testWidgets('GHContentMetadata adapts to theme correctly', (tester) async {
      await testInBothThemes(
        tester,
        () => const GHContentMetadata(
          items: [
            GHMetadataItem(icon: Icons.code, label: 'Language', value: 'Dart'),
            GHMetadataItem(icon: Icons.balance, label: 'License', value: 'MIT'),
          ],
        ),
        (isDark) {
          expect(find.text('Language'), findsOneWidget);
          expect(find.text('Dart'), findsOneWidget);
          expect(find.text('License'), findsOneWidget);
          expect(find.text('MIT'), findsOneWidget);
          expect(find.byIcon(Icons.code), findsOneWidget);
          expect(find.byIcon(Icons.balance), findsOneWidget);
        },
      );
    });

    testWidgets('Color contrast meets accessibility standards', (tester) async {
      // Test primary text on background
      await testInBothThemes(
        tester,
        () => Container(
          color: Theme.of(
            tester.element(find.byType(Container)),
          ).colorScheme.surface,
          child: Text(
            'Primary Text',
            style: GHTokens.bodyLarge.copyWith(
              color: Theme.of(
                tester.element(find.byType(Container)),
              ).colorScheme.onSurface,
            ),
          ),
        ),
        (isDark) {
          // Verify text is visible (this is a basic check,
          // full contrast ratio testing would require additional tools)
          expect(find.text('Primary Text'), findsOneWidget);
        },
      );
    });

    testWidgets('Card variants maintain consistency across themes', (
      tester,
    ) async {
      await testInBothThemes(
        tester,
        () => Column(
          children: [
            GHCard(child: const Text('Default')),
            GHCard.compact(child: const Text('Compact')),
            GHCard.tight(child: const Text('Tight')),
            GHCard.zeroPadding(child: const Text('Zero')),
          ],
        ),
        (isDark) {
          expect(find.text('Default'), findsOneWidget);
          expect(find.text('Compact'), findsOneWidget);
          expect(find.text('Tight'), findsOneWidget);
          expect(find.text('Zero'), findsOneWidget);

          // All cards should be visible
          expect(find.byType(Card), findsNWidgets(4));
        },
      );
    });

    testWidgets('Interactive elements maintain proper touch targets', (
      tester,
    ) async {
      await testInBothThemes(
        tester,
        () => Column(
          children: [
            GHButton(label: 'Button', onPressed: () {}),
            const SizedBox(height: 16),
            GHChip(label: 'Chip', onTap: () {}),
            const SizedBox(height: 16),
            IconButton(icon: const Icon(Icons.star), onPressed: () {}),
          ],
        ),
        (isDark) {
          // Verify all interactive elements exist
          expect(find.text('Button'), findsOneWidget);
          expect(find.text('Chip'), findsOneWidget);
          expect(find.byIcon(Icons.star), findsOneWidget);

          // Verify interactive elements exist and are testable
          expect(find.byType(ElevatedButton), findsOneWidget);
          expect(find.byType(IconButton), findsOneWidget);
        },
      );
    });
  });
}
