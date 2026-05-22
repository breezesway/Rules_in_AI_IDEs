# Navigation Architecture

## Overview

The gh3 application uses a modular, GitHub.com-compatible navigation system built on GoRouter with RouteProvider pattern. This document defines the current state, planned enhancements, and implementation roadmap for the navigation architecture.

## Current Navigation Structure

### Implemented Routes

| Route | Screen | Description |
|-------|--------|-------------|
| `/loading` | LoadingScreen | Initial app loading state |
| `/login` | LoginScreen | GitHub OAuth authentication |
| `/` | HomeScreen | Authenticated user dashboard |
| `/:login` | UserDetailsScreen | User profile overview |
| `/:login/@repositories` | UserRepositoriesScreen | User repositories (with @ prefix) |
| `/:login/starred` | UserStarredScreen | User starred repositories |
| `/:login/organizations` | UserOrganizationsScreen | User organizations |

### Current Architecture Features

- **Modular RouteProvider Pattern**: Each screen module provides its own route configuration
- **Type-Safe Navigation**: AppRoute base class provides type-safe navigation methods
- **Authentication Routing**: Automatic redirects based on auth state
- **Dependency Injection**: Route providers registered with Injectable pattern
- **Route Collection**: Dynamic route collection via RouteCollectionService
- **Route Specificity**: Automatic route sorting by specificity for correct matching

### Current Issues

1. **GitHub URL Incompatibility**: Current `/:login/@repositories` doesn't match GitHub.com patterns
2. **Ambiguous Routes**: Cannot distinguish between users, organizations, and repositories
3. **Limited Repository Support**: No repository browsing capabilities
4. **Query Parameter Limitations**: Current routing system doesn't support query-based navigation (`?tab=repositories`)


## Screen Implementation Table

| Category | Screen Name | Status | Priority | URL | Implementation Notes |
|----------|-------------|--------|----------|-----|---------------------|
| **Auth** | LoadingScreen | ✅ Implemented | - | `/loading` | Complete - handles auth loading state |
| **Auth** | LoginScreen | ✅ Implemented | - | `/login` | Complete - GitHub OAuth flow |
| **Dashboard** | HomeScreen | ✅ Implemented | - | `/` | Complete - authenticated dashboard |
| **User Profile** | UserDetailsScreen | ✅ Implemented | - | `/:login` | Complete - user overview |
| **User Profile** | UserRepositoriesScreen | ✅ Implemented | - | `/:login/@repositories` | Need URL change to `/@tab/repositories` |
| **User Profile** | UserStarredScreen | 🔄 Placeholder | P2 | `/:login/starred` | Placeholder screen - needs GraphQL + URL change to `/@tab/starred` |
| **User Profile** | UserOrganizationsScreen | 🔄 Placeholder | P2 | `/:login/organizations` | Placeholder screen - needs GraphQL + URL change to `/@tab/organizations` |
| **User Profile** | UserProjectsScreen | ❌ Not Implemented | P2 | `/:login/@tab/projects` | New screen - user projects tab |
| **User Profile** | UserPackagesScreen | ❌ Not Implemented | P3 | `/:login/@tab/packages` | New screen - user packages tab |
| **User Profile** | UserGistsScreen | ❌ Not Implemented | P3 | `/:login/@tab/gists` | New screen - user gists tab |
| **User Profile** | UserFollowersScreen | ❌ Not Implemented | P2 | `/:login/@tab/followers` | New screen - user followers list |
| **User Profile** | UserFollowingScreen | ❌ Not Implemented | P2 | `/:login/@tab/following` | New screen - users being followed |
| **Repository** | RepositoryScreen | ❌ Not Implemented | P1 | `/:owner/:repo` | Critical - repository overview/code tab |
| **Repository** | RepositoryTreeScreen | ❌ Not Implemented | P1 | `/:owner/:repo/tree/:ref/:path*` | Critical - file browser interface |
| **Repository** | RepositoryFileScreen | ❌ Not Implemented | P1 | `/:owner/:repo/blob/:ref/:path*` | Critical - file viewer with syntax highlighting |
| **Repository** | RepositoryIssuesScreen | ❌ Not Implemented | P1 | `/:owner/:repo/issues` | High priority - issues list |
| **Repository** | IssueDetailScreen | ❌ Not Implemented | P1 | `/:owner/:repo/issues/:number` | High priority - issue detail view |
| **Repository** | RepositoryPullsScreen | ❌ Not Implemented | P1 | `/:owner/:repo/pulls` | High priority - PR list |
| **Repository** | PullRequestDetailScreen | ❌ Not Implemented | P1 | `/:owner/:repo/pull/:number` | High priority - PR detail view |
| **Repository** | RepositoryCommitsScreen | ❌ Not Implemented | P2 | `/:owner/:repo/commits/:ref?` | Medium priority - commit history |
| **Repository** | CommitDetailScreen | ❌ Not Implemented | P2 | `/:owner/:repo/commit/:sha` | Medium priority - commit diff view |
| **Repository** | RepositoryActionsScreen | ❌ Not Implemented | P2 | `/:owner/:repo/actions` | Medium priority - actions/workflows |
| **Repository** | ActionRunDetailScreen | ❌ Not Implemented | P3 | `/:owner/:repo/actions/runs/:run_id` | Low priority - action run details |
| **Repository** | RepositoryProjectsScreen | ❌ Not Implemented | P3 | `/:owner/:repo/projects` | Low priority - repo projects |
| **Repository** | RepositoryWikiScreen | ❌ Not Implemented | P3 | `/:owner/:repo/wiki` | Low priority - wiki home |
| **Repository** | WikiPageScreen | ❌ Not Implemented | P3 | `/:owner/:repo/wiki/:page*` | Low priority - wiki page viewer |
| **Repository** | RepositorySecurityScreen | ❌ Not Implemented | P3 | `/:owner/:repo/security` | Low priority - security overview |
| **Repository** | RepositoryInsightsScreen | ❌ Not Implemented | P3 | `/:owner/:repo/insights` | Low priority - repo analytics |
| **Repository** | RepositorySettingsScreen | ❌ Not Implemented | P3 | `/:owner/:repo/settings` | Low priority - repo settings |
| **Repository** | RepositoryReleasesScreen | ❌ Not Implemented | P2 | `/:owner/:repo/@part/releases` | Medium priority - releases list |
| **Repository** | ReleaseDetailScreen | ❌ Not Implemented | P3 | `/:owner/:repo/@part/releases/:tag` | Low priority - release details |
| **Repository** | RepositoryStargazersScreen | ❌ Not Implemented | P3 | `/:owner/:repo/@part/stargazers` | Mobile screen - users who starred |
| **Repository** | RepositoryWatchersScreen | ❌ Not Implemented | P3 | `/:owner/:repo/@part/watchers` | Mobile screen - users watching |
| **Repository** | RepositoryForksScreen | ❌ Not Implemented | P3 | `/:owner/:repo/@part/forks` | Mobile screen - repository forks |
| **Repository** | RepositoryContributorsScreen | ❌ Not Implemented | P3 | `/:owner/:repo/@part/contributors` | Mobile screen - repository contributors |
| **Repository** | RepositoryLanguagesScreen | ❌ Not Implemented | P3 | `/:owner/:repo/@part/languages` | Mobile screen - repository languages |
| **Repository** | RepositoryTagsScreen | ❌ Not Implemented | P3 | `/:owner/:repo/@part/tags` | Mobile screen - repository tags |
| **Repository** | RepositoryBranchesScreen | ❌ Not Implemented | P3 | `/:owner/:repo/@part/branches` | Mobile screen - repository branches |
| **Repository** | ActionScreen | ❌ Not Implemented | P2 | `/:owner/:repo/@part/actions/:workflow` | Medium priority - specific workflow |
| **Repository** | ActionRunsScreen | ❌ Not Implemented | P2 | `/:owner/:repo/@part/actions/:workflow/runs` | Medium priority - workflow runs |
| **Repository** | ActionRunScreen | ❌ Not Implemented | P2 | `/:owner/:repo/@part/actions/runs/:run_id` | Medium priority - specific run detail |
| **Repository** | ChecksScreen | ❌ Not Implemented | P2 | `/:owner/:repo/@part/checks` | Medium priority - commit checks |
| **Repository** | CheckScreen | ❌ Not Implemented | P3 | `/:owner/:repo/@part/checks/:check_id` | Low priority - specific check detail |
| **Search** | SearchScreen | ❌ Not Implemented | P2 | `/search` | Medium priority - global search |
| **Search** | SearchRepositoriesScreen | ❌ Not Implemented | P2 | `/search?q=:query&type=repositories` | Future - needs query param support |
| **Search** | SearchCodeScreen | ❌ Not Implemented | P3 | `/search?q=:query&type=code` | Future - needs query param support |
| **Search** | SearchIssuesScreen | ❌ Not Implemented | P3 | `/search?q=:query&type=issues` | Future - needs query param support |
| **Search** | SearchUsersScreen | ❌ Not Implemented | P3 | `/search?q=:query&type=users` | Future - needs query param support |
| **Search** | SearchOrganizationsScreen | ❌ Not Implemented | P3 | `/search?q=:query&type=organizations` | Future - needs query param support |
| **Explore** | ExploreScreen | ❌ Not Implemented | P2 | `/explore` | Medium priority - content discovery |
| **Explore** | TrendingRepositoriesScreen | ❌ Not Implemented | P2 | `/trending` | Medium priority - trending repos |
| **Explore** | TopicsScreen | ❌ Not Implemented | P3 | `/topics` | Low priority - topic browsing |
| **Explore** | TopicDetailScreen | ❌ Not Implemented | P3 | `/topics/:topic` | Low priority - topic detail |
| **Organization** | OrganizationScreen | ❌ Not Implemented | P2 | `/:org` | Medium priority - org overview (detect org vs user) |
| **Organization** | OrgRepositoriesScreen | ❌ Not Implemented | P2 | `/:org/@tab/repositories` | Medium priority - org repos |
| **Organization** | OrgPeopleScreen | ❌ Not Implemented | P3 | `/:org/@tab/people` | Low priority - org members |
| **Organization** | OrgProjectsScreen | ❌ Not Implemented | P3 | `/:org/@tab/projects` | Low priority - org projects |
| **Organization** | OrgPackagesScreen | ❌ Not Implemented | P3 | `/:org/@tab/packages` | Low priority - org packages |
| **Organization** | OrgSettingsScreen | ❌ Not Implemented | P3 | `/:org/@tab/settings` | Low priority - org settings |
| **User Management** | DashboardScreen | ❌ Not Implemented | P2 | `/dashboard` | Medium priority - personal dashboard |
| **User Management** | NotificationsScreen | ❌ Not Implemented | P2 | `/notifications` | Medium priority - user notifications |
| **User Management** | UserSettingsScreen | ❌ Not Implemented | P3 | `/settings` | Low priority - user settings |
| **User Management** | ProfileSettingsScreen | ❌ Not Implemented | P3 | `/settings/profile` | Low priority - profile settings |
| **User Management** | AccountSettingsScreen | ❌ Not Implemented | P3 | `/settings/account` | Low priority - account settings |
| **Projects** | GlobalProjectsScreen | ❌ Not Implemented | P2 | `/projects` | Medium priority - global projects discovery |
| **Projects** | ProjectScreen | ❌ Not Implemented | P2 | `/projects/:project_id` | Medium priority - specific project detail |
| **Projects** | UserProjectScreen | ❌ Not Implemented | P3 | `/:login/@part/projects/:project_id` | Low priority - user project detail |
| **Projects** | OrgProjectScreen | ❌ Not Implemented | P3 | `/:org/@part/projects/:project_id` | Low priority - org project detail |
| **Projects** | RepoProjectScreen | ❌ Not Implemented | P3 | `/:owner/:repo/@part/projects/:project_id` | Low priority - repo project detail |

## Status Legend
- **✅ Implemented**: Fully functional with data loading
- **🔄 Placeholder**: Basic UI shell exists but no data/functionality
- **❌ Not Implemented**: Screen doesn't exist

## Priority Legend
- **P1**: Critical - Core functionality, blocks other features
- **P2**: High - Important features, enhances user experience
- **P3**: Medium - Nice-to-have features, can be deferred

## Code Agent Implementation Notes

### Next Immediate Actions
1. **Fix existing URL structure**: Update `UserRepositoriesScreen`, `UserStarredScreen`, `UserOrganizationsScreen` to use `/@tab/` pattern
2. **Implement P1 Repository screens**: Focus on `RepositoryScreen`, `RepositoryTreeScreen`, `RepositoryFileScreen` first
3. **Follow existing patterns**: Use established ViewModel factory + RouteProvider + Screen structure

### Technical Requirements for Each Screen
- Extend existing modular architecture (screen folder with ViewModel, RouteProvider, Screen)
- Use Injectable pattern for route providers: `@Named("ScreenNameRouteProvider")` `@Singleton(as: RouteProvider)`
- Implement GraphQL queries in `*.graphql` files with code generation
- Follow Widget-GraphQL separation pattern with factory constructors
- Write comprehensive tests for each screen module

### Dependencies and Blockers
- Repository screens depend on GitHub GraphQL schema exploration
- Search screens blocked until query parameter routing support added
- Some advanced features require additional GraphQL queries to be defined

## Technical Implementation Guidelines

### Route Provider Pattern
- Continue using `@Named` and `@Singleton(as: RouteProvider)` pattern
- Implement query parameter parsing in route builders
- Use ViewModel factories for dependency injection
- Maintain modular screen architecture

### URL Validation
- Implement GitHub username validation (alphanumeric, hyphens, max 39 chars)
- Repository name validation (alphanumeric, hyphens, underscores, periods)
- Path parameter sanitization for security

### Navigation State Management
- **Current**: Use path parameters for tab state (`/@tab/repositories`)
- **Future**: Use query parameters for tab state (`?tab=repositories`)
- Implement deep linking for all major features
- Maintain navigation history for proper back navigation
- Support browser-style navigation (forward/back)

### Performance Considerations
- Lazy load repository content (large file trees)
- Implement pagination for large lists (issues, commits)
- Cache frequently accessed data (user profiles, repository metadata)
- Use incremental loading for search results

## Migration Strategy

### Phase 1 Migration
1. **Update Current Routes**: Replace `/:login/@repositories` with `/:login/@tab/repositories`
2. **Add New Tab Routes**: Create additional `/@tab/` routes for starred, organizations, etc.
3. **Update Navigation Calls**: Replace old route usage throughout app
4. **Test Deep Links**: Ensure all deep links work with new format

### Phase 6 Migration (Query Parameter Support)
1. **Add Query Support**: Implement GoRouter query parameter routing
2. **Dual Support**: Support both path-based (`/@tab/`) and query-based (`?tab=`) URLs
3. **Gradual Migration**: Migrate screens one by one to query-based navigation
4. **Deprecate Path-based**: Mark `/@tab/` routes as deprecated after migration

### Backward Compatibility
- Maintain redirect support for old URL patterns during transition
- Update CLAUDE.md documentation with new navigation patterns
- Provide migration guide for any custom navigation implementations

## Success Metrics

### Functional Metrics
- **URL Compatibility**: 100% GitHub.com URL pattern compatibility
- **Deep Linking**: All major features accessible via direct URL
- **Navigation Performance**: Sub-200ms navigation between screens
- **Route Coverage**: Support for all planned GitHub features

### Technical Metrics
- **Route Resolution**: < 10ms route resolution time
- **Memory Usage**: Minimal route provider memory footprint
- **Code Maintainability**: Modular route providers with clear separation of concerns
- **Test Coverage**: 90%+ coverage for navigation logic

## Future Considerations

### Enhanced Features
- **Browser Integration**: History API support for web platform
- **Offline Navigation**: Route caching for offline usage
- **Custom Schemes**: Support for gh3:// custom URL scheme
- **Share Integration**: Native sharing with proper URL generation

### Platform Expansion
- **Web Platform**: Browser-compatible navigation with URL bar support
- **Desktop Platforms**: Native navigation patterns for macOS/Windows
- **Mobile Deep Links**: iOS Universal Links and Android App Links
- **Cross-Platform State**: Synchronized navigation state across devices