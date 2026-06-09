import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/screens/home_screen/widgets/work_item_list_tile.dart';

void main() {
  group('WorkItemListTile', () {
    testWidgets('should display title and icon correctly', (tester) async {
      // Arrange
      const title = 'Issues';
      const icon = Icons.bug_report;

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: WorkItemListTile(title: title, icon: icon),
          ),
        ),
      );

      // Assert
      expect(find.text(title), findsOneWidget);
      expect(find.byIcon(icon), findsOneWidget);
      expect(find.byIcon(Icons.arrow_forward_ios), findsOneWidget);
    });

    testWidgets('should display different work items correctly', (
      tester,
    ) async {
      // Test data for different work items
      final workItems = [
        {'title': 'Issues', 'icon': Icons.bug_report},
        {'title': 'Pull requests', 'icon': Icons.call_merge},
        {'title': 'Discussions', 'icon': Icons.forum},
        {'title': 'Projects', 'icon': Icons.folder_open},
        {'title': 'Repositories', 'icon': Icons.source},
        {'title': 'Organizations', 'icon': Icons.business},
        {'title': 'Starred', 'icon': Icons.star},
      ];

      for (final item in workItems) {
        // Act
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: WorkItemListTile(
                title: item['title'] as String,
                icon: item['icon'] as IconData,
              ),
            ),
          ),
        );

        // Assert
        expect(find.text(item['title'] as String), findsOneWidget);
        expect(find.byIcon(item['icon'] as IconData), findsOneWidget);
        expect(find.byIcon(Icons.arrow_forward_ios), findsOneWidget);

        // Clear the widget tree for the next test
        await tester.pumpWidget(Container());
      }
    });

    testWidgets('should handle tap when onTap is provided', (tester) async {
      // Arrange
      bool tapped = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: WorkItemListTile(
              title: 'Issues',
              icon: Icons.bug_report,
              onTap: () => tapped = true,
            ),
          ),
        ),
      );

      // Act
      await tester.tap(find.byType(ListTile));

      // Assert
      expect(tapped, true);
    });

    testWidgets('should not crash when onTap is null', (tester) async {
      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: WorkItemListTile(
              title: 'Issues',
              icon: Icons.bug_report,
              onTap: null,
            ),
          ),
        ),
      );

      // Assert - should not crash when tapping
      await tester.tap(find.byType(ListTile));
      await tester.pump();

      // Should still render properly
      expect(find.text('Issues'), findsOneWidget);
      expect(find.byIcon(Icons.bug_report), findsOneWidget);
    });

    testWidgets('should use correct styling and colors', (tester) async {
      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: WorkItemListTile(title: 'Issues', icon: Icons.bug_report),
          ),
        ),
      );

      // Assert
      final listTile = tester.widget<ListTile>(find.byType(ListTile));
      expect(
        listTile.contentPadding,
        const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      );

      // Check that icons are present
      final leadingIcon = tester.widget<Icon>(find.byIcon(Icons.bug_report));
      final trailingIcon = tester.widget<Icon>(
        find.byIcon(Icons.arrow_forward_ios),
      );

      expect(leadingIcon, isNotNull);
      expect(trailingIcon, isNotNull);
      expect(trailingIcon.size, 16);
    });
  });
}
