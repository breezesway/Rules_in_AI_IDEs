/// Route definitions for the UI system example screens
class ExampleRoutes {
  static const String home = '/';
  static const String userProfile = '/user/:username';
  static const String repository = '/repo/:owner/:name';
  static const String repositoryTree = '/repo/:owner/:name/tree';
  static const String repositoryFile = '/repo/:owner/:name/file';
  static const String issues = '/repo/:owner/:name/issues';
  static const String issueDetail = '/repo/:owner/:name/issue/:number';
  static const String pulls = '/repo/:owner/:name/pulls';
  static const String pullDetail = '/repo/:owner/:name/pull/:number';
  static const String search = '/search';
  static const String trending = '/trending';
  static const String starred = '/starred';
  static const String userRepositories = '/user/:username/repositories';
  static const String userStarred = '/user/:username/starred';
  static const String userOrganizations = '/user/:username/organizations';

  /// Helper methods for navigation
  static String userProfilePath(String username) => '/user/$username';
  static String repositoryPath(String owner, String name) =>
      '/repo/$owner/$name';
  static String repositoryTreePath(String owner, String name, {String? path}) =>
      '/repo/$owner/$name/tree${path != null ? '?path=$path' : ''}';
  static String repositoryFilePath(
    String owner,
    String name, {
    String? filePath,
  }) => '/repo/$owner/$name/file${filePath != null ? '?path=$filePath' : ''}';
  static String issuesPath(String owner, String name) =>
      '/repo/$owner/$name/issues';
  static String issueDetailPath(String owner, String name, int number) =>
      '/repo/$owner/$name/issue/$number';
  static String pullsPath(String owner, String name) =>
      '/repo/$owner/$name/pulls';
  static String pullDetailPath(String owner, String name, int number) =>
      '/repo/$owner/$name/pull/$number';
  static String userRepositoriesPath(String username) =>
      '/user/$username/repositories';
  static String userStarredPath(String username) => '/user/$username/starred';
  static String userOrganizationsPath(String username) =>
      '/user/$username/organizations';
}
