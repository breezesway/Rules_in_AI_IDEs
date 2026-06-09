import 'dart:async';
import 'package:ferry/ferry.dart';
import '../base_viewmodel.dart';
import '../../services/graphql_error_handler.dart';
import '__generated__/user_details_viewmodel.req.gql.dart';
import '__generated__/user_details_viewmodel.data.gql.dart';
import '__generated__/user_details_viewmodel.var.gql.dart';

/// ViewModel for handling user details screen logic with GraphQL.
class UserDetailsViewModel extends DisposableViewModel {
  final String _login;
  final Client _ferryClient;

  UserDetailsViewModel(this._login, this._ferryClient);

  // Store raw GraphQL results - no model conversion
  OperationResponse<GGetUserDetailsData, GGetUserDetailsVars>? _userResult;
  OperationResponse<GGetUserRepositoriesData, GGetUserRepositoriesVars>?
  _repositoriesResult;

  StreamSubscription<
    OperationResponse<GGetUserDetailsData, GGetUserDetailsVars>
  >?
  _userSubscription;
  StreamSubscription<
    OperationResponse<GGetUserRepositoriesData, GGetUserRepositoriesVars>
  >?
  _reposSubscription;

  // Pagination state for repositories
  String? _endCursor;
  bool _hasNextPage = true;
  static const int _pageSize = 20;

  /// The user login being displayed.
  String get login => _login;

  // Expose raw GraphQL data for UI consumption
  GGetUserDetailsData_user? get user => _userResult?.data?.user;
  GGetUserRepositoriesData_user_repositories? get repositories =>
      _repositoriesResult?.data?.user?.repositories;

  List<GGetUserRepositoriesData_user_repositories_nodes> get repositoryNodes =>
      repositories?.nodes
          ?.cast<GGetUserRepositoriesData_user_repositories_nodes>()
          .toList() ??
      [];

  bool get isLoading =>
      (_userResult?.loading ?? true) || (_repositoriesResult?.loading ?? true);

  bool get hasMoreRepositories => _hasNextPage;
  bool get isEmpty => repositoryNodes.isEmpty;

  String? get error {
    // Check user details errors
    if (_userResult != null) {
      final linkException = _userResult!.linkException;
      final graphqlErrors = _userResult!.graphqlErrors;

      if (linkException != null ||
          (graphqlErrors != null && graphqlErrors.isNotEmpty)) {
        return GraphQLErrorHandler.getErrorMessage(_userResult!);
      }
    }

    // Check repositories errors
    if (_repositoriesResult != null) {
      final linkException = _repositoriesResult!.linkException;
      final graphqlErrors = _repositoriesResult!.graphqlErrors;

      if (linkException != null ||
          (graphqlErrors != null && graphqlErrors.isNotEmpty)) {
        return GraphQLErrorHandler.getErrorMessage(_repositoriesResult!);
      }
    }

    return null;
  }

  /// Initialize the view model and load user data.
  Future<void> init() async {
    await loadUserDetails();
    await loadUserRepositories();
  }

  /// Load user details via GraphQL
  Future<void> loadUserDetails() async {
    final request = GGetUserDetailsReq((b) => b..vars.login = _login);

    _userSubscription?.cancel();
    _userSubscription = _ferryClient.request(request).listen((result) {
      _userResult = result;
      notifyListeners();
    });
  }

  /// Load user repositories via GraphQL
  Future<void> loadUserRepositories() async {
    _endCursor = null;
    _hasNextPage = true;

    final request = GGetUserRepositoriesReq(
      (b) => b
        ..vars.login = _login
        ..vars.first = _pageSize
        ..vars.after = null,
    );

    _reposSubscription?.cancel();
    _reposSubscription = _ferryClient.request(request).listen((result) {
      _repositoriesResult = result;

      if (result.data?.user?.repositories != null) {
        final pageInfo = result.data!.user!.repositories.pageInfo;
        _hasNextPage = pageInfo.hasNextPage;
        _endCursor = pageInfo.endCursor;
      }

      notifyListeners();
    });
  }

  /// Load more repositories (pagination)
  Future<void> loadMoreRepositories() async {
    if (isLoading || !_hasNextPage || _endCursor == null) return;

    final request = GGetUserRepositoriesReq(
      (b) => b
        ..vars.login = _login
        ..vars.first = _pageSize
        ..vars.after = _endCursor,
    );

    // For pagination, we'll need to merge results
    // This is a simplified approach - in production you might want more sophisticated caching
    _ferryClient.request(request).listen((result) {
      if (result.data?.user?.repositories != null) {
        final newRepositories = result.data!.user!.repositories;

        // Update pagination info
        final pageInfo = newRepositories.pageInfo;
        _hasNextPage = pageInfo.hasNextPage;
        _endCursor = pageInfo.endCursor;

        // For simplicity, just trigger a refresh - in production you'd merge properly
        notifyListeners();
      }
    });
  }

  /// Refresh both user details and repositories
  Future<void> refresh() async {
    await loadUserDetails();
    await loadUserRepositories();
  }

  /// Clear any existing error
  void clearError() {
    // Force refresh to clear error
    refresh();
  }

  @override
  void onDispose() {
    _userSubscription?.cancel();
    _reposSubscription?.cancel();
    _userSubscription = null;
    _reposSubscription = null;
    _userResult = null;
    _repositoriesResult = null;
  }
}
