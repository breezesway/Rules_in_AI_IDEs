import 'package:flutter/material.dart';
import '../utils/color_utils.dart';
import '../utils/date_formatter.dart';
import '../utils/number_formatter.dart';

/// Centralized provider for realistic fake data used in design system showcase screens.
///
/// This class provides sample data that represents real GitHub content including
/// repositories, users, issues, and other entities for demonstration purposes.
class FakeDataProvider {
  // Private constructor to prevent instantiation
  const FakeDataProvider._();

  /// Sample GitHub repositories with realistic data
  static final List<FakeRepository> repositories = [
    FakeRepository(
      name: 'react',
      owner: 'facebook',
      description:
          'A declarative, efficient, and flexible JavaScript library for building user interfaces.',
      language: 'JavaScript',
      starCount: 218000,
      forkCount: 45200,
      watcherCount: 6800,
      issueCount: 1234,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 2)),
      isPrivate: false,
      topics: ['javascript', 'react', 'frontend', 'ui', 'library'],
      license: 'MIT',
    ),
    FakeRepository(
      name: 'flutter',
      owner: 'flutter',
      description:
          'Flutter makes it easy and fast to build beautiful apps for mobile and beyond.',
      language: 'Dart',
      starCount: 162000,
      forkCount: 26700,
      watcherCount: 3400,
      issueCount: 12567,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 5)),
      isPrivate: false,
      topics: ['flutter', 'dart', 'mobile', 'cross-platform', 'ui'],
      license: 'BSD-3-Clause',
    ),
    FakeRepository(
      name: 'vscode',
      owner: 'microsoft',
      description: 'Visual Studio Code - Open Source ("Code - OSS")',
      language: 'TypeScript',
      starCount: 156000,
      forkCount: 27800,
      watcherCount: 3200,
      issueCount: 5678,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 1)),
      isPrivate: false,
      topics: ['typescript', 'editor', 'vscode', 'electron'],
      license: 'MIT',
    ),
    FakeRepository(
      name: 'kubernetes',
      owner: 'kubernetes',
      description: 'Production-Grade Container Scheduling and Management',
      language: 'Go',
      starCount: 106000,
      forkCount: 38400,
      watcherCount: 3100,
      issueCount: 2345,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 3)),
      isPrivate: false,
      topics: ['go', 'kubernetes', 'containers', 'orchestration'],
      license: 'Apache-2.0',
    ),
    FakeRepository(
      name: 'tensorflow',
      owner: 'tensorflow',
      description: 'An Open Source Machine Learning Framework for Everyone',
      language: 'Python',
      starCount: 182000,
      forkCount: 88200,
      watcherCount: 8900,
      issueCount: 3456,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 4)),
      isPrivate: false,
      topics: ['python', 'machine-learning', 'tensorflow', 'ai'],
      license: 'Apache-2.0',
    ),
  ];

  /// Sample GitHub users with realistic profiles
  static final List<FakeUser> users = [
    FakeUser(
      login: 'octocat',
      name: 'The Octocat',
      bio: 'GitHub mascot and friendly neighborhood cat-octopus hybrid.',
      avatarUrl: 'https://github.com/octocat.png',
      followers: 4200,
      following: 9,
      repositories: 8,
      location: 'San Francisco, CA',
      company: 'GitHub',
      website: 'https://github.com/octocat',
      joinedDate: DateTime(2011, 1, 25),
    ),
    FakeUser(
      login: 'torvalds',
      name: 'Linus Torvalds',
      bio: 'Creator of Linux and Git. Just a simple Finnish guy.',
      avatarUrl: 'https://github.com/torvalds.png',
      followers: 156000,
      following: 0,
      repositories: 4,
      location: 'Portland, OR',
      company: 'Linux Foundation',
      website: null,
      joinedDate: DateTime(2011, 9, 19),
    ),
    FakeUser(
      login: 'gaearon',
      name: 'Dan Abramov',
      bio: 'Working on @reactjs. Co-author of Redux and Create React App.',
      avatarUrl: 'https://github.com/gaearon.png',
      followers: 89000,
      following: 171,
      repositories: 245,
      location: 'London, UK',
      company: 'Meta',
      website: 'https://overreacted.io',
      joinedDate: DateTime(2011, 6, 2),
    ),
    FakeUser(
      login: 'ken',
      name: 'Ken Thompson',
      bio: 'Co-creator of Unix, B programming language, and UTF-8.',
      avatarUrl: 'https://github.com/ken.png',
      followers: 23000,
      following: 0,
      repositories: 1,
      location: 'Murray Hill, NJ',
      company: 'Google',
      website: null,
      joinedDate: DateTime(2012, 3, 15),
    ),
    FakeUser(
      login: 'dhh',
      name: 'David Heinemeier Hansson',
      bio: 'Creator of Ruby on Rails, Founder & CTO at Basecamp.',
      avatarUrl: 'https://github.com/dhh.png',
      followers: 67000,
      following: 123,
      repositories: 89,
      location: 'Chicago, IL',
      company: 'Basecamp',
      website: 'https://dhh.dk',
      joinedDate: DateTime(2008, 4, 10),
    ),
  ];

  /// Sample GitHub issues with realistic content
  static final List<FakeIssue> issues = [
    FakeIssue(
      number: 1234,
      title: 'Add dark mode support to the application',
      body:
          'Users have been requesting dark mode support. This would improve accessibility and user experience, especially for users working in low-light environments.',
      author: users[2], // gaearon
      status: IssueStatus.open,
      labels: ['enhancement', 'ui', 'accessibility'],
      assignees: [users[0]], // octocat
      createdAt: DateTime.now().subtract(const Duration(hours: 2)),
      updatedAt: DateTime.now().subtract(const Duration(minutes: 30)),
      commentCount: 15,
    ),
    FakeIssue(
      number: 1235,
      title: 'Fix memory leak in image loading component',
      body:
          'There appears to be a memory leak when loading large images. Memory usage continues to grow and doesn\'t get released properly.',
      author: users[1], // torvalds
      status: IssueStatus.closed,
      labels: ['bug', 'performance', 'images'],
      assignees: [users[2]], // gaearon
      createdAt: DateTime.now().subtract(const Duration(days: 5)),
      updatedAt: DateTime.now().subtract(const Duration(days: 1)),
      commentCount: 8,
    ),
    FakeIssue(
      number: 1236,
      title: 'Implement user authentication with OAuth',
      body:
          'Add support for OAuth authentication with GitHub, Google, and other providers.',
      author: users[4], // dhh
      status: IssueStatus.draft,
      labels: ['feature', 'authentication', 'oauth'],
      assignees: [],
      createdAt: DateTime.now().subtract(const Duration(days: 3)),
      updatedAt: DateTime.now().subtract(const Duration(hours: 6)),
      commentCount: 3,
    ),
    FakeIssue(
      number: 1237,
      title: 'Update documentation for new API endpoints',
      body:
          'The documentation needs to be updated to reflect the new API endpoints introduced in v2.0.',
      author: users[0], // octocat
      status: IssueStatus.merged,
      labels: ['documentation', 'api'],
      assignees: [users[4]], // dhh
      createdAt: DateTime.now().subtract(const Duration(days: 7)),
      updatedAt: DateTime.now().subtract(const Duration(days: 2)),
      commentCount: 12,
    ),
  ];

  /// GitHub-appropriate button labels for demonstrations
  static const List<String> buttonLabels = [
    'Star',
    'Watch',
    'Fork',
    'Follow',
    'Clone',
    'Download',
    'Subscribe',
    'Unwatch',
    'Unstar',
    'Unfollow',
    'Create',
    'Edit',
    'Delete',
    'Merge',
    'Close',
    'Reopen',
    'Assign',
    'Review',
    'Approve',
    'Request Changes',
  ];

  /// Status labels for various GitHub entities
  static const List<String> statusLabels = [
    'Open',
    'Closed',
    'Merged',
    'Draft',
    'In Progress',
    'Approved',
    'Pending',
    'Rejected',
    'Under Review',
    'Needs Work',
    'Ready to Merge',
    'Blocked',
    'On Hold',
    'Completed',
  ];

  /// Sample commit messages
  static const List<String> commitMessages = [
    'Fix critical bug in authentication flow',
    'Add support for dark mode theme',
    'Update dependencies to latest versions',
    'Improve performance of image loading',
    'Add unit tests for user service',
    'Refactor navigation component',
    'Update README with installation instructions',
    'Fix typo in error message',
    'Add validation for user input',
    'Optimize database queries',
    'Update API documentation',
    'Fix responsive layout issues',
  ];

  /// Get sample relative dates for demonstration
  static List<String> getSampleDates() {
    return DateFormatter.getSampleRelativeDates();
  }

  /// Get sample formatted numbers for demonstration
  static List<String> getSampleNumbers() {
    return NumberFormatter.getSampleFormattedNumbers();
  }

  /// Get sample GitHub statistics
  static List<Map<String, dynamic>> getSampleStats() {
    return NumberFormatter.getSampleGitHubStats();
  }

  /// Get popular programming languages with colors
  static List<Map<String, dynamic>> getLanguages() {
    return ColorUtils.getPopularLanguages();
  }

  /// Get a random repository from the sample data
  static FakeRepository getRandomRepository() {
    return repositories[DateTime.now().millisecond % repositories.length];
  }

  /// Get a random user from the sample data
  static FakeUser getRandomUser() {
    return users[DateTime.now().millisecond % users.length];
  }

  /// Get a random issue from the sample data
  static FakeIssue getRandomIssue() {
    return issues[DateTime.now().millisecond % issues.length];
  }
}

/// Model for fake repository data
class FakeRepository {
  final String name;
  final String owner;
  final String description;
  final String language;
  final int starCount;
  final int forkCount;
  final int watcherCount;
  final int issueCount;
  final DateTime lastUpdated;
  final bool isPrivate;
  final List<String> topics;
  final String license;

  const FakeRepository({
    required this.name,
    required this.owner,
    required this.description,
    required this.language,
    required this.starCount,
    required this.forkCount,
    required this.watcherCount,
    required this.issueCount,
    required this.lastUpdated,
    required this.isPrivate,
    required this.topics,
    required this.license,
  });

  String get fullName => '$owner/$name';
  Color get languageColor => ColorUtils.getLanguageColor(language);
  String get formattedStars => NumberFormatter.formatCompact(starCount);
  String get formattedForks => NumberFormatter.formatCompact(forkCount);
  String get formattedWatchers => NumberFormatter.formatCompact(watcherCount);
  String get lastUpdatedRelative => DateFormatter.formatRelative(lastUpdated);
}

/// Model for fake user data
class FakeUser {
  final String login;
  final String name;
  final String bio;
  final String avatarUrl;
  final int followers;
  final int following;
  final int repositories;
  final String? location;
  final String? company;
  final String? website;
  final DateTime joinedDate;

  const FakeUser({
    required this.login,
    required this.name,
    required this.bio,
    required this.avatarUrl,
    required this.followers,
    required this.following,
    required this.repositories,
    this.location,
    this.company,
    this.website,
    required this.joinedDate,
  });

  String get formattedFollowers => NumberFormatter.formatCompact(followers);
  String get formattedFollowing => NumberFormatter.formatCompact(following);
  String get formattedRepositories =>
      NumberFormatter.formatCompact(repositories);
  String get joinedDateRelative => DateFormatter.formatRelative(joinedDate);
}

/// Issue status enumeration
enum IssueStatus { open, closed, merged, draft }

/// Model for fake issue data
class FakeIssue {
  final int number;
  final String title;
  final String body;
  final FakeUser author;
  final IssueStatus status;
  final List<String> labels;
  final List<FakeUser> assignees;
  final DateTime createdAt;
  final DateTime updatedAt;
  final int commentCount;

  const FakeIssue({
    required this.number,
    required this.title,
    required this.body,
    required this.author,
    required this.status,
    required this.labels,
    required this.assignees,
    required this.createdAt,
    required this.updatedAt,
    required this.commentCount,
  });

  String get createdAtRelative => DateFormatter.formatRelative(createdAt);
  String get updatedAtRelative => DateFormatter.formatRelative(updatedAt);
  String get formattedCommentCount =>
      NumberFormatter.formatCompact(commentCount);
}
