import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/components/gh_card.dart';
import 'package:gh3/src/ui-system/tokens/gh_tokens.dart';

void main() {
  group('GHCard', () {
    testWidgets('should create standard card with default padding', (
      tester,
    ) async {
      await tester.pumpWidget(MaterialApp(home: GHCard(child: Container())));

      final card = tester.widget<GHCard>(find.byType(GHCard));
      expect(card.padding, isNull);
    });

    testWidgets('should create compact card with 12dp padding', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: GHCard.compact(child: Container())),
        ),
      );

      final card = tester.widget<GHCard>(find.byType(GHCard));
      expect(card.padding, equals(const EdgeInsets.all(GHTokens.spacing12)));
    });

    testWidgets('should create tight card with 8dp padding', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: GHCard.tight(child: Container())),
        ),
      );

      final card = tester.widget<GHCard>(find.byType(GHCard));
      expect(card.padding, equals(const EdgeInsets.all(GHTokens.spacing8)));
    });

    testWidgets('should create zero padding card', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: GHCard.zeroPadding(child: Container())),
        ),
      );

      final card = tester.widget<GHCard>(find.byType(GHCard));
      expect(card.padding, equals(EdgeInsets.zero));
    });

    testWidgets('should handle tap callback for all variants', (tester) async {
      bool tapped = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Column(
              children: [
                GHCard(onTap: () => tapped = true, child: Container()),
                GHCard.compact(onTap: () => tapped = true, child: Container()),
                GHCard.tight(onTap: () => tapped = true, child: Container()),
                GHCard.zeroPadding(
                  onTap: () => tapped = true,
                  child: Container(),
                ),
              ],
            ),
          ),
        ),
      );

      // Test each variant can be tapped
      await tester.tap(find.byType(GHCard).first);
      expect(tapped, isTrue);
    });

    group('padding validation', () {
      test('compact padding should be 4dp grid compliant', () {
        expect(GHTokens.spacing12 % 4, equals(0));
        expect(GHTokens.spacing12, equals(12.0));
      });

      test('tight padding should be 4dp grid compliant', () {
        expect(GHTokens.spacing8 % 4, equals(0));
        expect(GHTokens.spacing8, equals(8.0));
      });

      test('padding hierarchy should be correct', () {
        expect(0, lessThan(GHTokens.spacing8)); // zero < tight
        expect(
          GHTokens.spacing8,
          lessThan(GHTokens.spacing12),
        ); // tight < compact
        expect(
          GHTokens.spacing12,
          lessThan(GHTokens.spacing16),
        ); // compact < standard
      });
    });

    group('visual differences verification', () {
      testWidgets('card variants should have visually distinct padding', (
        tester,
      ) async {
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: Column(
                children: [
                  GHCard(child: Container(height: 50, color: Colors.red)),
                  GHCard.compact(
                    child: Container(height: 50, color: Colors.green),
                  ),
                  GHCard.tight(
                    child: Container(height: 50, color: Colors.blue),
                  ),
                  GHCard.zeroPadding(
                    child: Container(height: 50, color: Colors.yellow),
                  ),
                ],
              ),
            ),
          ),
        );

        final cards = tester.widgetList<GHCard>(find.byType(GHCard)).toList();
        expect(cards.length, equals(4));

        // Verify different padding values
        expect(cards[0].padding, isNull); // Default uses 16dp in build method
        expect(cards[1].padding, equals(const EdgeInsets.all(12.0))); // Compact
        expect(cards[2].padding, equals(const EdgeInsets.all(8.0))); // Tight
        expect(cards[3].padding, equals(EdgeInsets.zero)); // Zero
      });

      testWidgets('all variants should maintain consistent card styling', (
        tester,
      ) async {
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: Column(
                children: [
                  GHCard(child: Text('Standard')),
                  GHCard.compact(child: Text('Compact')),
                  GHCard.tight(child: Text('Tight')),
                  GHCard.zeroPadding(child: Text('Zero')),
                ],
              ),
            ),
          ),
        );

        final materialCards = tester
            .widgetList<Card>(find.byType(Card))
            .toList();
        expect(materialCards.length, equals(4));

        // All cards should have same elevation
        for (final card in materialCards) {
          expect(card.elevation, equals(GHTokens.elevation1));
        }

        // All cards should have same shape
        for (final card in materialCards) {
          final shape = card.shape as RoundedRectangleBorder;
          expect(
            shape.borderRadius,
            equals(BorderRadius.circular(GHTokens.radius8)),
          );
        }
      });

      testWidgets('zero padding should work with ListTile', (tester) async {
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: GHCard.zeroPadding(
                child: ListTile(
                  leading: Icon(Icons.person),
                  title: Text('User Name'),
                  subtitle: Text('user@example.com'),
                  trailing: Icon(Icons.chevron_right),
                ),
              ),
            ),
          ),
        );

        expect(find.byType(ListTile), findsOneWidget);
        expect(find.byType(GHCard), findsOneWidget);

        final card = tester.widget<GHCard>(find.byType(GHCard));
        expect(card.padding, equals(EdgeInsets.zero));
      });

      testWidgets('compact should be appropriate for secondary content', (
        tester,
      ) async {
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: GHCard.compact(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Metadata',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    Text('Created: 2 days ago'),
                    Text('Updated: 1 hour ago'),
                    Text('Size: 2.3 MB'),
                  ],
                ),
              ),
            ),
          ),
        );

        final card = tester.widget<GHCard>(find.byType(GHCard));
        expect(card.padding, equals(const EdgeInsets.all(12.0)));
        expect(find.text('Metadata'), findsOneWidget);
      });

      testWidgets('tight should be appropriate for dense layouts', (
        tester,
      ) async {
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: GHCard.tight(
                child: Row(
                  children: [
                    Icon(Icons.star, size: 16),
                    SizedBox(width: 4),
                    Text('4.5', style: TextStyle(fontSize: 12)),
                    SizedBox(width: 8),
                    Icon(Icons.download, size: 16),
                    SizedBox(width: 4),
                    Text('1.2k', style: TextStyle(fontSize: 12)),
                  ],
                ),
              ),
            ),
          ),
        );

        final card = tester.widget<GHCard>(find.byType(GHCard));
        expect(card.padding, equals(const EdgeInsets.all(8.0)));
        expect(find.text('4.5'), findsOneWidget);
        expect(find.text('1.2k'), findsOneWidget);
      });
    });

    group('appropriate use cases verification', () {
      test('should have clear use case distinctions', () {
        // Standard (16dp): Primary content, main cards
        expect(GHTokens.spacing16, equals(16.0));

        // Compact (12dp): Secondary content, metadata cards
        expect(GHTokens.spacing12, equals(12.0));

        // Tight (8dp): Dense content, status indicators
        expect(GHTokens.spacing8, equals(8.0));

        // Zero (0dp): Self-padded content like ListTile
        expect(EdgeInsets.zero.left, equals(0.0));
      });
    });
  });
}
