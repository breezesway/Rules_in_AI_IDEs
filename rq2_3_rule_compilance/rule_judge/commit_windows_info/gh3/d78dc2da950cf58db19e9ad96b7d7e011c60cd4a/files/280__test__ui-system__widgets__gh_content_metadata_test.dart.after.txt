import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/widgets/gh_content_metadata.dart';
import 'package:gh3/src/ui-system/tokens/gh_tokens.dart';

void main() {
  group('GHMetadataItem', () {
    test('should create item with required parameters', () {
      const item = GHMetadataItem(label: 'Author', value: 'John Doe');

      expect(item.label, equals('Author'));
      expect(item.value, equals('John Doe'));
      expect(item.icon, isNull);
      expect(item.onTap, isNull);
      expect(item.isLink, isFalse);
    });

    test('should create item with all parameters', () {
      void onTap() {}

      final item = GHMetadataItem(
        icon: Icons.person,
        label: 'Author',
        value: 'John Doe',
        onTap: onTap,
        isLink: true,
      );

      expect(item.icon, equals(Icons.person));
      expect(item.label, equals('Author'));
      expect(item.value, equals('John Doe'));
      expect(item.onTap, equals(onTap));
      expect(item.isLink, isTrue);
    });
  });

  group('GHContentMetadata', () {
    testWidgets('should display metadata items', (tester) async {
      const items = [
        GHMetadataItem(label: 'Author', value: 'John Doe'),
        GHMetadataItem(label: 'Created', value: '2 days ago'),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHContentMetadata(items: items)),
        ),
      );

      expect(find.text('Author'), findsOneWidget);
      expect(find.text('John Doe'), findsOneWidget);
      expect(find.text('Created'), findsOneWidget);
      expect(find.text('2 days ago'), findsOneWidget);
    });

    testWidgets('should display title when provided', (tester) async {
      const items = [GHMetadataItem(label: 'Author', value: 'John Doe')];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHContentMetadata(title: 'Repository Info', items: items),
          ),
        ),
      );

      expect(find.text('Repository Info'), findsOneWidget);
      expect(find.text('Author'), findsOneWidget);
    });

    testWidgets('should not display title when not provided', (tester) async {
      const items = [GHMetadataItem(label: 'Author', value: 'John Doe')];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHContentMetadata(items: items)),
        ),
      );

      expect(find.text('Repository Info'), findsNothing);
      expect(find.text('Author'), findsOneWidget);
    });

    testWidgets('should display icons when provided', (tester) async {
      const items = [
        GHMetadataItem(icon: Icons.person, label: 'Author', value: 'John Doe'),
        GHMetadataItem(
          icon: Icons.calendar_today,
          label: 'Created',
          value: '2 days ago',
        ),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHContentMetadata(items: items)),
        ),
      );

      expect(find.byIcon(Icons.person), findsOneWidget);
      expect(find.byIcon(Icons.calendar_today), findsOneWidget);
    });

    testWidgets('should handle tappable items', (tester) async {
      bool tapped = false;
      final items = [
        GHMetadataItem(
          label: 'Website',
          value: 'github.com',
          onTap: () => tapped = true,
        ),
      ];

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: GHContentMetadata(items: items)),
        ),
      );

      await tester.tap(find.byType(InkWell).first);
      await tester.pump();

      expect(tapped, isTrue);
    });

    testWidgets('should show external link icon for tappable items', (
      tester,
    ) async {
      const items = [
        GHMetadataItem(label: 'Website', value: 'github.com', onTap: null),
        GHMetadataItem(label: 'Repository', value: 'example/repo', onTap: null),
      ];

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: GHContentMetadata(items: items)),
        ),
      );

      expect(find.byIcon(Icons.open_in_new), findsNothing);

      // Now test with tappable item
      const tappableItems = [
        GHMetadataItem(label: 'Website', value: 'github.com', onTap: null),
      ];

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentMetadata(
              items: tappableItems
                  .map(
                    (item) => GHMetadataItem(
                      label: item.label,
                      value: item.value,
                      onTap: () {},
                    ),
                  )
                  .toList(),
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.open_in_new), findsOneWidget);
    });

    testWidgets('should style link values correctly', (tester) async {
      const items = [
        GHMetadataItem(label: 'Website', value: 'github.com', isLink: true),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHContentMetadata(items: items)),
        ),
      );

      final valueText = tester.widget<Text>(find.text('github.com'));
      expect(valueText.style?.decoration, equals(TextDecoration.underline));
    });

    testWidgets('should show dividers when enabled', (tester) async {
      const items = [
        GHMetadataItem(label: 'Author', value: 'John Doe'),
        GHMetadataItem(label: 'Created', value: '2 days ago'),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHContentMetadata(items: items, showDividers: true),
          ),
        ),
      );

      // Should have one divider container between two items
      expect(find.byType(Container), findsOneWidget);
    });

    testWidgets('should use custom spacing when provided', (tester) async {
      const items = [
        GHMetadataItem(label: 'Author', value: 'John Doe'),
        GHMetadataItem(label: 'Created', value: '2 days ago'),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHContentMetadata(items: items, itemSpacing: 16.0),
          ),
        ),
      );

      final spacers = find.byWidgetPredicate(
        (widget) => widget is SizedBox && widget.height == 16.0,
      );
      expect(spacers, findsAtLeastNWidgets(1));
    });

    testWidgets('should use custom padding when provided', (tester) async {
      const customPadding = EdgeInsets.all(24.0);
      const items = [GHMetadataItem(label: 'Author', value: 'John Doe')];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHContentMetadata(items: items, padding: customPadding),
          ),
        ),
      );

      // Find the specific padding widget by looking for our custom padding
      final paddingWidgets = find.byWidgetPredicate(
        (widget) => widget is Padding && widget.padding == customPadding,
      );
      expect(paddingWidgets, findsOneWidget);
    });

    testWidgets('should handle empty items list', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHContentMetadata(items: [])),
        ),
      );

      expect(find.byType(Column), findsOneWidget);
      expect(find.byType(Text), findsNothing);
    });

    testWidgets('should use correct cross axis alignment', (tester) async {
      const items = [GHMetadataItem(label: 'Author', value: 'John Doe')];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHContentMetadata(
              items: items,
              crossAxisAlignment: CrossAxisAlignment.center,
            ),
          ),
        ),
      );

      final column = tester.widget<Column>(find.byType(Column));
      expect(column.crossAxisAlignment, equals(CrossAxisAlignment.center));
    });
  });

  group('GHMetadataChips', () {
    testWidgets('should display chips for metadata items', (tester) async {
      const items = [
        GHMetadataItem(label: 'Language', value: 'Dart'),
        GHMetadataItem(label: 'Framework', value: 'Flutter'),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHMetadataChips(items: items)),
        ),
      );

      expect(find.text('Dart'), findsOneWidget);
      expect(find.text('Flutter'), findsOneWidget);
      expect(find.byType(Wrap), findsOneWidget);
    });

    testWidgets('should display title when provided', (tester) async {
      const items = [GHMetadataItem(label: 'Language', value: 'Dart')];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHMetadataChips(title: 'Technologies', items: items),
          ),
        ),
      );

      expect(find.text('Technologies'), findsOneWidget);
      expect(find.text('Dart'), findsOneWidget);
    });

    testWidgets('should display icons in chips when provided', (tester) async {
      const items = [
        GHMetadataItem(icon: Icons.code, label: 'Language', value: 'Dart'),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHMetadataChips(items: items)),
        ),
      );

      expect(find.byIcon(Icons.code), findsOneWidget);
      expect(find.text('Dart'), findsOneWidget);
    });

    testWidgets('should handle tappable chips', (tester) async {
      bool tapped = false;
      final items = [
        GHMetadataItem(
          label: 'Tag',
          value: 'flutter',
          onTap: () => tapped = true,
        ),
      ];

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: GHMetadataChips(items: items)),
        ),
      );

      await tester.tap(find.byType(InkWell).first);
      await tester.pump();

      expect(tapped, isTrue);
    });

    testWidgets('should use custom spacing when provided', (tester) async {
      const items = [
        GHMetadataItem(label: 'Tag1', value: 'flutter'),
        GHMetadataItem(label: 'Tag2', value: 'dart'),
      ];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHMetadataChips(items: items, spacing: 12.0, runSpacing: 6.0),
          ),
        ),
      );

      final wrap = tester.widget<Wrap>(find.byType(Wrap));
      expect(wrap.spacing, equals(12.0));
      expect(wrap.runSpacing, equals(6.0));
    });

    testWidgets('should use custom padding when provided', (tester) async {
      const customPadding = EdgeInsets.all(20.0);
      const items = [GHMetadataItem(label: 'Tag', value: 'flutter')];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHMetadataChips(items: items, padding: customPadding),
          ),
        ),
      );

      // Find the specific padding widget by looking for our custom padding
      final paddingWidgets = find.byWidgetPredicate(
        (widget) => widget is Padding && widget.padding == customPadding,
      );
      expect(paddingWidgets, findsOneWidget);
    });

    testWidgets('should handle empty items list', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHMetadataChips(items: [])),
        ),
      );

      expect(find.byType(SizedBox), findsOneWidget);
      expect(find.byType(Wrap), findsNothing);
    });

    testWidgets('should use correct cross axis alignment', (tester) async {
      const items = [GHMetadataItem(label: 'Tag', value: 'flutter')];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHMetadataChips(
              items: items,
              crossAxisAlignment: CrossAxisAlignment.center,
            ),
          ),
        ),
      );

      final column = tester.widget<Column>(find.byType(Column));
      expect(column.crossAxisAlignment, equals(CrossAxisAlignment.center));
    });

    testWidgets('should style chips correctly', (tester) async {
      const items = [GHMetadataItem(label: 'Tag', value: 'flutter')];

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHMetadataChips(items: items)),
        ),
      );

      final container = tester.widget<Container>(
        find.byWidgetPredicate(
          (widget) => widget is Container && widget.decoration != null,
        ),
      );
      final decoration = container.decoration as BoxDecoration;
      expect(
        decoration.borderRadius,
        equals(BorderRadius.circular(GHTokens.radius16)),
      );
      expect(
        container.padding,
        equals(
          const EdgeInsets.symmetric(
            horizontal: GHTokens.spacing8,
            vertical: GHTokens.spacing4,
          ),
        ),
      );
    });
  });

  group('integration tests', () {
    testWidgets('should work together with various configurations', (
      tester,
    ) async {
      const standardItems = [
        GHMetadataItem(
          icon: Icons.person,
          label: 'Author',
          value: 'John Doe',
          onTap: null,
        ),
        GHMetadataItem(
          icon: Icons.link,
          label: 'Website',
          value: 'github.com',
          onTap: null,
          isLink: true,
        ),
      ];

      const chipItems = [
        GHMetadataItem(icon: Icons.code, label: 'Language', value: 'Dart'),
        GHMetadataItem(
          icon: Icons.mobile_friendly,
          label: 'Platform',
          value: 'Flutter',
        ),
      ];

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Column(
              children: [
                GHContentMetadata(
                  title: 'Repository Details',
                  items: standardItems
                      .map(
                        (item) => GHMetadataItem(
                          icon: item.icon,
                          label: item.label,
                          value: item.value,
                          onTap: item.label == 'Website' ? () {} : null,
                          isLink: item.isLink,
                        ),
                      )
                      .toList(),
                  showDividers: true,
                ),
                const SizedBox(height: 24),
                const GHMetadataChips(title: 'Technologies', items: chipItems),
              ],
            ),
          ),
        ),
      );

      // Verify standard metadata
      expect(find.text('Repository Details'), findsOneWidget);
      expect(find.text('Author'), findsOneWidget);
      expect(find.text('John Doe'), findsOneWidget);
      expect(find.text('Website'), findsOneWidget);
      expect(find.text('github.com'), findsOneWidget);

      // Verify chips
      expect(find.text('Technologies'), findsOneWidget);
      expect(find.text('Dart'), findsOneWidget);
      expect(find.text('Flutter'), findsOneWidget);

      // Verify icons
      expect(find.byIcon(Icons.person), findsOneWidget);
      expect(find.byIcon(Icons.link), findsOneWidget);
      expect(find.byIcon(Icons.code), findsOneWidget);
      expect(find.byIcon(Icons.mobile_friendly), findsOneWidget);

      // Verify external link icon for tappable item
      expect(find.byIcon(Icons.open_in_new), findsOneWidget);
    });

    testWidgets('should handle mixed content types appropriately', (
      tester,
    ) async {
      final items = [
        const GHMetadataItem(label: 'Simple', value: 'Text value'),
        GHMetadataItem(
          label: 'Link',
          value: 'Click me',
          isLink: true,
          onTap: () {},
        ),
      ];

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: GHContentMetadata(items: items)),
        ),
      );

      expect(find.text('Simple'), findsOneWidget);
      expect(find.text('Link'), findsOneWidget);
      expect(find.byIcon(Icons.open_in_new), findsOneWidget);
    });
  });
}
