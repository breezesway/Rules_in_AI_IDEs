import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/navigation/ui_system_app.dart';

void main() {
  setUp(() {
    WidgetController.hitTestWarningShouldBeFatal = false;
  });

  group('Basic UI Tests', () {
    testWidgets('UAT app should launch successfully', (tester) async {
      await tester.pumpWidget(const UISystemApp());
      await tester.pumpAndSettle();

      expect(find.text('GH3 Design System - UAT'), findsOneWidget);
      expect(find.text('Design System Showcase'), findsOneWidget);
    });

    testWidgets('should display build information', (tester) async {
      await tester.pumpWidget(const UISystemApp());
      await tester.pumpAndSettle();

      expect(find.text('Build Information'), findsOneWidget);
      expect(
        find.text('GitHub Mobile Design System v1.0.0 - Phase 4 Demo'),
        findsOneWidget,
      );
      expect(
        find.text(
          'Comprehensive stakeholder demonstration with before/after comparisons, '
          'interactive components, and professional validation tools',
        ),
        findsOneWidget,
      );
    });

    testWidgets('should display feature highlights', (tester) async {
      await tester.pumpWidget(const UISystemApp());
      await tester.pumpAndSettle();

      expect(find.text('Material Design 3 Foundation'), findsOneWidget);
      expect(find.text('Navigation Efficiency Improvements'), findsOneWidget);
      expect(find.text('Visual Consistency Through 4dp Grid'), findsOneWidget);
      expect(find.text('Enhanced State Management'), findsOneWidget);
    });
  });
}
