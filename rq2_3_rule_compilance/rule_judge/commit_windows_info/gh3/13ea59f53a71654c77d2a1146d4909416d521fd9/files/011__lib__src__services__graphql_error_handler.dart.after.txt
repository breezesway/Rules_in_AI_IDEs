import 'package:ferry/ferry.dart';
import 'package:gql_http_link/gql_http_link.dart';
import 'graphql_errors.dart';

class GraphQLErrorHandler {
  static GraphQLError processResponse(OperationResponse response) {
    // Network errors (HTTP status codes)
    if (response.linkException != null) {
      final linkError = response.linkException!;
      if (linkError is HttpLinkServerException) {
        if (linkError.response.statusCode == 401) {
          return const GraphQLAuthenticationError(
            'Authentication failed - please login again',
          );
        }
        if (linkError.response.statusCode == 403) {
          // Check for rate limiting headers
          final resetHeader = linkError.response.headers['x-ratelimit-reset'];
          if (resetHeader != null) {
            final resetTime = DateTime.fromMillisecondsSinceEpoch(
              int.parse(resetHeader) * 1000,
            );
            final remaining =
                linkError.response.headers['x-ratelimit-remaining'];
            return GraphQLRateLimitError(
              'Rate limit exceeded. Try again later.',
              resetTime: resetTime,
              remainingPoints: remaining != null
                  ? int.tryParse(remaining)
                  : null,
            );
          }
          return const GraphQLAuthenticationError(
            'Access forbidden - insufficient permissions',
          );
        }
        return GraphQLNetworkError(
          'Network error: ${linkError.response.statusCode}',
          statusCode: linkError.response.statusCode,
        );
      }
      // Network connectivity issues
      return const GraphQLOfflineError(
        'No internet connection - please check your network',
      );
    }

    // GraphQL errors - treat as failures (no partial data)
    final graphqlErrors = response.graphqlErrors;
    if (graphqlErrors != null && graphqlErrors.isNotEmpty) {
      final firstError = graphqlErrors.first;
      final fieldErrors = <String>[];

      // Extract field errors from extensions if available
      if (firstError.extensions != null &&
          firstError.extensions!['field_errors'] != null) {
        final errors = firstError.extensions!['field_errors'];
        if (errors is List) {
          fieldErrors.addAll(errors.cast<String>());
        }
      }

      return GraphQLValidationError(
        firstError.message,
        fieldErrors: fieldErrors,
      );
    }

    return const GraphQLValidationError('Unknown error occurred');
  }

  static String getErrorMessage(dynamic error) {
    if (error is GraphQLError) {
      return error.message;
    }
    if (error is OperationResponse) {
      final processedError = processResponse(error);
      return processedError.message;
    }
    if (error is List && error.isNotEmpty) {
      // Handle lists of GraphQL errors
      return error.map((e) => e.toString()).join(', ');
    }
    return error?.toString() ?? 'Unknown error occurred';
  }
}
