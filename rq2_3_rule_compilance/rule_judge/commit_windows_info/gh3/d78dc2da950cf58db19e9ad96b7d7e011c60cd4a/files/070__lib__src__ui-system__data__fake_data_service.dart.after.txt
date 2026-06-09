import 'dart:math';
import '../widgets/gh_status_badge.dart';
import '../widgets/gh_file_tree_item.dart';

/// Centralized fake data service for the UI system.
///
/// This service provides realistic fake data for all GitHub widgets
/// including repositories, users, issues, and files. All data is
/// generated to match real GitHub usage patterns.
class FakeDataService {
  static final FakeDataService _instance = FakeDataService._internal();
  factory FakeDataService() => _instance;
  FakeDataService._internal();

  final Random _random = Random();

  /// Get a list of fake repositories
  List<FakeRepository> getRepositories({int count = 20}) {
    return _repositories.take(count).toList();
  }

  /// Get a list of fake users
  List<FakeUser> getUsers({int count = 20}) {
    return _users.take(count).toList();
  }

  /// Get a list of fake issues
  List<FakeIssue> getIssues({int count = 30}) {
    return _issues.take(count).toList();
  }

  /// Get comments for a specific issue
  List<FakeComment> getIssueComments(int issueNumber) {
    // Generate consistent comments based on issue number
    final random = Random(issueNumber);
    final commentCount = random.nextInt(10) + 1;

    return List.generate(commentCount, (index) {
      final authors = ['alice', 'bob', 'charlie', 'diana', 'eve'];
      final author = authors[random.nextInt(authors.length)];

      return FakeComment(
        id: index + 1,
        body: _generateCommentBody(random),
        authorLogin: author,
        authorAvatarUrl: 'https://github.com/$author.png',
        createdAt: DateTime.now().subtract(
          Duration(hours: random.nextInt(48), minutes: random.nextInt(60)),
        ),
        reactions: _generateReactions(random),
      );
    });
  }

  String _generateCommentBody(Random random) {
    final comments = [
      'This looks good to me! 👍',
      'I think we should also consider the edge case where the user input is empty.',
      'Could you add some unit tests for this functionality?',
      'The implementation looks solid, but we might want to optimize for performance.',
      'Great work! This fixes the issue I was experiencing.',
      'Can we make sure this is backwards compatible?',
      'I\'ve tested this locally and it works perfectly.',
      'We should update the documentation to reflect these changes.',
      'This might conflict with the changes in PR #123.',
      'Approved! Ready to merge once tests pass.',
      'I found a small bug in line 42 - the null check is missing.',
      'This feature request has been highly anticipated by our users.',
    ];
    return comments[random.nextInt(comments.length)];
  }

  List<FakeReaction> _generateReactions(Random random) {
    final reactions = ['👍', '👎', '😄', '🎉', '😕', '❤️', '🚀', '👀'];
    final reactionCount = random.nextInt(4);

    return List.generate(reactionCount, (index) {
      return FakeReaction(
        emoji: reactions[random.nextInt(reactions.length)],
        count: random.nextInt(5) + 1,
      );
    });
  }

  /// Get a list of fake files
  List<FakeFile> getFiles({int count = 20}) {
    return _files.take(count).toList();
  }

  /// Get repository files for a specific path
  List<FakeFile> getRepositoryFiles(String owner, String name, {String? path}) {
    // Generate consistent files based on repository and path
    final repoKey = '$owner/$name';
    final pathKey = path ?? '';
    final seed = repoKey.hashCode + pathKey.hashCode;
    final random = Random(seed);

    if (pathKey.isEmpty) {
      // Root directory
      return [
        FakeFile(
          name: 'lib',
          type: GHFileType.directory,
          lastCommitMessage: 'Add main library structure',
          author: 'flutter-dev',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(30)),
          ),
        ),
        FakeFile(
          name: 'test',
          type: GHFileType.directory,
          lastCommitMessage: 'Add comprehensive tests',
          author: 'test-author',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(15)),
          ),
        ),
        FakeFile(
          name: 'README.md',
          type: GHFileType.markdown,
          size: 1024 + random.nextInt(5000),
          lastCommitMessage: 'Update documentation',
          author: 'docs-team',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(7)),
          ),
        ),
        FakeFile(
          name: 'pubspec.yaml',
          type: GHFileType.config,
          size: 512 + random.nextInt(1000),
          lastCommitMessage: 'Update dependencies',
          author: 'maintainer',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(10)),
          ),
        ),
        FakeFile(
          name: 'analysis_options.yaml',
          type: GHFileType.config,
          size: 256 + random.nextInt(500),
          lastCommitMessage: 'Configure analysis options',
          author: 'flutter-dev',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(20)),
          ),
        ),
        FakeFile(
          name: 'CHANGELOG.md',
          type: GHFileType.markdown,
          size: 2048 + random.nextInt(3000),
          lastCommitMessage: 'Update changelog for v2.1.0',
          author: 'release-bot',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(5)),
          ),
        ),
      ];
    } else if (pathKey == 'lib') {
      // lib directory
      return [
        FakeFile(
          name: 'src',
          type: GHFileType.directory,
          lastCommitMessage: 'Organize source code',
          author: 'flutter-dev',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(25)),
          ),
        ),
        FakeFile(
          name: 'main.dart',
          type: GHFileType.code,
          size: 1024 + random.nextInt(2000),
          lastCommitMessage: 'Update main entry point',
          author: 'flutter-dev',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(12)),
          ),
        ),
        FakeFile(
          name: 'app.dart',
          type: GHFileType.code,
          size: 2048 + random.nextInt(3000),
          lastCommitMessage: 'Refactor app structure',
          author: 'architect',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(8)),
          ),
        ),
      ];
    } else if (pathKey == 'lib/src') {
      // lib/src directory
      return [
        FakeFile(
          name: 'ui',
          type: GHFileType.directory,
          lastCommitMessage: 'Add UI components',
          author: 'ui-team',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(20)),
          ),
        ),
        FakeFile(
          name: 'data',
          type: GHFileType.directory,
          lastCommitMessage: 'Add data models',
          author: 'backend-dev',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(15)),
          ),
        ),
        FakeFile(
          name: 'utils',
          type: GHFileType.directory,
          lastCommitMessage: 'Add utility functions',
          author: 'utils-team',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(18)),
          ),
        ),
        FakeFile(
          name: 'constants.dart',
          type: GHFileType.code,
          size: 512 + random.nextInt(1000),
          lastCommitMessage: 'Update app constants',
          author: 'config-team',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(10)),
          ),
        ),
      ];
    } else if (pathKey == 'test') {
      // test directory
      return [
        FakeFile(
          name: 'unit',
          type: GHFileType.directory,
          lastCommitMessage: 'Add unit tests',
          author: 'test-author',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(12)),
          ),
        ),
        FakeFile(
          name: 'widget',
          type: GHFileType.directory,
          lastCommitMessage: 'Add widget tests',
          author: 'ui-tester',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(8)),
          ),
        ),
        FakeFile(
          name: 'integration',
          type: GHFileType.directory,
          lastCommitMessage: 'Add integration tests',
          author: 'qa-team',
          lastModified: DateTime.now().subtract(
            Duration(days: random.nextInt(15)),
          ),
        ),
      ];
    } else {
      // Default empty or nested directories
      return [];
    }
  }

  /// Search repositories by name or description
  List<FakeRepository> searchRepositories(String query) {
    if (query.isEmpty) return getRepositories();

    final lowerQuery = query.toLowerCase();
    return _repositories
        .where(
          (repo) =>
              repo.name.toLowerCase().contains(lowerQuery) ||
              repo.description.toLowerCase().contains(lowerQuery) ||
              repo.owner.toLowerCase().contains(lowerQuery) ||
              repo.topics.any(
                (topic) => topic.toLowerCase().contains(lowerQuery),
              ),
        )
        .toList();
  }

  /// Search users by name or username
  List<FakeUser> searchUsers(String query) {
    if (query.isEmpty) return getUsers();

    final lowerQuery = query.toLowerCase();
    return _users
        .where(
          (user) =>
              user.login.toLowerCase().contains(lowerQuery) ||
              (user.name?.toLowerCase().contains(lowerQuery) ?? false) ||
              (user.bio?.toLowerCase().contains(lowerQuery) ?? false) ||
              (user.company?.toLowerCase().contains(lowerQuery) ?? false) ||
              (user.location?.toLowerCase().contains(lowerQuery) ?? false),
        )
        .toList();
  }

  /// Search issues by title
  List<FakeIssue> searchIssues(String query) {
    if (query.isEmpty) return getIssues();

    final lowerQuery = query.toLowerCase();
    return _issues
        .where(
          (issue) =>
              issue.title.toLowerCase().contains(lowerQuery) ||
              issue.body.toLowerCase().contains(lowerQuery) ||
              issue.labels.any(
                (label) => label.toLowerCase().contains(lowerQuery),
              ),
        )
        .toList();
  }

  /// Advanced search across all content types
  Map<String, List<dynamic>> searchAll(String query) {
    if (query.isEmpty) {
      return {
        'repositories': <FakeRepository>[],
        'users': <FakeUser>[],
        'issues': <FakeIssue>[],
      };
    }

    return {
      'repositories': searchRepositories(query),
      'users': searchUsers(query),
      'issues': searchIssues(query),
    };
  }

  /// Filter repositories by language
  List<FakeRepository> filterRepositoriesByLanguage(String language) {
    return _repositories.where((repo) => repo.language == language).toList();
  }

  /// Filter repositories by multiple criteria
  List<FakeRepository> filterRepositories({
    String? language,
    bool? isPrivate,
    List<String>? topics,
    int? minStars,
    int? maxStars,
    DateTime? updatedAfter,
    DateTime? updatedBefore,
  }) {
    return _repositories.where((repo) {
      if (language != null && repo.language != language) return false;
      if (isPrivate != null && repo.isPrivate != isPrivate) return false;
      if (topics != null &&
          !topics.any((topic) => repo.topics.contains(topic))) {
        return false;
      }
      if (minStars != null && repo.starCount < minStars) return false;
      if (maxStars != null && repo.starCount > maxStars) return false;
      if (updatedAfter != null && repo.lastUpdated.isBefore(updatedAfter)) {
        return false;
      }
      if (updatedBefore != null && repo.lastUpdated.isAfter(updatedBefore)) {
        return false;
      }
      return true;
    }).toList();
  }

  /// Filter issues by status
  List<FakeIssue> filterIssuesByStatus(GHStatusType status) {
    return _issues.where((issue) => issue.status == status).toList();
  }

  /// Filter issues by multiple criteria
  List<FakeIssue> filterIssues({
    GHStatusType? status,
    List<String>? labels,
    String? assignee,
    String? author,
    bool? isPullRequest,
    DateTime? createdAfter,
    DateTime? createdBefore,
  }) {
    return _issues.where((issue) {
      if (status != null && issue.status != status) return false;
      if (labels != null &&
          !labels.any((label) => issue.labels.contains(label))) {
        return false;
      }
      if (assignee != null && issue.assigneeLogin != assignee) return false;
      if (author != null && issue.authorLogin != author) return false;
      if (isPullRequest != null && issue.isPullRequest != isPullRequest) {
        return false;
      }
      if (createdAfter != null && issue.createdAt.isBefore(createdAfter)) {
        return false;
      }
      if (createdBefore != null && issue.createdAt.isAfter(createdBefore)) {
        return false;
      }
      return true;
    }).toList();
  }

  /// Filter users by criteria
  List<FakeUser> filterUsers({
    String? location,
    String? company,
    int? minRepos,
    int? maxRepos,
    int? minFollowers,
    int? maxFollowers,
  }) {
    return _users.where((user) {
      if (location != null &&
          user.location?.toLowerCase() != location.toLowerCase()) {
        return false;
      }
      if (company != null &&
          user.company?.toLowerCase() != company.toLowerCase()) {
        return false;
      }
      if (minRepos != null && user.repositoryCount < minRepos) return false;
      if (maxRepos != null && user.repositoryCount > maxRepos) return false;
      if (minFollowers != null && user.followerCount < minFollowers) {
        return false;
      }
      if (maxFollowers != null && user.followerCount > maxFollowers) {
        return false;
      }
      return true;
    }).toList();
  }

  /// Get available filter options
  Map<String, List<String>> getFilterOptions() {
    final languages = _repositories.map((r) => r.language).toSet().toList();
    final topics = _repositories.expand((r) => r.topics).toSet().toList();
    final labels = _issues.expand((i) => i.labels).toSet().toList();
    final locations = _users
        .map((u) => u.location)
        .where((l) => l != null)
        .cast<String>()
        .toSet()
        .toList();
    final companies = _users
        .map((u) => u.company)
        .where((c) => c != null)
        .cast<String>()
        .toSet()
        .toList();

    return {
      'languages': languages,
      'topics': topics,
      'labels': labels,
      'locations': locations,
      'companies': companies,
    };
  }

  /// Sort repositories by different criteria
  List<FakeRepository> sortRepositories(
    List<FakeRepository> repos,
    String sortBy, {
    bool ascending = false,
  }) {
    final sorted = List<FakeRepository>.from(repos);

    switch (sortBy) {
      case 'name':
        sorted.sort(
          (a, b) =>
              ascending ? a.name.compareTo(b.name) : b.name.compareTo(a.name),
        );
        break;
      case 'stars':
        sorted.sort(
          (a, b) => ascending
              ? a.starCount.compareTo(b.starCount)
              : b.starCount.compareTo(a.starCount),
        );
        break;
      case 'forks':
        sorted.sort(
          (a, b) => ascending
              ? a.forkCount.compareTo(b.forkCount)
              : b.forkCount.compareTo(a.forkCount),
        );
        break;
      case 'updated':
        sorted.sort(
          (a, b) => ascending
              ? a.lastUpdated.compareTo(b.lastUpdated)
              : b.lastUpdated.compareTo(a.lastUpdated),
        );
        break;
      case 'created':
        sorted.sort((a, b) {
          final aCreated = a.createdAt ?? DateTime(2000);
          final bCreated = b.createdAt ?? DateTime(2000);
          return ascending
              ? aCreated.compareTo(bCreated)
              : bCreated.compareTo(aCreated);
        });
        break;
    }

    return sorted;
  }

  /// Sort issues by different criteria
  List<FakeIssue> sortIssues(
    List<FakeIssue> issues,
    String sortBy, {
    bool ascending = false,
  }) {
    final sorted = List<FakeIssue>.from(issues);

    switch (sortBy) {
      case 'created':
        sorted.sort(
          (a, b) => ascending
              ? a.createdAt.compareTo(b.createdAt)
              : b.createdAt.compareTo(a.createdAt),
        );
        break;
      case 'updated':
        sorted.sort((a, b) {
          final aUpdated = a.closedAt ?? a.createdAt;
          final bUpdated = b.closedAt ?? b.createdAt;
          return ascending
              ? aUpdated.compareTo(bUpdated)
              : bUpdated.compareTo(aUpdated);
        });
        break;
      case 'comments':
        sorted.sort(
          (a, b) => ascending
              ? a.commentCount.compareTo(b.commentCount)
              : b.commentCount.compareTo(a.commentCount),
        );
        break;
      case 'title':
        sorted.sort(
          (a, b) => ascending
              ? a.title.compareTo(b.title)
              : b.title.compareTo(a.title),
        );
        break;
    }

    return sorted;
  }

  /// Get random repository
  FakeRepository getRandomRepository() {
    return _repositories[_random.nextInt(_repositories.length)];
  }

  /// Get random user
  FakeUser getRandomUser() {
    return _users[_random.nextInt(_users.length)];
  }

  /// Get random issue
  FakeIssue getRandomIssue() {
    return _issues[_random.nextInt(_issues.length)];
  }

  /// Get activity feed data
  List<FakeActivity> getActivityFeed({int count = 20}) {
    return _generateActivityFeed(count);
  }

  /// Get user's starred repositories
  List<FakeRepository> getUserStarredRepos(String username, {int count = 20}) {
    // Simulate user-specific starred repos
    return _repositories.take(count).toList();
  }

  /// Get user's organizations
  List<FakeOrganization> getUserOrganizations(String username) {
    final user = _users.firstWhere(
      (u) => u.login == username,
      orElse: () => _users.first,
    );
    return user.organizations;
  }

  /// Get repository issues
  List<FakeIssue> getRepositoryIssues(
    String owner,
    String name, {
    int count = 30,
  }) {
    // Simulate repository-specific issues
    return _issues.take(count).toList();
  }

  /// Get repository contributors
  List<FakeContributor> getRepositoryContributors(
    String owner,
    String name, {
    int count = 10,
  }) {
    return _generateContributors(count);
  }

  /// Get repository releases
  List<FakeRelease> getRepositoryReleases(
    String owner,
    String name, {
    int count = 5,
  }) {
    return _generateReleases(count);
  }

  /// Generate activity feed
  List<FakeActivity> _generateActivityFeed(int count) {
    final activities = <FakeActivity>[];
    final activityTypes = [
      'starred',
      'forked',
      'created',
      'pushed',
      'opened_issue',
      'opened_pr',
    ];

    for (int i = 0; i < count; i++) {
      final user = getRandomUser();
      final repo = getRandomRepository();
      final type = activityTypes[_random.nextInt(activityTypes.length)];

      activities.add(
        FakeActivity(
          type: type,
          title: _getActivityTitle(type, user.login, repo),
          description: _getActivityDescription(type),
          actorLogin: user.login,
          actorAvatarUrl: user.avatarUrl,
          createdAt: DateTime.now().subtract(Duration(hours: i * 2)),
          repositoryName: repo.name,
          repositoryOwner: repo.owner,
        ),
      );
    }

    return activities;
  }

  /// Generate contributors
  List<FakeContributor> _generateContributors(int count) {
    final contributors = <FakeContributor>[];
    final users = _users.take(count).toList();

    for (int i = 0; i < users.length; i++) {
      contributors.add(
        FakeContributor(
          login: users[i].login,
          avatarUrl: users[i].avatarUrl,
          contributions: _random.nextInt(500) + 1,
        ),
      );
    }

    return contributors
      ..sort((a, b) => b.contributions.compareTo(a.contributions));
  }

  /// Generate releases
  List<FakeRelease> _generateReleases(int count) {
    final releases = <FakeRelease>[];

    for (int i = 0; i < count; i++) {
      final version = 'v${2 - (i * 0.1)}.$i.0';
      releases.add(
        FakeRelease(
          tagName: version,
          name: version,
          body:
              'Release notes for $version\n\n- Bug fixes and improvements\n- New features added',
          authorLogin: getRandomUser().login,
          publishedAt: DateTime.now().subtract(Duration(days: i * 30)),
          isPrerelease: i == 0 && _random.nextBool(),
        ),
      );
    }

    return releases;
  }

  String _getActivityTitle(String type, String username, FakeRepository repo) {
    switch (type) {
      case 'starred':
        return '$username starred ${repo.owner}/${repo.name}';
      case 'forked':
        return '$username forked ${repo.owner}/${repo.name}';
      case 'created':
        return '$username created ${repo.owner}/${repo.name}';
      case 'pushed':
        return '$username pushed to ${repo.owner}/${repo.name}';
      case 'opened_issue':
        return '$username opened an issue in ${repo.owner}/${repo.name}';
      case 'opened_pr':
        return '$username opened a pull request in ${repo.owner}/${repo.name}';
      default:
        return '$username performed an action on ${repo.owner}/${repo.name}';
    }
  }

  String _getActivityDescription(String type) {
    switch (type) {
      case 'starred':
        return 'Added this repository to their stars';
      case 'forked':
        return 'Created a fork of this repository';
      case 'created':
        return 'Created a new repository';
      case 'pushed':
        return 'Pushed new commits';
      case 'opened_issue':
        return 'Opened a new issue';
      case 'opened_pr':
        return 'Opened a new pull request';
      default:
        return 'Performed an action';
    }
  }

  // Static data collections
  static final List<FakeRepository> _repositories = [
    FakeRepository(
      owner: 'facebook',
      name: 'react',
      description: 'The library for web and native user interfaces',
      language: 'JavaScript',
      starCount: 218000,
      forkCount: 45200,
      watcherCount: 6800,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 2)),
      createdAt: DateTime(2013, 5, 24),
      isPrivate: false,
      topics: ['javascript', 'react', 'frontend', 'ui'],
      license: 'MIT',
      homepage: 'https://reactjs.org',
    ),
    FakeRepository(
      owner: 'flutter',
      name: 'flutter',
      description:
          'Flutter makes it easy and fast to build beautiful apps for mobile and beyond',
      language: 'Dart',
      starCount: 158000,
      forkCount: 25800,
      watcherCount: 3200,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 4)),
      createdAt: DateTime(2015, 3, 6),
      isPrivate: false,
      topics: ['dart', 'flutter', 'mobile', 'cross-platform'],
      license: 'BSD-3-Clause',
      homepage: 'https://flutter.dev',
    ),
    FakeRepository(
      owner: 'microsoft',
      name: 'vscode',
      description: 'Visual Studio Code',
      language: 'TypeScript',
      starCount: 152000,
      forkCount: 26900,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 1)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'kubernetes',
      name: 'kubernetes',
      description: 'Production-Grade Container Scheduling and Management',
      language: 'Go',
      starCount: 104000,
      forkCount: 38200,
      lastUpdated: DateTime.now().subtract(const Duration(minutes: 30)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'vercel',
      name: 'next.js',
      description: 'The React Framework',
      language: 'JavaScript',
      starCount: 115000,
      forkCount: 25100,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 3)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'nodejs',
      name: 'node',
      description: 'Node.js JavaScript runtime',
      language: 'JavaScript',
      starCount: 98500,
      forkCount: 26800,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 6)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'vuejs',
      name: 'vue',
      description: 'The Progressive JavaScript Framework',
      language: 'TypeScript',
      starCount: 205000,
      forkCount: 33600,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 8)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'angular',
      name: 'angular',
      description: 'The modern web developer\'s platform',
      language: 'TypeScript',
      starCount: 92000,
      forkCount: 24300,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 12)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'tensorflow',
      name: 'tensorflow',
      description: 'An Open Source Machine Learning Framework for Everyone',
      language: 'C++',
      starCount: 180000,
      forkCount: 88200,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 5)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'pytorch',
      name: 'pytorch',
      description: 'Tensors and Dynamic neural networks in Python',
      language: 'Python',
      starCount: 75000,
      forkCount: 20400,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 3)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'rust-lang',
      name: 'rust',
      description:
          'Empowering everyone to build reliable and efficient software',
      language: 'Rust',
      starCount: 89000,
      forkCount: 11500,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 7)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'golang',
      name: 'go',
      description: 'The Go programming language',
      language: 'Go',
      starCount: 118000,
      forkCount: 17200,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 9)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'apple',
      name: 'swift',
      description: 'The Swift Programming Language',
      language: 'C++',
      starCount: 65000,
      forkCount: 10400,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 11)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'JetBrains',
      name: 'kotlin',
      description: 'The Kotlin Programming Language',
      language: 'Kotlin',
      starCount: 47000,
      forkCount: 5800,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 14)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'rails',
      name: 'rails',
      description: 'Ruby on Rails',
      language: 'Ruby',
      starCount: 54000,
      forkCount: 21200,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 16)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'laravel',
      name: 'laravel',
      description: 'A PHP framework for web artisans',
      language: 'PHP',
      starCount: 76000,
      forkCount: 24600,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 18)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'django',
      name: 'django',
      description: 'The Web framework for perfectionists with deadlines',
      language: 'Python',
      starCount: 75000,
      forkCount: 30800,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 20)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'spring-projects',
      name: 'spring-boot',
      description: 'Spring Boot',
      language: 'Java',
      starCount: 71000,
      forkCount: 39800,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 22)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'dotnet',
      name: 'core',
      description:
          '.NET is a cross-platform runtime for cloud, mobile, desktop, and IoT apps',
      language: 'C#',
      starCount: 19000,
      forkCount: 4900,
      lastUpdated: DateTime.now().subtract(const Duration(days: 1)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'elastic',
      name: 'elasticsearch',
      description: 'Free and Open, Distributed, RESTful Search Engine',
      language: 'Java',
      starCount: 67000,
      forkCount: 24100,
      lastUpdated: DateTime.now().subtract(const Duration(days: 2)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'redis',
      name: 'redis',
      description: 'Redis is an in-memory database that persists on disk',
      language: 'C',
      starCount: 63000,
      forkCount: 23200,
      lastUpdated: DateTime.now().subtract(const Duration(days: 3)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'mongodb',
      name: 'mongo',
      description: 'The MongoDB Database',
      language: 'C++',
      starCount: 25000,
      forkCount: 5600,
      lastUpdated: DateTime.now().subtract(const Duration(days: 4)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'postgres',
      name: 'postgres',
      description: 'Mirror of the official PostgreSQL GIT repository',
      language: 'C',
      starCount: 14000,
      forkCount: 4200,
      lastUpdated: DateTime.now().subtract(const Duration(days: 5)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'docker',
      name: 'docker-ce',
      description: 'Docker CE',
      language: 'Go',
      starCount: 6000,
      forkCount: 1100,
      lastUpdated: DateTime.now().subtract(const Duration(days: 6)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'hashicorp',
      name: 'terraform',
      description:
          'Terraform enables you to safely and predictably create, change, and improve infrastructure',
      language: 'Go',
      starCount: 40000,
      forkCount: 9200,
      lastUpdated: DateTime.now().subtract(const Duration(days: 7)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'ansible',
      name: 'ansible',
      description: 'Ansible is a radically simple IT automation platform',
      language: 'Python',
      starCount: 59000,
      forkCount: 23800,
      lastUpdated: DateTime.now().subtract(const Duration(days: 8)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'grafana',
      name: 'grafana',
      description:
          'The open and composable observability and data visualization platform',
      language: 'TypeScript',
      starCount: 58000,
      forkCount: 11600,
      lastUpdated: DateTime.now().subtract(const Duration(days: 9)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'prometheus',
      name: 'prometheus',
      description: 'The Prometheus monitoring system and time series database',
      language: 'Go',
      starCount: 52000,
      forkCount: 8900,
      lastUpdated: DateTime.now().subtract(const Duration(days: 10)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'apache',
      name: 'kafka',
      description: 'Mirror of Apache Kafka',
      language: 'Java',
      starCount: 27000,
      forkCount: 13400,
      lastUpdated: DateTime.now().subtract(const Duration(days: 11)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'apache',
      name: 'spark',
      description:
          'Apache Spark - A unified analytics engine for large-scale data processing',
      language: 'Scala',
      starCount: 37000,
      forkCount: 27800,
      lastUpdated: DateTime.now().subtract(const Duration(days: 12)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'jekyll',
      name: 'jekyll',
      description: 'Jekyll is a blog-aware static site generator in Ruby',
      language: 'Ruby',
      starCount: 47000,
      forkCount: 10200,
      lastUpdated: DateTime.now().subtract(const Duration(days: 13)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'gatsbyjs',
      name: 'gatsby',
      description: 'The fastest frontend for the headless web',
      language: 'JavaScript',
      starCount: 55000,
      forkCount: 10600,
      lastUpdated: DateTime.now().subtract(const Duration(days: 14)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'nuxt',
      name: 'nuxt.js',
      description: 'The Intuitive Vue Framework',
      language: 'JavaScript',
      starCount: 51000,
      forkCount: 4600,
      lastUpdated: DateTime.now().subtract(const Duration(days: 15)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'sveltejs',
      name: 'svelte',
      description: 'Cybernetically enhanced web apps',
      language: 'JavaScript',
      starCount: 75000,
      forkCount: 3900,
      lastUpdated: DateTime.now().subtract(const Duration(days: 16)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'remix-run',
      name: 'remix',
      description:
          'Build Better Websites. Create modern, resilient user experiences with web fundamentals',
      language: 'TypeScript',
      starCount: 27000,
      forkCount: 2300,
      lastUpdated: DateTime.now().subtract(const Duration(days: 17)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'solidjs',
      name: 'solid',
      description:
          'A declarative, efficient, and flexible JavaScript library for building user interfaces',
      language: 'TypeScript',
      starCount: 30000,
      forkCount: 850,
      lastUpdated: DateTime.now().subtract(const Duration(days: 18)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'qwikdev',
      name: 'qwik',
      description:
          'The HTML-first framework. Instant apps of any size with ~ 1kb JS',
      language: 'TypeScript',
      starCount: 19000,
      forkCount: 1200,
      lastUpdated: DateTime.now().subtract(const Duration(days: 19)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'astro-build',
      name: 'astro',
      description:
          'The web framework that scales with you — Build fast content sites, powerful web applications, dynamic server APIs, and everything in-between',
      language: 'TypeScript',
      starCount: 42000,
      forkCount: 2200,
      lastUpdated: DateTime.now().subtract(const Duration(days: 20)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'vitejs',
      name: 'vite',
      description: 'Next generation frontend tooling. It\'s fast!',
      language: 'TypeScript',
      starCount: 64000,
      forkCount: 5700,
      lastUpdated: DateTime.now().subtract(const Duration(days: 21)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'webpack',
      name: 'webpack',
      description: 'A bundler for javascript and friends',
      language: 'JavaScript',
      starCount: 64000,
      forkCount: 8700,
      lastUpdated: DateTime.now().subtract(const Duration(days: 22)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'rollup',
      name: 'rollup',
      description: 'Next-generation ES module bundler',
      language: 'JavaScript',
      starCount: 24000,
      forkCount: 1500,
      lastUpdated: DateTime.now().subtract(const Duration(days: 23)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'parcel-bundler',
      name: 'parcel',
      description: 'The zero configuration build tool for the web',
      language: 'JavaScript',
      starCount: 43000,
      forkCount: 2200,
      lastUpdated: DateTime.now().subtract(const Duration(days: 24)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'esbuild',
      name: 'esbuild',
      description: 'An extremely fast JavaScript and CSS bundler and minifier',
      language: 'Go',
      starCount: 37000,
      forkCount: 1100,
      lastUpdated: DateTime.now().subtract(const Duration(days: 25)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'swc-project',
      name: 'swc',
      description: 'Rust-based platform for the Web',
      language: 'Rust',
      starCount: 29000,
      forkCount: 1100,
      lastUpdated: DateTime.now().subtract(const Duration(days: 26)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'rome',
      name: 'tools',
      description:
          'Unified developer tools for JavaScript, TypeScript, and the web',
      language: 'Rust',
      starCount: 23000,
      forkCount: 660,
      lastUpdated: DateTime.now().subtract(const Duration(days: 27)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'denoland',
      name: 'deno',
      description: 'A modern runtime for JavaScript and TypeScript',
      language: 'Rust',
      starCount: 92000,
      forkCount: 5100,
      lastUpdated: DateTime.now().subtract(const Duration(days: 28)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'oven-sh',
      name: 'bun',
      description:
          'Incredibly fast JavaScript runtime, bundler, test runner, and package manager – all in one',
      language: 'Zig',
      starCount: 68000,
      forkCount: 2400,
      lastUpdated: DateTime.now().subtract(const Duration(days: 29)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'tauri-apps',
      name: 'tauri',
      description:
          'Build smaller, faster, and more secure desktop applications with a web frontend',
      language: 'Rust',
      starCount: 75000,
      forkCount: 2200,
      lastUpdated: DateTime.now().subtract(const Duration(days: 30)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'electron',
      name: 'electron',
      description:
          'Build cross-platform desktop apps with JavaScript, HTML, and CSS',
      language: 'C++',
      starCount: 111000,
      forkCount: 14900,
      lastUpdated: DateTime.now().subtract(const Duration(days: 31)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'microsoft',
      name: 'playwright',
      description: 'Playwright is a framework for Web Testing and Automation',
      language: 'TypeScript',
      starCount: 61000,
      forkCount: 3300,
      lastUpdated: DateTime.now().subtract(const Duration(days: 32)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'puppeteer',
      name: 'puppeteer',
      description: 'Headless Chrome Node.js API',
      language: 'TypeScript',
      starCount: 86000,
      forkCount: 9000,
      lastUpdated: DateTime.now().subtract(const Duration(days: 33)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'cypress-io',
      name: 'cypress',
      description:
          'Fast, easy and reliable testing for anything that runs in a browser',
      language: 'JavaScript',
      starCount: 45000,
      forkCount: 3000,
      lastUpdated: DateTime.now().subtract(const Duration(days: 34)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'SeleniumHQ',
      name: 'selenium',
      description: 'A browser automation framework and ecosystem',
      language: 'Java',
      starCount: 28000,
      forkCount: 8000,
      lastUpdated: DateTime.now().subtract(const Duration(days: 35)),
      isPrivate: false,
    ),
  ];

  static final List<FakeUser> _users = [
    FakeUser(
      login: 'octocat',
      name: 'The Octocat',
      bio: 'GitHub mascot and friendly neighborhood cat',
      avatarUrl: 'https://github.com/octocat.png',
      location: 'San Francisco, CA',
      company: 'GitHub',
      website: 'https://github.com',
      repositoryCount: 8,
      followerCount: 4200,
      followingCount: 9,
      createdAt: DateTime(2011, 1, 25),
      organizations: [
        FakeOrganization(
          login: 'github',
          name: 'GitHub',
          description: 'Built for developers',
          avatarUrl: 'https://github.com/github.png',
          publicRepos: 150,
          publicMembers: 500,
        ),
      ],
      starredCount: 42,
    ),
    FakeUser(
      login: 'torvalds',
      name: 'Linus Torvalds',
      bio: 'Creator of Linux and Git',
      avatarUrl: 'https://github.com/torvalds.png',
      location: 'Portland, OR',
      repositoryCount: 4,
      followerCount: 180000,
      followingCount: 0,
      createdAt: DateTime(2011, 9, 3),
      organizations: [],
      starredCount: 12,
    ),
    FakeUser(
      login: 'gaearon',
      name: 'Dan Abramov',
      bio: 'Working on @reactjs. Co-author of Redux and Create React App.',
      avatarUrl: 'https://github.com/gaearon.png',
      location: 'London, UK',
      company: 'Meta',
      website: 'https://overreacted.io',
      repositoryCount: 67,
      followerCount: 89000,
      followingCount: 171,
      createdAt: DateTime(2011, 6, 2),
      organizations: [
        FakeOrganization(
          login: 'facebook',
          name: 'Facebook',
          description:
              'We are working to build community through open source technology.',
          avatarUrl: 'https://github.com/facebook.png',
          publicRepos: 180,
          publicMembers: 230,
        ),
        FakeOrganization(
          login: 'reactjs',
          name: 'React',
          description:
              'React is a JavaScript library for building user interfaces.',
          avatarUrl: 'https://github.com/reactjs.png',
          publicRepos: 25,
          publicMembers: 45,
        ),
      ],
      starredCount: 89,
    ),
    FakeUser(
      login: 'kentcdodds',
      name: 'Kent C. Dodds',
      bio:
          'Making software development more accessible · Husband, Father, Latter-day Saint, Teacher, OSS, @remix_run',
      avatarUrl: 'https://github.com/kentcdodds.png',
      location: 'Utah, USA',
      company: 'Remix',
      website: 'https://kentcdodds.com',
      repositoryCount: 234,
      followerCount: 45000,
      followingCount: 156,
      createdAt: DateTime(2010, 8, 30),
      organizations: [
        FakeOrganization(
          login: 'remix-run',
          name: 'Remix',
          description: 'Build Better Websites',
          avatarUrl: 'https://github.com/remix-run.png',
          publicRepos: 50,
          publicMembers: 12,
        ),
        FakeOrganization(
          login: 'testing-library',
          name: 'Testing Library',
          description:
              'Simple and complete testing utilities that encourage good testing practices',
          avatarUrl: 'https://github.com/testing-library.png',
          publicRepos: 35,
          publicMembers: 25,
        ),
      ],
      starredCount: 156,
    ),
    FakeUser(
      login: 'sindresorhus',
      name: 'Sindre Sorhus',
      bio:
          'Full-Time Open-Sourcerer ·· Maker of 1000+ npm packages and apps ·· Into Swift and Node.js',
      avatarUrl: 'https://github.com/sindresorhus.png',
      repositoryCount: 1200,
      followerCount: 67000,
      followingCount: 89,
    ),
    FakeUser(
      login: 'addyosmani',
      name: 'Addy Osmani',
      bio: 'Engineering Manager at Google working on Chrome',
      avatarUrl: 'https://github.com/addyosmani.png',
      repositoryCount: 156,
      followerCount: 78000,
      followingCount: 234,
    ),
    FakeUser(
      login: 'tj',
      name: 'TJ Holowaychuk',
      bio:
          'Founder of Apex Software. Creator of Express, Koa, Stylus, Component, and many more',
      avatarUrl: 'https://github.com/tj.png',
      repositoryCount: 289,
      followerCount: 56000,
      followingCount: 12,
    ),
    FakeUser(
      login: 'yyx990803',
      name: 'Evan You',
      bio: 'Creator of @vuejs, previously @meteor & @google',
      avatarUrl: 'https://github.com/yyx990803.png',
      repositoryCount: 78,
      followerCount: 92000,
      followingCount: 45,
    ),
    FakeUser(
      login: 'ryanflorence',
      name: 'Ryan Florence',
      bio:
          'Co-founder of @remix-run, creator of @reach/router (merged into React Router), React Training',
      avatarUrl: 'https://github.com/ryanflorence.png',
      repositoryCount: 145,
      followerCount: 34000,
      followingCount: 123,
    ),
    FakeUser(
      login: 'mjackson',
      name: 'Michael Jackson',
      bio: 'Co-founder of @remix-run. Creator of unpkg and React Router',
      avatarUrl: 'https://github.com/mjackson.png',
      repositoryCount: 89,
      followerCount: 28000,
      followingCount: 67,
    ),
    FakeUser(
      login: 'sebmarkbage',
      name: 'Sebastian Markbåge',
      bio: 'React Core Team at Meta',
      avatarUrl: 'https://github.com/sebmarkbage.png',
      repositoryCount: 34,
      followerCount: 23000,
      followingCount: 89,
    ),
    FakeUser(
      login: 'sophiebits',
      name: 'Sophie Alpert',
      bio: 'Former React team lead at Facebook, now at Humu',
      avatarUrl: 'https://github.com/sophiebits.png',
      repositoryCount: 56,
      followerCount: 19000,
      followingCount: 234,
    ),
    FakeUser(
      login: 'acdlite',
      name: 'Andrew Clark',
      bio: 'React Core Team at Meta',
      avatarUrl: 'https://github.com/acdlite.png',
      repositoryCount: 67,
      followerCount: 15000,
      followingCount: 123,
    ),
    FakeUser(
      login: 'rickhanlonii',
      name: 'Rick Hanlon',
      bio: 'React Core Team at Meta',
      avatarUrl: 'https://github.com/rickhanlonii.png',
      repositoryCount: 45,
      followerCount: 12000,
      followingCount: 78,
    ),
    FakeUser(
      login: 'bvaughn',
      name: 'Brian Vaughn',
      bio: 'React DevTools and Profiler at Meta',
      avatarUrl: 'https://github.com/bvaughn.png',
      repositoryCount: 89,
      followerCount: 18000,
      followingCount: 156,
    ),
    FakeUser(
      login: 'timneutkens',
      name: 'Tim Neutkens',
      bio: 'Co-creator of Next.js at Vercel',
      avatarUrl: 'https://github.com/timneutkens.png',
      repositoryCount: 123,
      followerCount: 25000,
      followingCount: 89,
    ),
    FakeUser(
      login: 'rauchg',
      name: 'Guillermo Rauch',
      bio: 'CEO at Vercel. Creator of Socket.IO, Mongoose, Next.js',
      avatarUrl: 'https://github.com/rauchg.png',
      repositoryCount: 167,
      followerCount: 87000,
      followingCount: 234,
    ),
    FakeUser(
      login: 'zenorocha',
      name: 'Zeno Rocha',
      bio: 'CPO at Resend. Creator of Dracula Theme',
      avatarUrl: 'https://github.com/zenorocha.png',
      repositoryCount: 234,
      followerCount: 43000,
      followingCount: 345,
    ),
    FakeUser(
      login: 'wesbos',
      name: 'Wes Bos',
      bio:
          'Full Stack Developer, Speaker and Teacher. Creator of really good courses',
      avatarUrl: 'https://github.com/wesbos.png',
      repositoryCount: 189,
      followerCount: 56000,
      followingCount: 123,
    ),
    FakeUser(
      login: 'bradtraversy',
      name: 'Brad Traversy',
      bio: 'Web Developer & Instructor at Traversy Media',
      avatarUrl: 'https://github.com/bradtraversy.png',
      repositoryCount: 345,
      followerCount: 78000,
      followingCount: 67,
    ),
    FakeUser(
      login: 'getify',
      name: 'Kyle Simpson',
      bio: 'Author of "You Don\'t Know JS" book series. Open web evangelist',
      avatarUrl: 'https://github.com/getify.png',
      repositoryCount: 123,
      followerCount: 34000,
      followingCount: 89,
    ),
    FakeUser(
      login: 'mdo',
      name: 'Mark Otto',
      bio: 'Co-creator of Bootstrap. Design systems at GitHub',
      avatarUrl: 'https://github.com/mdo.png',
      repositoryCount: 89,
      followerCount: 45000,
      followingCount: 234,
    ),
    FakeUser(
      login: 'fat',
      name: 'Jacob Thornton',
      bio: 'Co-creator of Bootstrap. Design at Medium',
      avatarUrl: 'https://github.com/fat.png',
      repositoryCount: 67,
      followerCount: 23000,
      followingCount: 156,
    ),
    FakeUser(
      login: 'dhh',
      name: 'David Heinemeier Hansson',
      bio: 'Creator of Ruby on Rails, Founder & CTO at Basecamp',
      avatarUrl: 'https://github.com/dhh.png',
      repositoryCount: 45,
      followerCount: 67000,
      followingCount: 23,
    ),
    FakeUser(
      login: 'tenderlove',
      name: 'Aaron Patterson',
      bio: 'Ruby and Rails core team member',
      avatarUrl: 'https://github.com/tenderlove.png',
      repositoryCount: 234,
      followerCount: 34000,
      followingCount: 123,
    ),
  ];

  static final List<FakeIssue> _issues = [
    FakeIssue(
      number: 1234,
      title: 'Add dark mode support to the application',
      body:
          'We should add dark mode support to improve user experience in low-light environments. This would include:\n\n- Dark theme colors\n- Proper contrast ratios\n- System theme detection\n- Theme switching UI',
      status: GHStatusType.open,
      labels: ['enhancement', 'ui', 'good first issue'],
      authorLogin: 'johndoe',
      authorAvatarUrl: 'https://github.com/johndoe.png',
      createdAt: DateTime.now().subtract(const Duration(hours: 2)),
      updatedAt: DateTime.now().subtract(const Duration(minutes: 30)),
      commentCount: 5,
      assignee: 'janedoe',
      comments: [
        FakeComment(
          id: 1,
          body: 'Great idea! I\'d love to help with this.',
          authorLogin: 'gaearon',
          authorAvatarUrl: 'https://github.com/gaearon.png',
          createdAt: DateTime.now().subtract(const Duration(hours: 1)),
          reactions: [
            FakeReaction(
              emoji: '👍',
              count: 3,
              users: ['alice', 'bob', 'charlie'],
            ),
            FakeReaction(emoji: '❤️', count: 1, users: ['alice']),
          ],
        ),
      ],
      reactions: [
        FakeReaction(emoji: '👍', count: 8, users: ['alice', 'bob', 'charlie']),
        FakeReaction(emoji: '🎉', count: 2, users: ['alice', 'bob']),
      ],
    ),
    FakeIssue(
      number: 1235,
      title: 'Fix memory leak in image loading component',
      status: GHStatusType.closed,
      labels: ['bug', 'performance'],
      authorLogin: 'alice',
      authorAvatarUrl: 'https://github.com/alice.png',
      createdAt: DateTime.now().subtract(const Duration(days: 3)),
      commentCount: 12,
    ),
    FakeIssue(
      number: 1236,
      title: 'Implement user authentication with OAuth',
      status: GHStatusType.open,
      labels: ['feature', 'authentication', 'security'],
      authorLogin: 'gaearon',
      authorAvatarUrl: 'https://github.com/gaearon.png',
      createdAt: DateTime.now().subtract(const Duration(hours: 6)),
      commentCount: 8,
      assignee: 'kentcdodds',
      // assigneeAvatarUrl: 'https://github.com/kentcdodds.png',
    ),
    FakeIssue(
      number: 1237,
      title: 'Update dependencies to latest versions',
      status: GHStatusType.merged,
      labels: ['dependencies', 'maintenance'],
      authorLogin: 'sindresorhus',
      authorAvatarUrl: 'https://github.com/sindresorhus.png',
      createdAt: DateTime.now().subtract(const Duration(days: 1)),
      commentCount: 3,
    ),
    FakeIssue(
      number: 1238,
      title: 'Add TypeScript support for better type safety',
      status: GHStatusType.draft,
      labels: ['typescript', 'enhancement'],
      authorLogin: 'addyosmani',
      authorAvatarUrl: 'https://github.com/addyosmani.png',
      createdAt: DateTime.now().subtract(const Duration(hours: 12)),
      commentCount: 15,
      assignee: 'tj',
      // assigneeAvatarUrl: 'https://github.com/tj.png',
    ),
    FakeIssue(
      number: 1239,
      title: 'Performance optimization for large datasets',
      status: GHStatusType.open,
      labels: ['performance', 'optimization', 'help wanted'],
      authorLogin: 'yyx990803',
      authorAvatarUrl: 'https://github.com/yyx990803.png',
      createdAt: DateTime.now().subtract(const Duration(hours: 18)),
      commentCount: 22,
    ),
    FakeIssue(
      number: 1240,
      title: 'Fix responsive design issues on mobile devices',
      status: GHStatusType.closed,
      labels: ['bug', 'mobile', 'css'],
      authorLogin: 'ryanflorence',
      authorAvatarUrl: 'https://github.com/ryanflorence.png',
      createdAt: DateTime.now().subtract(const Duration(days: 2)),
      commentCount: 7,
      assignee: 'mjackson',
      // assigneeAvatarUrl: 'https://github.com/mjackson.png',
    ),
    FakeIssue(
      number: 1241,
      title: 'Add comprehensive unit tests for core components',
      status: GHStatusType.open,
      labels: ['testing', 'quality', 'good first issue'],
      authorLogin: 'sebmarkbage',
      authorAvatarUrl: 'https://github.com/sebmarkbage.png',
      createdAt: DateTime.now().subtract(const Duration(hours: 4)),
      commentCount: 11,
    ),
    FakeIssue(
      number: 1242,
      title: 'Implement real-time notifications system',
      status: GHStatusType.open,
      labels: ['feature', 'websockets', 'notifications'],
      authorLogin: 'sophiebits',
      authorAvatarUrl: 'https://github.com/sophiebits.png',
      createdAt: DateTime.now().subtract(const Duration(days: 4)),
      commentCount: 19,
      assignee: 'acdlite',
      // assigneeAvatarUrl: 'https://github.com/acdlite.png',
    ),
    FakeIssue(
      number: 1243,
      title: 'Security vulnerability in user input validation',
      status: GHStatusType.closed,
      labels: ['security', 'critical', 'bug'],
      authorLogin: 'rickhanlonii',
      authorAvatarUrl: 'https://github.com/rickhanlonii.png',
      createdAt: DateTime.now().subtract(const Duration(days: 5)),
      commentCount: 6,
    ),
    FakeIssue(
      number: 1244,
      title: 'Add internationalization (i18n) support',
      status: GHStatusType.draft,
      labels: ['i18n', 'enhancement', 'help wanted'],
      authorLogin: 'bvaughn',
      authorAvatarUrl: 'https://github.com/bvaughn.png',
      createdAt: DateTime.now().subtract(const Duration(hours: 8)),
      commentCount: 13,
    ),
    FakeIssue(
      number: 1245,
      title: 'Improve accessibility for screen readers',
      status: GHStatusType.open,
      labels: ['accessibility', 'a11y', 'enhancement'],
      authorLogin: 'timneutkens',
      authorAvatarUrl: 'https://github.com/timneutkens.png',
      createdAt: DateTime.now().subtract(const Duration(days: 6)),
      commentCount: 9,
      assignee: 'rauchg',
      // assigneeAvatarUrl: 'https://github.com/rauchg.png',
    ),
    FakeIssue(
      number: 1246,
      title: 'Database migration script fails on production',
      status: GHStatusType.open,
      labels: ['bug', 'database', 'production', 'critical'],
      authorLogin: 'zenorocha',
      authorAvatarUrl: 'https://github.com/zenorocha.png',
      createdAt: DateTime.now().subtract(const Duration(hours: 1)),
      commentCount: 4,
    ),
    FakeIssue(
      number: 1247,
      title: 'Add support for custom themes',
      status: GHStatusType.merged,
      labels: ['feature', 'theming', 'ui'],
      authorLogin: 'wesbos',
      authorAvatarUrl: 'https://github.com/wesbos.png',
      createdAt: DateTime.now().subtract(const Duration(days: 7)),
      commentCount: 16,
    ),
    FakeIssue(
      number: 1248,
      title: 'Optimize bundle size for better performance',
      status: GHStatusType.open,
      labels: ['performance', 'bundling', 'optimization'],
      authorLogin: 'bradtraversy',
      authorAvatarUrl: 'https://github.com/bradtraversy.png',
      createdAt: DateTime.now().subtract(const Duration(hours: 14)),
      commentCount: 8,
    ),
    FakeIssue(
      number: 1249,
      title: 'Add drag and drop functionality',
      status: GHStatusType.draft,
      labels: ['feature', 'ui', 'interaction'],
      authorLogin: 'getify',
      authorAvatarUrl: 'https://github.com/getify.png',
      createdAt: DateTime.now().subtract(const Duration(days: 8)),
      commentCount: 12,
      assignee: 'mdo',
      // assigneeAvatarUrl: 'https://github.com/mdo.png',
    ),
    FakeIssue(
      number: 1250,
      title: 'Fix broken links in documentation',
      status: GHStatusType.closed,
      labels: ['documentation', 'bug', 'good first issue'],
      authorLogin: 'fat',
      authorAvatarUrl: 'https://github.com/fat.png',
      createdAt: DateTime.now().subtract(const Duration(days: 9)),
      commentCount: 2,
    ),
    FakeIssue(
      number: 1251,
      title: 'Implement caching strategy for API responses',
      status: GHStatusType.open,
      labels: ['performance', 'caching', 'api'],
      authorLogin: 'dhh',
      authorAvatarUrl: 'https://github.com/dhh.png',
      createdAt: DateTime.now().subtract(const Duration(hours: 20)),
      commentCount: 14,
    ),
    FakeIssue(
      number: 1252,
      title: 'Add support for keyboard shortcuts',
      status: GHStatusType.open,
      labels: ['feature', 'accessibility', 'ux'],
      authorLogin: 'tenderlove',
      authorAvatarUrl: 'https://github.com/tenderlove.png',
      createdAt: DateTime.now().subtract(const Duration(days: 10)),
      commentCount: 7,
      assignee: 'octocat',
      // assigneeAvatarUrl: 'https://github.com/octocat.png',
    ),
    FakeIssue(
      number: 1253,
      title: 'Memory usage spikes during file uploads',
      status: GHStatusType.open,
      labels: ['bug', 'memory', 'file-upload'],
      authorLogin: 'torvalds',
      authorAvatarUrl: 'https://github.com/torvalds.png',
      createdAt: DateTime.now().subtract(const Duration(hours: 3)),
      commentCount: 18,
    ),
    FakeIssue(
      number: 1254,
      title: 'Add progressive web app (PWA) support',
      status: GHStatusType.draft,
      labels: ['pwa', 'enhancement', 'mobile'],
      authorLogin: 'gaearon',
      authorAvatarUrl: 'https://github.com/gaearon.png',
      createdAt: DateTime.now().subtract(const Duration(days: 11)),
      commentCount: 25,
    ),
    FakeIssue(
      number: 1255,
      title: 'Improve error handling and user feedback',
      status: GHStatusType.open,
      labels: ['ux', 'error-handling', 'enhancement'],
      authorLogin: 'kentcdodds',
      authorAvatarUrl: 'https://github.com/kentcdodds.png',
      createdAt: DateTime.now().subtract(const Duration(hours: 16)),
      commentCount: 10,
    ),
    FakeIssue(
      number: 1256,
      title: 'Add support for multiple file formats',
      status: GHStatusType.merged,
      labels: ['feature', 'file-handling'],
      authorLogin: 'sindresorhus',
      authorAvatarUrl: 'https://github.com/sindresorhus.png',
      createdAt: DateTime.now().subtract(const Duration(days: 12)),
      commentCount: 6,
    ),
    FakeIssue(
      number: 1257,
      title: 'Fix race condition in async operations',
      status: GHStatusType.closed,
      labels: ['bug', 'async', 'concurrency'],
      authorLogin: 'addyosmani',
      authorAvatarUrl: 'https://github.com/addyosmani.png',
      createdAt: DateTime.now().subtract(const Duration(days: 13)),
      commentCount: 9,
    ),
    FakeIssue(
      number: 1258,
      title: 'Add comprehensive API documentation',
      status: GHStatusType.open,
      labels: ['documentation', 'api', 'help wanted'],
      authorLogin: 'tj',
      authorAvatarUrl: 'https://github.com/tj.png',
      createdAt: DateTime.now().subtract(const Duration(hours: 22)),
      commentCount: 4,
    ),
    FakeIssue(
      number: 1259,
      title: 'Implement user preferences and settings',
      status: GHStatusType.draft,
      labels: ['feature', 'user-settings', 'ui'],
      authorLogin: 'yyx990803',
      authorAvatarUrl: 'https://github.com/yyx990803.png',
      createdAt: DateTime.now().subtract(const Duration(days: 14)),
      commentCount: 17,
    ),
    FakeIssue(
      number: 1260,
      title: 'Fix CSS layout issues in Safari',
      status: GHStatusType.open,
      labels: ['bug', 'css', 'safari', 'browser-specific'],
      authorLogin: 'ryanflorence',
      authorAvatarUrl: 'https://github.com/ryanflorence.png',
      createdAt: DateTime.now().subtract(const Duration(hours: 10)),
      commentCount: 5,
    ),
    FakeIssue(
      number: 1261,
      title: 'Add automated testing pipeline',
      status: GHStatusType.merged,
      labels: ['testing', 'ci-cd', 'automation'],
      authorLogin: 'mjackson',
      authorAvatarUrl: 'https://github.com/mjackson.png',
      createdAt: DateTime.now().subtract(const Duration(days: 15)),
      commentCount: 11,
    ),
    FakeIssue(
      number: 1262,
      title: 'Improve search functionality with filters',
      status: GHStatusType.open,
      labels: ['feature', 'search', 'ui'],
      authorLogin: 'sebmarkbage',
      authorAvatarUrl: 'https://github.com/sebmarkbage.png',
      createdAt: DateTime.now().subtract(const Duration(hours: 26)),
      commentCount: 13,
    ),
    FakeIssue(
      number: 1263,
      title: 'Add support for custom plugins',
      status: GHStatusType.draft,
      labels: ['feature', 'plugins', 'extensibility'],
      authorLogin: 'sophiebits',
      authorAvatarUrl: 'https://github.com/sophiebits.png',
      createdAt: DateTime.now().subtract(const Duration(days: 16)),
      commentCount: 21,
    ),
    FakeIssue(
      number: 1264,
      title: 'Fix memory leaks in event listeners',
      status: GHStatusType.closed,
      labels: ['bug', 'memory', 'events'],
      authorLogin: 'acdlite',
      authorAvatarUrl: 'https://github.com/acdlite.png',
      createdAt: DateTime.now().subtract(const Duration(days: 17)),
      commentCount: 8,
    ),
  ];

  static final List<FakeFile> _files = [
    FakeFile(
      name: 'README.md',
      type: GHFileType.markdown,
      lastCommitMessage: 'Update installation instructions',
      lastModified: DateTime.now().subtract(const Duration(days: 2)),
      author: 'johndoe',
      size: 2400,
      path: 'README.md',
      content: '''# GitHub Client

A modern GitHub client built with Flutter.

## Features

- Browse repositories
- View issues and pull requests
- User profiles and organizations
- Dark mode support
- Cross-platform (iOS, Android, Web)

## Installation

1. Clone the repository
2. Run `flutter pub get`
3. Run `flutter run`

## Contributing

Pull requests are welcome! Please read our contributing guidelines first.

## License

MIT License - see LICENSE file for details.''',
    ),
    FakeFile(
      name: 'src',
      type: GHFileType.directory,
      lastCommitMessage: 'Add new components',
      lastModified: DateTime.now().subtract(const Duration(hours: 5)),
      author: 'janedoe',
    ),
    FakeFile(
      name: 'package.json',
      type: GHFileType.config,
      lastCommitMessage: 'Update dependencies',
      lastModified: DateTime.now().subtract(const Duration(hours: 12)),
      author: 'gaearon',
      size: 1200,
    ),
    FakeFile(
      name: 'lib',
      type: GHFileType.directory,
      lastCommitMessage: 'Refactor core library',
      lastModified: DateTime.now().subtract(const Duration(days: 1)),
      author: 'kentcdodds',
    ),
    FakeFile(
      name: 'main.dart',
      type: GHFileType.code,
      lastCommitMessage: 'Fix app initialization',
      lastModified: DateTime.now().subtract(const Duration(hours: 8)),
      author: 'sindresorhus',
      size: 3400,
      path: 'lib/main.dart',
      content: '''import 'package:flutter/material.dart';
import 'src/app.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GitHub Client',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'GitHub Client'),
    );
  }
}''',
    ),
    FakeFile(
      name: 'pubspec.yaml',
      type: GHFileType.config,
      lastCommitMessage: 'Add new dependencies',
      lastModified: DateTime.now().subtract(const Duration(days: 3)),
      author: 'addyosmani',
      size: 800,
    ),
    FakeFile(
      name: 'test',
      type: GHFileType.directory,
      lastCommitMessage: 'Add comprehensive tests',
      lastModified: DateTime.now().subtract(const Duration(hours: 18)),
      author: 'tj',
    ),
    FakeFile(
      name: 'docs',
      type: GHFileType.directory,
      lastCommitMessage: 'Update documentation',
      lastModified: DateTime.now().subtract(const Duration(days: 4)),
      author: 'yyx990803',
    ),
    FakeFile(
      name: 'CHANGELOG.md',
      type: GHFileType.markdown,
      lastCommitMessage: 'Update changelog for v2.1.0',
      lastModified: DateTime.now().subtract(const Duration(days: 5)),
      author: 'ryanflorence',
      size: 5600,
    ),
    FakeFile(
      name: 'LICENSE',
      type: GHFileType.file,
      lastCommitMessage: 'Update license year',
      lastModified: DateTime.now().subtract(const Duration(days: 180)),
      author: 'mjackson',
      size: 1100,
    ),
    FakeFile(
      name: '.gitignore',
      type: GHFileType.config,
      lastCommitMessage: 'Add build artifacts to gitignore',
      lastModified: DateTime.now().subtract(const Duration(days: 6)),
      author: 'sebmarkbage',
      size: 450,
    ),
    FakeFile(
      name: 'assets',
      type: GHFileType.directory,
      lastCommitMessage: 'Add new icons and images',
      lastModified: DateTime.now().subtract(const Duration(hours: 24)),
      author: 'sophiebits',
    ),
    FakeFile(
      name: 'config.json',
      type: GHFileType.config,
      lastCommitMessage: 'Update production config',
      lastModified: DateTime.now().subtract(const Duration(days: 7)),
      author: 'acdlite',
      size: 680,
    ),
    FakeFile(
      name: 'scripts',
      type: GHFileType.directory,
      lastCommitMessage: 'Add deployment scripts',
      lastModified: DateTime.now().subtract(const Duration(days: 8)),
      author: 'rickhanlonii',
    ),
    FakeFile(
      name: 'Dockerfile',
      type: GHFileType.config,
      lastCommitMessage: 'Optimize Docker image size',
      lastModified: DateTime.now().subtract(const Duration(days: 9)),
      author: 'bvaughn',
      size: 890,
    ),
    FakeFile(
      name: 'docker-compose.yml',
      type: GHFileType.config,
      lastCommitMessage: 'Add development environment',
      lastModified: DateTime.now().subtract(const Duration(days: 10)),
      author: 'timneutkens',
      size: 1200,
    ),
    FakeFile(
      name: '.github',
      type: GHFileType.directory,
      lastCommitMessage: 'Add GitHub workflows',
      lastModified: DateTime.now().subtract(const Duration(days: 11)),
      author: 'rauchg',
    ),
    FakeFile(
      name: 'tsconfig.json',
      type: GHFileType.config,
      lastCommitMessage: 'Update TypeScript configuration',
      lastModified: DateTime.now().subtract(const Duration(days: 12)),
      author: 'zenorocha',
      size: 560,
    ),
    FakeFile(
      name: 'webpack.config.js',
      type: GHFileType.code,
      lastCommitMessage: 'Optimize build configuration',
      lastModified: DateTime.now().subtract(const Duration(days: 13)),
      author: 'wesbos',
      size: 2300,
    ),
    FakeFile(
      name: 'jest.config.js',
      type: GHFileType.code,
      lastCommitMessage: 'Configure test environment',
      lastModified: DateTime.now().subtract(const Duration(days: 14)),
      author: 'bradtraversy',
      size: 780,
    ),
    FakeFile(
      name: '.eslintrc.js',
      type: GHFileType.config,
      lastCommitMessage: 'Update linting rules',
      lastModified: DateTime.now().subtract(const Duration(days: 15)),
      author: 'getify',
      size: 1400,
    ),
    FakeFile(
      name: '.prettierrc',
      type: GHFileType.config,
      lastCommitMessage: 'Configure code formatting',
      lastModified: DateTime.now().subtract(const Duration(days: 16)),
      author: 'mdo',
      size: 120,
    ),
    FakeFile(
      name: 'components',
      type: GHFileType.directory,
      lastCommitMessage: 'Add reusable UI components',
      lastModified: DateTime.now().subtract(const Duration(hours: 36)),
      author: 'fat',
    ),
    FakeFile(
      name: 'utils',
      type: GHFileType.directory,
      lastCommitMessage: 'Add utility functions',
      lastModified: DateTime.now().subtract(const Duration(days: 17)),
      author: 'dhh',
    ),
    FakeFile(
      name: 'styles',
      type: GHFileType.directory,
      lastCommitMessage: 'Update global styles',
      lastModified: DateTime.now().subtract(const Duration(days: 18)),
      author: 'tenderlove',
    ),
    FakeFile(
      name: 'api',
      type: GHFileType.directory,
      lastCommitMessage: 'Add API endpoints',
      lastModified: DateTime.now().subtract(const Duration(days: 19)),
      author: 'octocat',
    ),
    FakeFile(
      name: 'database',
      type: GHFileType.directory,
      lastCommitMessage: 'Add database migrations',
      lastModified: DateTime.now().subtract(const Duration(days: 20)),
      author: 'torvalds',
    ),
    FakeFile(
      name: 'public',
      type: GHFileType.directory,
      lastCommitMessage: 'Add static assets',
      lastModified: DateTime.now().subtract(const Duration(days: 21)),
      author: 'gaearon',
    ),
    FakeFile(
      name: 'build',
      type: GHFileType.directory,
      lastCommitMessage: 'Update build output',
      lastModified: DateTime.now().subtract(const Duration(hours: 2)),
      author: 'kentcdodds',
    ),
    FakeFile(
      name: 'node_modules',
      type: GHFileType.directory,
      lastCommitMessage: 'Install dependencies',
      lastModified: DateTime.now().subtract(const Duration(hours: 4)),
      author: 'sindresorhus',
    ),
  ];
}

/// Fake repository data model
class FakeRepository {
  final String owner;
  final String name;
  final String description;
  final String language;
  final int starCount;
  final int forkCount;
  final int watcherCount;
  final DateTime lastUpdated;
  final DateTime? createdAt;
  final bool isPrivate;
  final List<String> topics;
  final String? license;
  final String? homepage;
  final List<FakeFile> files;
  final List<FakeIssue> issues;
  final bool isFork;
  final bool isArchived;
  final List<FakeRelease> releases;
  final List<FakeContributor> contributors;
  final String? readme;
  final bool isStarred;
  final bool isWatched;

  const FakeRepository({
    required this.owner,
    required this.name,
    required this.description,
    required this.language,
    required this.starCount,
    required this.forkCount,
    this.watcherCount = 0,
    required this.lastUpdated,
    this.createdAt,
    this.isPrivate = false,
    this.topics = const [],
    this.license,
    this.homepage,
    this.files = const [],
    this.issues = const [],
    this.releases = const [],
    this.contributors = const [],
    this.readme,
    this.isStarred = false,
    this.isWatched = false,
    this.isFork = false,
    this.isArchived = false,
  });

  /// Create a copy of this repository with optional field overrides
  FakeRepository copyWith({
    String? owner,
    String? name,
    String? description,
    String? language,
    int? starCount,
    int? forkCount,
    int? watcherCount,
    DateTime? lastUpdated,
    DateTime? createdAt,
    bool? isPrivate,
    List<String>? topics,
    String? license,
    String? homepage,
    List<FakeFile>? files,
    List<FakeIssue>? issues,
    List<FakeRelease>? releases,
    List<FakeContributor>? contributors,
    String? readme,
    bool? isStarred,
    bool? isWatched,
  }) {
    return FakeRepository(
      owner: owner ?? this.owner,
      name: name ?? this.name,
      description: description ?? this.description,
      language: language ?? this.language,
      starCount: starCount ?? this.starCount,
      forkCount: forkCount ?? this.forkCount,
      watcherCount: watcherCount ?? this.watcherCount,
      lastUpdated: lastUpdated ?? this.lastUpdated,
      createdAt: createdAt ?? this.createdAt,
      isPrivate: isPrivate ?? this.isPrivate,
      topics: topics ?? this.topics,
      license: license ?? this.license,
      homepage: homepage ?? this.homepage,
      files: files ?? this.files,
      issues: issues ?? this.issues,
      releases: releases ?? this.releases,
      contributors: contributors ?? this.contributors,
      readme: readme ?? this.readme,
      isStarred: isStarred ?? this.isStarred,
      isWatched: isWatched ?? this.isWatched,
    );
  }
}

/// Fake user data model
class FakeUser {
  final String login;
  final String? name;
  final String? bio;
  final String avatarUrl;
  final String? location;
  final String? company;
  final String? website;
  final int repositoryCount;
  final int followerCount;
  final int followingCount;
  final DateTime? createdAt;
  final List<FakeOrganization> organizations;
  final bool isFollowing;
  final int? starredCount;

  const FakeUser({
    required this.login,
    this.name,
    this.bio,
    required this.avatarUrl,
    this.location,
    this.company,
    this.website,
    required this.repositoryCount,
    required this.followerCount,
    required this.followingCount,
    this.createdAt,
    this.organizations = const [],
    this.isFollowing = false,
    this.starredCount,
  });
}

/// Fake organization data model
class FakeOrganization {
  final String login;
  final String name;
  final String? description;
  final String avatarUrl;
  final int publicRepos;
  final int publicMembers;
  final String? website;
  final String? location;

  const FakeOrganization({
    required this.login,
    required this.name,
    this.description,
    required this.avatarUrl,
    required this.publicRepos,
    required this.publicMembers,
    this.website,
    this.location,
  });
}

/// Fake issue data model
class FakeIssue {
  final int number;
  final String title;
  final String body;
  final GHStatusType status;
  final List<String> labels;
  final String authorLogin;
  final String authorAvatarUrl;
  final DateTime createdAt;
  final DateTime? updatedAt;
  final DateTime? closedAt;
  final int commentCount;
  final String? assignee;
  final List<FakeComment> comments;
  final List<FakeReaction> reactions;
  final bool isPullRequest;

  const FakeIssue({
    required this.number,
    required this.title,
    this.body = '',
    required this.status,
    this.labels = const [],
    required this.authorLogin,
    required this.authorAvatarUrl,
    required this.createdAt,
    this.updatedAt,
    this.closedAt,
    this.commentCount = 0,
    this.assignee,
    this.comments = const [],
    this.reactions = const [],
    this.isPullRequest = false,
  });

  /// Getter for assignee login (for compatibility with GHIssueCard)
  String? get assigneeLogin => assignee;

  /// Getter for assignee avatar URL (for compatibility with GHIssueCard)
  String? get assigneeAvatarUrl =>
      assignee != null ? 'https://github.com/$assignee.png' : null;

  /// Creates a copy of this issue with the given fields replaced with new values
  FakeIssue copyWith({
    int? number,
    String? title,
    String? body,
    GHStatusType? status,
    List<String>? labels,
    String? authorLogin,
    String? authorAvatarUrl,
    DateTime? createdAt,
    DateTime? updatedAt,
    DateTime? closedAt,
    int? commentCount,
    String? assignee,
    List<FakeComment>? comments,
    List<FakeReaction>? reactions,
    bool? isPullRequest,
  }) {
    return FakeIssue(
      number: number ?? this.number,
      title: title ?? this.title,
      body: body ?? this.body,
      status: status ?? this.status,
      labels: labels ?? this.labels,
      authorLogin: authorLogin ?? this.authorLogin,
      authorAvatarUrl: authorAvatarUrl ?? this.authorAvatarUrl,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      closedAt: closedAt ?? this.closedAt,
      commentCount: commentCount ?? this.commentCount,
      assignee: assignee ?? this.assignee,
      comments: comments ?? this.comments,
      reactions: reactions ?? this.reactions,
      isPullRequest: isPullRequest ?? this.isPullRequest,
    );
  }
}

/// Fake file data model
class FakeFile {
  final String name;
  final GHFileType type;
  final String lastCommitMessage;
  final DateTime lastModified;
  final String author;
  final int? size;
  final String? content;
  final String path;

  const FakeFile({
    required this.name,
    required this.type,
    required this.lastCommitMessage,
    required this.lastModified,
    required this.author,
    this.size,
    this.content,
    this.path = '',
  });

  /// Returns true if this file is a directory
  bool get isDirectory => type == GHFileType.directory;
}

/// Fake comment data model
class FakeComment {
  final int id;
  final String body;
  final String authorLogin;
  final String authorAvatarUrl;
  final DateTime createdAt;
  final DateTime? updatedAt;
  final List<FakeReaction> reactions;

  const FakeComment({
    required this.id,
    required this.body,
    required this.authorLogin,
    required this.authorAvatarUrl,
    required this.createdAt,
    this.updatedAt,
    this.reactions = const [],
  });
}

/// Fake reaction data model
class FakeReaction {
  final String emoji;
  final int count;
  final List<String> users;

  const FakeReaction({
    required this.emoji,
    required this.count,
    this.users = const [],
  });
}

/// Fake release data model
class FakeRelease {
  final String tagName;
  final String name;
  final String? body;
  final String authorLogin;
  final DateTime publishedAt;
  final bool isPrerelease;
  final bool isDraft;
  final List<FakeAsset> assets;

  const FakeRelease({
    required this.tagName,
    required this.name,
    this.body,
    required this.authorLogin,
    required this.publishedAt,
    this.isPrerelease = false,
    this.isDraft = false,
    this.assets = const [],
  });
}

/// Fake asset data model
class FakeAsset {
  final String name;
  final int size;
  final int downloadCount;

  const FakeAsset({
    required this.name,
    required this.size,
    required this.downloadCount,
  });
}

/// Fake contributor data model
class FakeContributor {
  final String login;
  final String avatarUrl;
  final int contributions;

  const FakeContributor({
    required this.login,
    required this.avatarUrl,
    required this.contributions,
  });
}

/// Fake activity data model
class FakeActivity {
  final String type;
  final String title;
  final String? description;
  final String actorLogin;
  final String actorAvatarUrl;
  final DateTime createdAt;
  final String? repositoryName;
  final String? repositoryOwner;

  const FakeActivity({
    required this.type,
    required this.title,
    this.description,
    required this.actorLogin,
    required this.actorAvatarUrl,
    required this.createdAt,
    this.repositoryName,
    this.repositoryOwner,
  });
}
