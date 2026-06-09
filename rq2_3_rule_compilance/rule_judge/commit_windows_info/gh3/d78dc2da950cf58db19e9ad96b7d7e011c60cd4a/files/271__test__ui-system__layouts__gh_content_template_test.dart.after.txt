import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/layouts/gh_content_template.dart';
import 'package:gh3/src/ui-system/tokens/gh_tokens.dart';

void main() {
  group('GHContentTemplate', () {
    testWidgets('should display sections with proper spacing', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentTemplate(
              sections: [
                Container(height: 50, color: Colors.red),
                Container(height: 50, color: Colors.green),
                Container(height: 50, color: Colors.blue),
              ],
            ),
          ),
        ),
      );

      expect(find.byType(Container), findsNWidgets(3));
      expect(find.byType(SingleChildScrollView), findsOneWidget);
    });

    testWidgets('should display header when provided', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: GHContentTemplate(
            header: const Text('Header'),
            sections: [Container(height: 50, color: Colors.red)],
          ),
        ),
      );

      expect(find.text('Header'), findsOneWidget);
      expect(find.byType(Container), findsOneWidget);
    });

    testWidgets('should display actions when provided', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentTemplate(
              sections: [Container(height: 50, color: Colors.red)],
              actions: [
                ElevatedButton(onPressed: () {}, child: const Text('Action 1')),
                ElevatedButton(onPressed: () {}, child: const Text('Action 2')),
              ],
            ),
          ),
        ),
      );

      expect(find.text('Action 1'), findsOneWidget);
      expect(find.text('Action 2'), findsOneWidget);
      expect(find.byType(ElevatedButton), findsNWidgets(2));
    });

    testWidgets('should show dividers when enabled', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentTemplate(
              showDividers: true,
              sections: [
                Container(height: 50, color: Colors.red),
                Container(height: 50, color: Colors.green),
              ],
            ),
          ),
        ),
      );

      // Should have dividers between sections
      final dividers = find.byWidgetPredicate(
        (widget) =>
            widget is Container &&
            widget.margin ==
                const EdgeInsets.symmetric(vertical: GHTokens.spacing12),
      );
      expect(dividers, findsOneWidget); // One divider between 2 sections
    });

    testWidgets('should use custom divider when provided', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentTemplate(
              showDividers: true,
              divider: const Text('Custom Divider'),
              sections: [
                Container(height: 50, color: Colors.red),
                Container(height: 50, color: Colors.green),
              ],
            ),
          ),
        ),
      );

      expect(find.text('Custom Divider'), findsOneWidget);
    });

    testWidgets('should use custom padding when provided', (tester) async {
      const customPadding = EdgeInsets.all(32.0);

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentTemplate(
              padding: customPadding,
              sections: [Container(height: 50, color: Colors.red)],
            ),
          ),
        ),
      );

      final scrollView = tester.widget<SingleChildScrollView>(
        find.byType(SingleChildScrollView),
      );
      expect(scrollView.padding, equals(customPadding));
    });

    testWidgets('should apply custom scroll controller', (tester) async {
      final controller = ScrollController();

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentTemplate(
              scrollController: controller,
              sections: [Container(height: 50, color: Colors.red)],
            ),
          ),
        ),
      );

      final scrollView = tester.widget<SingleChildScrollView>(
        find.byType(SingleChildScrollView),
      );
      expect(scrollView.controller, equals(controller));
    });

    testWidgets('should apply custom cross axis alignment', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentTemplate(
              crossAxisAlignment: CrossAxisAlignment.center,
              sections: [Container(height: 50, color: Colors.red)],
            ),
          ),
        ),
      );

      final column = tester.widget<Column>(find.byType(Column));
      expect(column.crossAxisAlignment, equals(CrossAxisAlignment.center));
    });

    testWidgets('should handle empty sections list', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHContentTemplate(sections: [])),
        ),
      );

      expect(find.byType(SingleChildScrollView), findsOneWidget);
      expect(find.byType(Column), findsOneWidget);
    });

    testWidgets('should handle empty actions list', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentTemplate(
              sections: [Container(height: 50, color: Colors.red)],
              actions: [],
            ),
          ),
        ),
      );

      expect(find.byType(SingleChildScrollView), findsOneWidget);
      expect(find.byType(Wrap), findsNothing);
    });

    group('spacing verification', () {
      testWidgets('should use 24dp spacing between sections', (tester) async {
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: GHContentTemplate(
                sections: [
                  Container(height: 50, color: Colors.red),
                  Container(height: 50, color: Colors.green),
                ],
              ),
            ),
          ),
        );

        // Find SizedBox widgets used for spacing
        final sizedBoxes = find.byWidgetPredicate(
          (widget) => widget is SizedBox && widget.height == GHTokens.spacing24,
        );
        expect(sizedBoxes, findsAtLeastNWidgets(1));
      });

      testWidgets('should use 24dp spacing after header', (tester) async {
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: GHContentTemplate(
                header: const Text('Header'),
                sections: [Container(height: 50, color: Colors.red)],
              ),
            ),
          ),
        );

        final sizedBoxes = find.byWidgetPredicate(
          (widget) => widget is SizedBox && widget.height == GHTokens.spacing24,
        );
        expect(sizedBoxes, findsAtLeastNWidgets(1));
      });
    });
  });

  group('GHContentSection', () {
    testWidgets('should display title and content', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentSection(
              title: 'Section Title',
              content: Container(height: 100, color: Colors.blue),
            ),
          ),
        ),
      );

      expect(find.text('Section Title'), findsOneWidget);
      expect(find.byType(Container), findsOneWidget);
    });

    testWidgets('should display subtitle when provided', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentSection(
              title: 'Section Title',
              subtitle: 'Section subtitle',
              content: Container(height: 100, color: Colors.blue),
            ),
          ),
        ),
      );

      expect(find.text('Section Title'), findsOneWidget);
      expect(find.text('Section subtitle'), findsOneWidget);
      expect(find.byType(Container), findsOneWidget);
    });

    testWidgets('should display actions when provided', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentSection(
              title: 'Section Title',
              content: Container(height: 100, color: Colors.blue),
              actions: [
                IconButton(onPressed: () {}, icon: const Icon(Icons.edit)),
                IconButton(onPressed: () {}, icon: const Icon(Icons.delete)),
              ],
            ),
          ),
        ),
      );

      expect(find.text('Section Title'), findsOneWidget);
      expect(find.byIcon(Icons.edit), findsOneWidget);
      expect(find.byIcon(Icons.delete), findsOneWidget);
    });

    testWidgets('should hide title when showTitle is false', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentSection(
              title: 'Section Title',
              showTitle: false,
              content: Container(height: 100, color: Colors.blue),
            ),
          ),
        ),
      );

      expect(find.text('Section Title'), findsNothing);
      expect(find.byType(Container), findsOneWidget);
    });

    testWidgets('should use correct typography for title', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentSection(
              title: 'Section Title',
              content: Container(height: 100, color: Colors.blue),
            ),
          ),
        ),
      );

      final titleText = tester.widget<Text>(find.text('Section Title'));
      expect(titleText.style?.fontSize, equals(GHTokens.titleMedium.fontSize));
    });

    testWidgets('should use correct typography for subtitle', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentSection(
              title: 'Section Title',
              subtitle: 'Section subtitle',
              content: Container(height: 100, color: Colors.blue),
            ),
          ),
        ),
      );

      final subtitleText = tester.widget<Text>(find.text('Section subtitle'));
      expect(
        subtitleText.style?.fontSize,
        equals(GHTokens.bodyMedium.fontSize),
      );
    });

    testWidgets('should handle content-only section', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentSection(
              content: Container(height: 100, color: Colors.blue),
            ),
          ),
        ),
      );

      expect(find.byType(Container), findsOneWidget);
      expect(find.byType(Text), findsNothing);
    });

    group('header spacing', () {
      testWidgets('should use correct spacing between title and subtitle', (
        tester,
      ) async {
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: GHContentSection(
                title: 'Section Title',
                subtitle: 'Section subtitle',
                content: Container(height: 100, color: Colors.blue),
              ),
            ),
          ),
        );

        final sizedBoxes = find.byWidgetPredicate(
          (widget) => widget is SizedBox && widget.height == GHTokens.spacing4,
        );
        expect(sizedBoxes, findsOneWidget);
      });

      testWidgets('should use correct spacing between header and content', (
        tester,
      ) async {
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: GHContentSection(
                title: 'Section Title',
                content: Container(height: 100, color: Colors.blue),
              ),
            ),
          ),
        );

        final sizedBoxes = find.byWidgetPredicate(
          (widget) => widget is SizedBox && widget.height == GHTokens.spacing12,
        );
        expect(sizedBoxes, findsOneWidget);
      });
    });
  });

  group('integration tests', () {
    testWidgets('should work together with multiple sections', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentTemplate(
              header: const Text('Page Header'),
              sections: [
                GHContentSection(
                  title: 'Section 1',
                  subtitle: 'First section',
                  content: Container(height: 50, color: Colors.red),
                ),
                GHContentSection(
                  title: 'Section 2',
                  content: Container(height: 50, color: Colors.green),
                  actions: [
                    IconButton(onPressed: () {}, icon: const Icon(Icons.edit)),
                  ],
                ),
                GHContentSection(
                  content: Container(height: 50, color: Colors.blue),
                  showTitle: false,
                ),
              ],
              actions: [
                ElevatedButton(onPressed: () {}, child: const Text('Save')),
                TextButton(onPressed: () {}, child: const Text('Cancel')),
              ],
            ),
          ),
        ),
      );

      expect(find.text('Page Header'), findsOneWidget);
      expect(find.text('Section 1'), findsOneWidget);
      expect(find.text('First section'), findsOneWidget);
      expect(find.text('Section 2'), findsOneWidget);
      expect(find.byIcon(Icons.edit), findsOneWidget);
      expect(find.text('Save'), findsOneWidget);
      expect(find.text('Cancel'), findsOneWidget);
      expect(find.byType(Container), findsNWidgets(3));
    });

    testWidgets('should maintain proper visual hierarchy', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHContentTemplate(
              sections: [
                GHContentSection(
                  title: 'Important Section',
                  content: Column(
                    children: [
                      Container(height: 30, color: Colors.red),
                      Container(height: 30, color: Colors.green),
                    ],
                  ),
                ),
                GHContentSection(
                  title: 'Secondary Section',
                  subtitle: 'Less important information',
                  content: Container(height: 50, color: Colors.blue),
                ),
              ],
            ),
          ),
        ),
      );

      // Verify sections are properly structured
      expect(find.byType(GHContentSection), findsNWidgets(2));
      expect(find.text('Important Section'), findsOneWidget);
      expect(find.text('Secondary Section'), findsOneWidget);
      expect(find.text('Less important information'), findsOneWidget);
    });
  });
}
