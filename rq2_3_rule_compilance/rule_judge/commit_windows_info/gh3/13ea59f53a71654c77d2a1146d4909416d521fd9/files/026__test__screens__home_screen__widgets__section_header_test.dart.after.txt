import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/screens/home_screen/widgets/section_header.dart';

void main() {
  group('SectionHeader', () {
    testWidgets('should display title with correct styling', (tester) async {
      // Arrange
      const title = 'Test Section';

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: SectionHeader(title: title),
          ),
        ),
      );

      // Assert
      expect(find.text(title), findsOneWidget);
      
      final textWidget = tester.widget<Text>(find.text(title));
      expect(textWidget.style?.fontWeight, FontWeight.bold);
    });

    testWidgets('should display different titles', (tester) async {
      // Test multiple different titles
      const titles = ['My profile', 'My work', 'Settings'];

      for (final title in titles) {
        // Act
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: SectionHeader(title: title),
            ),
          ),
        );

        // Assert
        expect(find.text(title), findsOneWidget);
        
        // Clear the widget tree for the next test
        await tester.pumpWidget(Container());
      }
    });

    testWidgets('should use theme titleLarge text style', (tester) async {
      // Arrange
      const title = 'Test Title';
      
      await tester.pumpWidget(
        MaterialApp(
          theme: ThemeData(
            textTheme: const TextTheme(
              titleLarge: TextStyle(fontSize: 24, color: Colors.red),
            ),
          ),
          home: Scaffold(
            body: SectionHeader(title: title),
          ),
        ),
      );

      // Act & Assert
      final textWidget = tester.widget<Text>(find.text(title));
      expect(textWidget.style?.fontSize, 24);
      expect(textWidget.style?.fontWeight, FontWeight.bold);
    });
  });
}