import 'package:ferry/ferry.dart';
import 'package:gql_http_link/gql_http_link.dart';
import 'package:injectable/injectable.dart';
import 'token_storage.dart';

/// Service for configuring and providing Ferry GraphQL client with GitHub's GraphQL endpoint
/// Handles automatic authentication token injection and error handling for GraphQL operations
@injectable
class FerryClientService {
  final ITokenStorage _tokenStorage;
  Client? _client;

  FerryClientService(this._tokenStorage);

  /// Get or create Ferry client instance with authentication integration
  Future<Client> getClient() async {
    if (_client != null) return _client!;

    _client = await _createClient();
    return _client!;
  }

  /// Create a new Ferry client with GitHub GraphQL endpoint and authentication link
  Future<Client> _createClient() async {
    final token = await _tokenStorage.getToken();

    // Configure HTTP link with GitHub GraphQL endpoint and authentication headers
    final httpLink = HttpLink(
      'https://api.github.com/graphql',
      defaultHeaders: {
        'User-Agent': 'gh3-flutter-app',
        'Accept': 'application/vnd.github.v4+json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
    );

    final cache = Cache();

    return Client(link: httpLink, cache: cache);
  }

  /// Update authentication token and recreate client for automatic header updates
  /// Handles token refresh scenarios by forcing client recreation
  Future<void> updateAuthToken(String? token) async {
    _client = null; // Force recreation with new token
    _client = await _createClient();
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
