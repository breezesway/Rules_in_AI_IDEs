import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/state_widgets/gh_loading_indicator.dart';

void main() {
  group('GHLoadingTransition', () {
    testWidgets('should display loading indicator when isLoading is true', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHLoadingTransition(
              isLoading: true,
              loadingMessage: 'Loading...',
              child: Text('Content'),
            ),
          ),
        ),
      );

      expect(find.byType(GHLoadingIndicator), findsOneWidget);
      expect(find.text('Loading...'), findsOneWidget);
      expect(find.text('Content'), findsNothing);
    });

    testWidgets('should display child content when isLoading is false', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHLoadingTransition(
              isLoading: false,
              loadingMessage: 'Loading...',
              child: Text('Content'),
            ),
          ),
        ),
      );

      expect(find.byType(GHLoadingIndicator), findsNothing);
      expect(find.text('Loading...'), findsNothing);
      expect(find.text('Content'), findsOneWidget);
    });

    testWidgets('should use custom loading indicator when provided', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHLoadingTransition(
              isLoading: true,
              loadingIndicator: Text('Custom Loading'),
              child: Text('Content'),
            ),
          ),
        ),
      );

      expect(find.text('Custom Loading'), findsOneWidget);
      expect(find.byType(GHLoadingIndicator), findsNothing);
      expect(find.text('Content'), findsNothing);
    });

    testWidgets('should animate transition between states', (tester) async {
      bool isLoading = true;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: StatefulBuilder(
              builder: (context, setState) {
                return Column(
                  children: [
                    GHLoadingTransition(
                      isLoading: isLoading,
                      loadingMessage: 'Loading...',
                      duration: const Duration(milliseconds: 100),
                      child: const Text('Content'),
                    ),
                    ElevatedButton(
                      onPressed: () {
                        setState(() {
                          isLoading = !isLoading;
                        });
                      },
                      child: const Text('Toggle'),
                    ),
                  ],
                );
              },
            ),
          ),
        ),
      );

      // Initially loading
      expect(find.byType(GHLoadingIndicator), findsOneWidget);
      expect(find.text('Content'), findsNothing);

      // Toggle to content
      await tester.tap(find.text('Toggle'));
      await tester.pump();

      // During transition, AnimatedSwitcher may show both or neither
      await tester.pump(const Duration(milliseconds: 50));

      // After transition completes
      await tester.pumpAndSettle();
      expect(find.byType(GHLoadingIndicator), findsNothing);
      expect(find.text('Content'), findsOneWidget);
    });

    testWidgets('should respect custom duration', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHLoadingTransition(
              isLoading: true,
              loadingMessage: 'Loading...',
              duration: Duration(milliseconds: 500),
              child: Text('Content'),
            ),
          ),
        ),
      );

      expect(find.byType(AnimatedSwitcher), findsOneWidget);
      final animatedSwitcher = tester.widget<AnimatedSwitcher>(
        find.byType(AnimatedSwitcher),
      );
      expect(animatedSwitcher.duration, const Duration(milliseconds: 500));
    });

    testWidgets('should apply scale transition when enabled', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHLoadingTransition(
              isLoading: false,
              loadingMessage: 'Loading...',
              useScaleTransition: true,
              child: Text('Content'),
            ),
          ),
        ),
      );

      expect(find.byType(TweenAnimationBuilder<double>), findsOneWidget);
      expect(find.text('Content'), findsOneWidget);
    });

    testWidgets('should not apply scale transition when disabled', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHLoadingTransition(
              isLoading: false,
              loadingMessage: 'Loading...',
              useScaleTransition: false,
              child: Text('Content'),
            ),
          ),
        ),
      );

      expect(find.byType(TweenAnimationBuilder<double>), findsNothing);
      expect(find.text('Content'), findsOneWidget);
    });

    testWidgets('should use fade transition by default', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHLoadingTransition(
              isLoading: true,
              loadingMessage: 'Loading...',
              child: Text('Content'),
            ),
          ),
        ),
      );

      expect(find.byType(AnimatedSwitcher), findsOneWidget);
      final animatedSwitcher = tester.widget<AnimatedSwitcher>(
        find.byType(AnimatedSwitcher),
      );
      expect(animatedSwitcher.switchInCurve, Curves.easeInOut);
      expect(animatedSwitcher.switchOutCurve, Curves.easeInOut);
    });

    testWidgets('should handle no loading message gracefully', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHLoadingTransition(isLoading: true, child: Text('Content')),
          ),
        ),
      );

      expect(find.byType(GHLoadingIndicator), findsOneWidget);
      // Should use default indicator without a label
      final loadingIndicator = tester.widget<GHLoadingIndicator>(
        find.byType(GHLoadingIndicator),
      );
      expect(loadingIndicator.label, isNull);
    });

    testWidgets('should handle rapid state changes', (tester) async {
      bool isLoading = true;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: StatefulBuilder(
              builder: (context, setState) {
                return Column(
                  children: [
                    GHLoadingTransition(
                      isLoading: isLoading,
                      loadingMessage: 'Loading...',
                      duration: const Duration(milliseconds: 50),
                      child: const Text('Content'),
                    ),
                    ElevatedButton(
                      onPressed: () {
                        setState(() {
                          isLoading = !isLoading;
                        });
                      },
                      child: const Text('Toggle'),
                    ),
                  ],
                );
              },
            ),
          ),
        ),
      );

      // Rapid toggles
      await tester.tap(find.text('Toggle'));
      await tester.pump(const Duration(milliseconds: 10));
      await tester.tap(find.text('Toggle'));
      await tester.pump(const Duration(milliseconds: 10));
      await tester.tap(find.text('Toggle'));

      // Should handle rapid changes gracefully
      await tester.pumpAndSettle();
      expect(find.text('Content'), findsOneWidget);
    });
  });

  group('GHLoadingOverlay with transitions', () {
    testWidgets('should animate overlay appearance and disappearance', (
      tester,
    ) async {
      bool isLoading = true;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: StatefulBuilder(
              builder: (context, setState) {
                return Column(
                  children: [
                    SizedBox(
                      height: 200,
                      width: 200,
                      child: GHLoadingOverlay(
                        isLoading: isLoading,
                        message: 'Loading...',
                        child: const Text('Background Content'),
                      ),
                    ),
                    ElevatedButton(
                      onPressed: () {
                        setState(() {
                          isLoading = !isLoading;
                        });
                      },
                      child: const Text('Toggle'),
                    ),
                  ],
                );
              },
            ),
          ),
        ),
      );

      // Initially loading - background content should be visible
      expect(find.text('Background Content'), findsOneWidget);
      expect(find.text('Loading...'), findsOneWidget);

      // Toggle off loading
      await tester.tap(find.text('Toggle'));
      await tester.pump();

      // During transition
      await tester.pump(const Duration(milliseconds: 100));

      // After transition
      await tester.pumpAndSettle();
      expect(find.text('Background Content'), findsOneWidget);
      expect(find.text('Loading...'), findsNothing);
    });

    testWidgets('should use AnimatedOpacity for smooth transitions', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          home: GHLoadingOverlay(
            isLoading: true,
            message: 'Loading...',
            child: const Text('Background Content'),
          ),
        ),
      );

      expect(find.byType(AnimatedOpacity), findsOneWidget);
      final animatedOpacity = tester.widget<AnimatedOpacity>(
        find.byType(AnimatedOpacity),
      );
      expect(animatedOpacity.duration, const Duration(milliseconds: 200));
      expect(animatedOpacity.opacity, 1.0);
    });
  });
}
