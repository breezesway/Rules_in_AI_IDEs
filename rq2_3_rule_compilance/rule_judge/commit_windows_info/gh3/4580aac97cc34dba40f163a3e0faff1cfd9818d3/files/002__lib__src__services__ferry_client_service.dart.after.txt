import 'package:ferry/ferry.dart';
import 'package:gql_http_link/gql_http_link.dart';
import 'package:gql_exec/gql_exec.dart';
import 'package:injectable/injectable.dart';
import 'auth_service.dart';

/// Service for configuring and providing Ferry GraphQL client with GitHub's GraphQL endpoint
/// Handles automatic authentication token injection via private AuthLink implementation
@injectable
class FerryClientService {
  final AuthService _authService;
  Client? _client;

  FerryClientService(this._authService);

  /// Get or create Ferry client instance with authentication integration
  Client getClient() {
    _client ??= _createClient();
    return _client!;
  }

  /// Create a new Ferry client with GitHub GraphQL endpoint and dynamic authentication
  Client _createClient() {
    final authLink = _AuthLink(_authService);
    final httpLink = HttpLink("https://api.github.com/graphql");
    
    final link = Link.from([authLink, httpLink]);
    return Client(link: link);
  }


  /// Clear cache (useful for logout scenarios)
  void clearCache() {
    _client?.cache.clear();
  }

  /// Dispose resources and clean up subscriptions
  void dispose() {
    _client?.dispose();
    _client = null;
  }
}

/// Private authentication link implementation for FerryClientService
/// Dynamically injects GitHub access tokens into GraphQL requests
class _AuthLink extends Link {
  final AuthService _authService;

  _AuthLink(this._authService);

  @override
  Stream<Response> request(Request request, [NextLink? forward]) async* {
    final token = _authService.accessToken;
    
    final updatedRequest = request.updateContextEntry<HttpLinkHeaders>(
      (headers) => HttpLinkHeaders(
        headers: {
          ...?headers?.headers,
          'User-Agent': 'gh3-flutter-app',
          'Accept': 'application/vnd.github.v4+json',
          if (token != null) 'Authorization': 'Bearer $token',
        },
      ),
    );

    yield* forward!(updatedRequest);
  }
}
