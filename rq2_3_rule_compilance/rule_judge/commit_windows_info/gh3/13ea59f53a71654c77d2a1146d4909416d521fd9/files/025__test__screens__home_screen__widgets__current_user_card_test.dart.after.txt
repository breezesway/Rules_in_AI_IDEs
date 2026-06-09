import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/screens/home_screen/widgets/current_user_card.dart';
import 'package:mocktail_image_network/mocktail_image_network.dart';

void main() {
  group('CurrentUserCard', () {
    testWidgets('should display user information when provided', (tester) async {
      await mockNetworkImages(() async {
        // Arrange
        const name = 'John Doe';
        const login = 'johndoe';
        const avatarUrl = 'https://example.com/avatar.jpg';

        // Act
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: CurrentUserCard(
                name: name,
                login: login,
                avatarUrl: avatarUrl,
              ),
            ),
          ),
        );

        // Assert
        expect(find.text(name), findsOneWidget);
        expect(find.text('@$login'), findsOneWidget);
        expect(find.byType(Card), findsOneWidget);
        expect(find.byType(CircleAvatar), findsOneWidget);
        expect(find.byIcon(Icons.arrow_forward_ios), findsOneWidget);
      });
    });

    testWidgets('should display default values when user info is null', (tester) async {
      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CurrentUserCard(
              name: null,
              login: null,
              avatarUrl: null,
            ),
          ),
        ),
      );

      // Assert
      expect(find.text('User'), findsOneWidget);
      expect(find.text('@username'), findsOneWidget);
      expect(find.byIcon(Icons.person), findsOneWidget);
      expect(find.byIcon(Icons.arrow_forward_ios), findsOneWidget);
    });

    testWidgets('should show person icon when avatarUrl is null', (tester) async {
      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CurrentUserCard(
              name: 'John Doe',
              login: 'johndoe',
              avatarUrl: null,
            ),
          ),
        ),
      );

      // Assert
      final circleAvatar = tester.widget<CircleAvatar>(find.byType(CircleAvatar));
      expect(circleAvatar.backgroundImage, isNull);
      expect(find.byIcon(Icons.person), findsOneWidget);
    });

    testWidgets('should set NetworkImage when avatarUrl is provided', (tester) async {
      await mockNetworkImages(() async {
        // Arrange
        const avatarUrl = 'https://example.com/avatar.jpg';

        // Act
        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: CurrentUserCard(
                name: 'John Doe',
                login: 'johndoe',
                avatarUrl: avatarUrl,
              ),
            ),
          ),
        );

        // Assert
        final circleAvatar = tester.widget<CircleAvatar>(find.byType(CircleAvatar));
        expect(circleAvatar.backgroundImage, isA<NetworkImage>());
        expect((circleAvatar.backgroundImage as NetworkImage).url, avatarUrl);
        expect(circleAvatar.child, isNull);
      });
    });

    testWidgets('should be contained in a Card widget', (tester) async {
      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CurrentUserCard(
              name: 'John Doe',
              login: 'johndoe',
            ),
          ),
        ),
      );

      // Assert
      expect(find.byType(Card), findsOneWidget);
      expect(find.byType(ListTile), findsOneWidget);
      
      // ListTile should be inside Card
      final card = tester.widget<Card>(find.byType(Card));
      expect(card.child, isA<ListTile>());
    });

    testWidgets('should have no onTap functionality (placeholder)', (tester) async {
      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CurrentUserCard(
              name: 'John Doe',
              login: 'johndoe',
            ),
          ),
        ),
      );

      // Assert
      final listTile = tester.widget<ListTile>(find.byType(ListTile));
      expect(listTile.onTap, isNull);
    });

    testWidgets('should handle mixed null and non-null values', (tester) async {
      // Test case 1: name is null, login is provided
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CurrentUserCard(
              name: null,
              login: 'johndoe',
              avatarUrl: null,
            ),
          ),
        ),
      );

      expect(find.text('User'), findsOneWidget);
      expect(find.text('@johndoe'), findsOneWidget);
      
      // Clear and test case 2: name is provided, login is null
      await tester.pumpWidget(Container());
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CurrentUserCard(
              name: 'John Doe',
              login: null,
              avatarUrl: null,
            ),
          ),
        ),
      );

      expect(find.text('John Doe'), findsOneWidget);
      expect(find.text('@username'), findsOneWidget);
    });
  });
}