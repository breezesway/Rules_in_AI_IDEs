import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:gh3/src/services/ferry_client_service.dart';
import 'package:gh3/src/services/auth_service.dart';

import 'ferry_client_service_test.mocks.dart';

@GenerateMocks([AuthService])
void main() {
  group('FerryClientService', () {
    late MockAuthService mockAuthService;
    late FerryClientService ferryClientService;

    setUp(() {
      mockAuthService = MockAuthService();
      ferryClientService = FerryClientService(mockAuthService);
    });

    tearDown(() {
      ferryClientService.dispose();
    });

    test('should create Ferry client with authentication', () {
      when(mockAuthService.accessToken).thenReturn('test-token');
      
      final client = ferryClientService.getClient();
      expect(client, isNotNull);
    });

    test('should create Ferry client without token', () {
      when(mockAuthService.accessToken).thenReturn(null);
      
      final client = ferryClientService.getClient();
      expect(client, isNotNull);
    });

    test('should reuse existing client', () {
      final client1 = ferryClientService.getClient();
      final client2 = ferryClientService.getClient();
      expect(client1, same(client2));
    });

    test('should clear cache', () {
      expect(() => ferryClientService.clearCache(), returnsNormally);
    });

    test('should dispose resources', () {
      expect(() => ferryClientService.dispose(), returnsNormally);
    });
  });
}
