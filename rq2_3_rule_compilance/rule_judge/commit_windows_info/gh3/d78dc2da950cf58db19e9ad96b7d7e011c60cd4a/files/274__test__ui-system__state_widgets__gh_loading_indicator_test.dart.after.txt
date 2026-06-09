import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/state_widgets/gh_loading_indicator.dart';
import 'package:gh3/src/ui-system/tokens/gh_tokens.dart';

void main() {
  group('GHLoadingIndicator', () {
    testWidgets('should display circular progress indicator', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(home: Scaffold(body: GHLoadingIndicator())),
      );

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('should display label when provided', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHLoadingIndicator(label: 'Loading data...')),
        ),
      );

      expect(find.text('Loading data...'), findsOneWidget);
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('should not display label when not provided', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(home: Scaffold(body: GHLoadingIndicator())),
      );

      expect(find.byType(Text), findsNothing);
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('should use custom size when provided', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(home: Scaffold(body: GHLoadingIndicator(size: 48.0))),
      );

      final sizedBox = tester.widget<SizedBox>(find.byType(SizedBox).first);
      expect(sizedBox.width, equals(48.0));
      expect(sizedBox.height, equals(48.0));
    });

    testWidgets('should use custom color when provided', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHLoadingIndicator(color: Colors.red)),
        ),
      );

      final progressIndicator = tester.widget<CircularProgressIndicator>(
        find.byType(CircularProgressIndicator),
      );
      expect(progressIndicator.color, equals(Colors.red));
    });

    testWidgets('should use custom stroke width when provided', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHLoadingIndicator(strokeWidth: 4.0)),
        ),
      );

      final progressIndicator = tester.widget<CircularProgressIndicator>(
        find.byType(CircularProgressIndicator),
      );
      expect(progressIndicator.strokeWidth, equals(4.0));
    });

    testWidgets('should center content when centered is true', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHLoadingIndicator(centered: true)),
        ),
      );

      expect(find.byType(Center), findsOneWidget);
    });

    testWidgets('should not center content when centered is false', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHLoadingIndicator(centered: false)),
        ),
      );

      expect(find.byType(Center), findsNothing);
    });

    testWidgets('should apply custom padding when provided', (tester) async {
      const customPadding = EdgeInsets.all(20.0);

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHLoadingIndicator(padding: customPadding)),
        ),
      );

      final paddingWidget = tester.widget<Padding>(find.byType(Padding));
      expect(paddingWidget.padding, equals(customPadding));
    });
  });

  group('GHLoadingIndicator named constructors', () {
    testWidgets('small constructor should create 16x16 indicator', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(home: Scaffold(body: GHLoadingIndicator.small())),
      );

      final sizedBox = tester.widget<SizedBox>(find.byType(SizedBox).first);
      expect(sizedBox.width, equals(16.0));
      expect(sizedBox.height, equals(16.0));
    });

    testWidgets('medium constructor should create 24x24 indicator', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(home: Scaffold(body: GHLoadingIndicator.medium())),
      );

      final sizedBox = tester.widget<SizedBox>(find.byType(SizedBox).first);
      expect(sizedBox.width, equals(24.0));
      expect(sizedBox.height, equals(24.0));
    });

    testWidgets('large constructor should create 32x32 indicator', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(home: Scaffold(body: GHLoadingIndicator.large())),
      );

      final sizedBox = tester.widget<SizedBox>(find.byType(SizedBox).first);
      expect(sizedBox.width, equals(32.0));
      expect(sizedBox.height, equals(32.0));
    });

    testWidgets('named constructors should support label parameter', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHLoadingIndicator.large(label: 'Loading repositories...'),
          ),
        ),
      );

      expect(find.text('Loading repositories...'), findsOneWidget);
      final sizedBox = tester.widget<SizedBox>(find.byType(SizedBox).first);
      expect(sizedBox.width, equals(32.0));
      expect(sizedBox.height, equals(32.0));
    });
  });

  group('GHLoadingIndicator design token compliance', () {
    testWidgets('should use correct spacing between indicator and label', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHLoadingIndicator(label: 'Loading...')),
        ),
      );

      final sizedBoxes = find.byType(SizedBox);
      expect(sizedBoxes, findsNWidgets(2));

      final sizedBoxList = tester.widgetList<SizedBox>(sizedBoxes).toList();
      // The second SizedBox should be the spacing between indicator and label
      expect(sizedBoxList[1].height, equals(GHTokens.spacing8));
    });

    testWidgets('should use correct text style for label', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: GHLoadingIndicator(label: 'Loading...')),
        ),
      );

      final textWidget = tester.widget<Text>(find.text('Loading...'));
      // Check that it uses labelMedium style characteristics
      expect(textWidget.textAlign, equals(TextAlign.center));
    });
  });

  group('GHLoadingOverlay', () {
    testWidgets('should display child when not loading', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHLoadingOverlay(isLoading: false, child: Text('Content')),
          ),
        ),
      );

      expect(find.text('Content'), findsOneWidget);
      expect(find.byType(GHLoadingIndicator), findsNothing);
    });

    testWidgets('should display overlay when loading', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: SizedBox(
              height: 200,
              width: 200,
              child: GHLoadingOverlay(isLoading: true, child: Text('Content')),
            ),
          ),
        ),
      );

      expect(find.text('Content'), findsOneWidget);
      expect(find.byType(GHLoadingIndicator), findsOneWidget);
      expect(find.byType(Container), findsOneWidget);
    });

    testWidgets('should display message when provided', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: SizedBox(
              height: 200,
              width: 200,
              child: GHLoadingOverlay(
                isLoading: true,
                message: 'Loading data...',
                child: Text('Content'),
              ),
            ),
          ),
        ),
      );

      expect(find.text('Loading data...'), findsOneWidget);
      expect(find.byType(GHLoadingIndicator), findsOneWidget);
    });

    testWidgets('should use custom loading indicator when provided', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHLoadingOverlay(
              isLoading: true,
              loadingIndicator: Text('Custom Loading'),
              child: Text('Content'),
            ),
          ),
        ),
      );

      expect(find.text('Custom Loading'), findsOneWidget);
      expect(find.byType(GHLoadingIndicator), findsNothing);
    });
  });

  group('GHLoadingButton', () {
    testWidgets('should display button text', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHLoadingButton(text: 'Submit', onPressed: () async {}),
          ),
        ),
      );

      expect(find.text('Submit'), findsOneWidget);
      expect(find.byType(ElevatedButton), findsOneWidget);
    });

    testWidgets('should display icon when provided', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHLoadingButton(
              text: 'Submit',
              icon: Icons.send,
              onPressed: () async {},
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.send), findsOneWidget);
      expect(find.text('Submit'), findsOneWidget);
    });

    testWidgets('should show loading state when pressed', (tester) async {
      bool callbackCalled = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHLoadingButton(
              text: 'Submit',
              onPressed: () async {
                callbackCalled = true;
                await Future.delayed(const Duration(milliseconds: 10));
              },
            ),
          ),
        ),
      );

      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      expect(find.byType(GHLoadingIndicator), findsOneWidget);
      expect(callbackCalled, isTrue);

      // Wait for the async operation to complete
      await tester.pumpAndSettle();
    });

    testWidgets('should support different button styles', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Column(
              children: [
                GHLoadingButton(
                  text: 'Elevated',
                  style: GHLoadingButtonStyle.elevated,
                  onPressed: () async {},
                ),
                GHLoadingButton(
                  text: 'Outlined',
                  style: GHLoadingButtonStyle.outlined,
                  onPressed: () async {},
                ),
                GHLoadingButton(
                  text: 'Text',
                  style: GHLoadingButtonStyle.text,
                  onPressed: () async {},
                ),
              ],
            ),
          ),
        ),
      );

      expect(find.byType(ElevatedButton), findsOneWidget);
      expect(find.byType(OutlinedButton), findsOneWidget);
      expect(find.byType(TextButton), findsOneWidget);
    });

    testWidgets('should be disabled when enabled is false', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHLoadingButton(
              text: 'Submit',
              enabled: false,
              onPressed: () async {},
            ),
          ),
        ),
      );

      final button = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
      expect(button.onPressed, isNull);
    });
  });
}
