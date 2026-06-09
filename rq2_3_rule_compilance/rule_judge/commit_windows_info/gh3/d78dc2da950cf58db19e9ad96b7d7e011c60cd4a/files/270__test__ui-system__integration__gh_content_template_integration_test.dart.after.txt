import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/layouts/gh_content_template.dart';
import 'package:gh3/src/ui-system/layouts/gh_screen_template.dart';
import 'package:gh3/src/ui-system/widgets/gh_content_metadata.dart';
import 'package:gh3/src/ui-system/tokens/gh_tokens.dart';

void main() {
  group('GHContentTemplate Integration', () {
    testWidgets('should integrate seamlessly with GHScreenTemplate', (
      tester,
    ) async {
      const testSections = [
        GHContentSection(title: 'Section 1', content: Text('Content 1')),
        GHContentSection(title: 'Section 2', content: Text('Content 2')),
      ];

      await tester.pumpWidget(
        MaterialApp(
          home: GHScreenTemplate(
            title: 'Test Screen',
            body: const GHContentTemplate(sections: testSections),
          ),
        ),
      );

      // Verify screen template structure
      expect(find.text('Test Screen'), findsOneWidget);
      expect(find.byType(AppBar), findsOneWidget);

      // Verify content template sections
      expect(find.text('Section 1'), findsOneWidget);
      expect(find.text('Content 1'), findsOneWidget);
      expect(find.text('Section 2'), findsOneWidget);
      expect(find.text('Content 2'), findsOneWidget);

      // Verify scrollable structure
      expect(find.byType(SingleChildScrollView), findsOneWidget);
    });

    testWidgets('should maintain consistent page margins and layout', (
      tester,
    ) async {
      const testSections = [GHContentSection(content: Text('Test Content'))];

      await tester.pumpWidget(
        MaterialApp(
          home: GHScreenTemplate(
            title: 'Test Screen',
            body: const GHContentTemplate(
              padding: EdgeInsets.all(GHTokens.spacing16),
              sections: testSections,
            ),
          ),
        ),
      );

      // Verify padding is applied
      final scrollView = tester.widget<SingleChildScrollView>(
        find.byType(SingleChildScrollView),
      );
      expect(
        scrollView.padding,
        equals(const EdgeInsets.all(GHTokens.spacing16)),
      );
    });

    testWidgets('should work with various content types', (tester) async {
      const metadataItems = [
        GHMetadataItem(icon: Icons.person, label: 'Author', value: 'Test User'),
        GHMetadataItem(
          icon: Icons.schedule,
          label: 'Created',
          value: '2 days ago',
        ),
      ];

      final testSections = [
        const GHContentSection(
          title: 'Header',
          content: Text('Header Content'),
        ),
        GHContentSection(
          title: 'Metadata',
          content: Card(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: const GHContentMetadata(items: metadataItems),
            ),
          ),
        ),
        const GHContentSection(
          title: 'Actions',
          content: Row(
            children: [
              ElevatedButton(onPressed: null, child: Text('Action 1')),
              SizedBox(width: 8),
              OutlinedButton(onPressed: null, child: Text('Action 2')),
            ],
          ),
        ),
      ];

      await tester.pumpWidget(
        MaterialApp(
          home: GHScreenTemplate(
            title: 'Integration Test',
            body: GHContentTemplate(sections: testSections),
          ),
        ),
      );

      // Verify all section types render correctly
      expect(find.text('Header'), findsOneWidget);
      expect(find.text('Header Content'), findsOneWidget);
      expect(find.text('Metadata'), findsOneWidget);
      expect(find.text('Author'), findsOneWidget);
      expect(find.text('Test User'), findsOneWidget);
      expect(find.text('Actions'), findsOneWidget);
      expect(find.text('Action 1'), findsOneWidget);
      expect(find.text('Action 2'), findsOneWidget);

      // Verify proper icon display
      expect(find.byIcon(Icons.person), findsOneWidget);
      expect(find.byIcon(Icons.schedule), findsOneWidget);
    });

    testWidgets('should handle refresh indicators correctly', (tester) async {
      const testSections = [
        GHContentSection(content: Text('Refresh Test Content')),
      ];

      await tester.pumpWidget(
        MaterialApp(
          home: GHScreenTemplate(
            title: 'Refresh Test',
            body: RefreshIndicator(
              onRefresh: () async {},
              child: const GHContentTemplate(
                physics: AlwaysScrollableScrollPhysics(),
                sections: testSections,
              ),
            ),
          ),
        ),
      );

      // Verify refresh indicator works with content template
      expect(find.byType(RefreshIndicator), findsOneWidget);
      expect(find.text('Refresh Test Content'), findsOneWidget);

      // Verify physics are properly applied
      final scrollView = tester.widget<SingleChildScrollView>(
        find.byType(SingleChildScrollView),
      );
      expect(scrollView.physics, isA<AlwaysScrollableScrollPhysics>());
    });

    testWidgets('should support custom scroll controllers', (tester) async {
      final scrollController = ScrollController();
      const testSections = [GHContentSection(content: Text('Controller Test'))];

      await tester.pumpWidget(
        MaterialApp(
          home: GHScreenTemplate(
            title: 'Controller Test',
            body: GHContentTemplate(
              scrollController: scrollController,
              sections: testSections,
            ),
          ),
        ),
      );

      // Verify controller is properly applied
      final scrollView = tester.widget<SingleChildScrollView>(
        find.byType(SingleChildScrollView),
      );
      expect(scrollView.controller, equals(scrollController));
    });

    testWidgets('should maintain proper spacing between sections', (
      tester,
    ) async {
      const testSections = [
        GHContentSection(
          title: 'First Section',
          content: Text('First Content'),
        ),
        GHContentSection(
          title: 'Second Section',
          content: Text('Second Content'),
        ),
      ];

      await tester.pumpWidget(
        MaterialApp(home: GHContentTemplate(sections: testSections)),
      );

      expect(find.text('First Section'), findsOneWidget);
      expect(find.text('Second Section'), findsOneWidget);

      final spacingBoxes = find.byWidgetPredicate(
        (widget) => widget is SizedBox && widget.height == GHTokens.spacing24,
      );
      expect(spacingBoxes, findsAtLeastNWidgets(1));
    });
  });
}
