abstract class GraphQLError {
  final String message;
  final String? code;

  const GraphQLError(this.message, {this.code});

  @override
  String toString() =>
      'GraphQLError: $message${code != null ? ' (Code: $code)' : ''}';
}

class GraphQLNetworkError extends GraphQLError {
  final int? statusCode;

  const GraphQLNetworkError(super.message, {this.statusCode})
    : super(code: 'NETWORK_ERROR');
}

class GraphQLAuthenticationError extends GraphQLError {
  const GraphQLAuthenticationError(super.message)
    : super(code: 'AUTHENTICATION_ERROR');
}

class GraphQLRateLimitError extends GraphQLError {
  final DateTime? resetTime;
  final int? remainingPoints;

  const GraphQLRateLimitError(
    super.message, {
    this.resetTime,
    this.remainingPoints,
  }) : super(code: 'RATE_LIMIT_ERROR');
}

class GraphQLValidationError extends GraphQLError {
  final List<String> fieldErrors;

  const GraphQLValidationError(super.message, {this.fieldErrors = const []})
    : super(code: 'VALIDATION_ERROR');
}

class GraphQLOfflineError extends GraphQLError {
  const GraphQLOfflineError(super.message) : super(code: 'OFFLINE_ERROR');
}
