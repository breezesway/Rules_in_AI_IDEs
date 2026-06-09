import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/components/gh_card.dart';
import 'package:gh3/src/ui-system/tokens/gh_tokens.dart';

void main() {
  group('GHCard', () {
    testWidgets('should display child widget', (tester) async {
      const testText = 'Test Card Content';

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHCard(child: Text(testText))),
        ),
      );

      expect(find.text(testText), findsOneWidget);
    });

    testWidgets('should apply default padding', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHCard(child: Text('Content'))),
        ),
      );

      final paddings = tester.widgetList<Padding>(find.byType(Padding));
      final cardPadding = paddings.firstWhere(
        (p) => p.padding == const EdgeInsets.all(GHTokens.spacing16),
      );
      expect(
        cardPadding.padding,
        equals(const EdgeInsets.all(GHTokens.spacing16)),
      );
    });

    testWidgets('should apply custom padding when provided', (tester) async {
      const customPadding = EdgeInsets.all(GHTokens.spacing24);

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHCard(padding: customPadding, child: Text('Content')),
          ),
        ),
      );

      final paddings = tester.widgetList<Padding>(find.byType(Padding));
      final cardPadding = paddings.firstWhere(
        (p) => p.padding == customPadding,
      );
      expect(cardPadding.padding, equals(customPadding));
    });

    testWidgets('should apply default elevation', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHCard(child: Text('Content'))),
        ),
      );

      final card = tester.widget<Card>(find.byType(Card));
      expect(card.elevation, equals(GHTokens.elevation1));
    });

    testWidgets('should apply custom elevation when provided', (tester) async {
      const customElevation = GHTokens.elevation3;

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHCard(elevation: customElevation, child: Text('Content')),
          ),
        ),
      );

      final card = tester.widget<Card>(find.byType(Card));
      expect(card.elevation, equals(customElevation));
    });

    testWidgets('should apply default margin', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHCard(child: Text('Content'))),
        ),
      );

      final card = tester.widget<Card>(find.byType(Card));
      expect(card.margin, equals(const EdgeInsets.all(GHTokens.spacing4)));
    });

    testWidgets('should apply custom margin when provided', (tester) async {
      const customMargin = EdgeInsets.all(GHTokens.spacing8);

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHCard(margin: customMargin, child: Text('Content')),
          ),
        ),
      );

      final card = tester.widget<Card>(find.byType(Card));
      expect(card.margin, equals(customMargin));
    });

    testWidgets('should have correct border radius', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHCard(child: Text('Content'))),
        ),
      );

      final card = tester.widget<Card>(find.byType(Card));
      final shape = card.shape as RoundedRectangleBorder;
      expect(
        shape.borderRadius,
        equals(BorderRadius.circular(GHTokens.radius8)),
      );
    });

    testWidgets('should call onTap when tapped', (tester) async {
      bool wasTapped = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHCard(
              onTap: () {
                wasTapped = true;
              },
              child: const Text('Tappable Card'),
            ),
          ),
        ),
      );

      await tester.tap(find.byType(GHCard));
      expect(wasTapped, isTrue);
    });

    testWidgets('should not be tappable when onTap is null', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(body: GHCard(child: Text('Non-tappable Card'))),
        ),
      );

      final inkWell = tester.widget<InkWell>(find.byType(InkWell));
      expect(inkWell.onTap, isNull);
    });

    testWidgets('should have InkWell with correct border radius', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHCard(onTap: () {}, child: const Text('Content')),
          ),
        ),
      );

      final inkWell = tester.widget<InkWell>(find.byType(InkWell));
      expect(
        inkWell.borderRadius,
        equals(BorderRadius.circular(GHTokens.radius8)),
      );
    });

    testWidgets('should be accessible', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHCard(onTap: () {}, child: const Text('Accessible Card')),
          ),
        ),
      );

      // Verify that the card can be found and interacted with
      expect(find.byType(GHCard), findsOneWidget);
      expect(find.text('Accessible Card'), findsOneWidget);

      // Verify tap functionality
      await tester.tap(find.byType(GHCard));
      await tester.pump();
    });
  });
}
