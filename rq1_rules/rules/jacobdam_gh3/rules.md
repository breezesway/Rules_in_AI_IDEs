# Development Rules & Guidelines

This document contains **mandatory** rules that must be followed when working on this project. These rules ensure code quality, maintainability, and architectural consistency.

## Rule 1: Widget-GraphQL Separation Pattern

### 🚨 CRITICAL RULE: Widgets MUST NOT directly receive GraphQL generated classes as parameters

**Problem**: Directly passing GraphQL generated classes to widgets creates tight coupling between UI components and GraphQL implementation details, making widgets harder to test, reuse, and maintain.

**Solution**: Use explicit fields with factory constructors for GraphQL integration.

### ✅ Correct Implementation


```dart
// ✅ GOOD: Widget with explicit fields
class UserCard extends StatelessWidget {
  final String login;
  final String? name;
  final String? bio;
  final String avatarUrl;
  final int repositoryCount;
  final int followerCount;
  final VoidCallback? onTap;

  const UserCard({
    super.key,
    required this.login,
    this.name,
    this.bio,
    required this.avatarUrl,
    required this.repositoryCount,
    required this.followerCount,
    this.onTap,
  });

  // Factory constructor for GraphQL integration
  factory UserCard.fromFragment(
    GUserCardFragment fragment, {
    Key? key,
    VoidCallback? onTap,
  }) {
    return UserCard(
      key: key,
      login: fragment.login,
      name: fragment.name,
      bio: fragment.bio,
      avatarUrl: fragment.avatarUrl.value,
      repositoryCount: fragment.repositories.totalCount,
      followerCount: fragment.followers.totalCount,
      onTap: onTap,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: CircleAvatar(
          backgroundImage: NetworkImage(avatarUrl),
        ),
        title: Text(name ?? login),
        subtitle: Text('@$login'),
        onTap: onTap,
      ),
    );
  }
}
```

### ❌ Incorrect Implementation

```dart
// ❌ BAD: Widget directly using GraphQL generated class
class UserCard extends StatelessWidget {
  final GUserCardFragment user; // ❌ Direct GraphQL dependency
  final VoidCallback? onTap;

  const UserCard({super.key, required this.user, this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: CircleAvatar(
          backgroundImage: NetworkImage(user.avatarUrl.value), // ❌ GraphQL-specific API
        ),
        title: Text(user.name ?? user.login),
        subtitle: Text('@${user.login}'),
        onTap: onTap,
      ),
    );
  }
}
```

### Pattern Benefits

1. **Testability**: Widgets can be tested with simple mock data without GraphQL setup
2. **Reusability**: Widgets can be used with different data sources (REST APIs, local data, etc.)
3. **Maintainability**: Changes to GraphQL schema don't break widget implementations
4. **Type Safety**: Explicit fields provide clear contracts and better IDE support
5. **Performance**: No unnecessary GraphQL object passing through widget tree

### Usage Examples

```dart
// Usage with GraphQL data
final userFragment = getUserCardFragment();
final widget = UserCard.fromFragment(userFragment, onTap: () => handleTap());

// Usage in tests with mock data
final widget = UserCard(
  login: 'testuser',
  name: 'Test User',
  bio: 'Test bio',
  avatarUrl: 'https://example.com/avatar.jpg',
  repositoryCount: 42,
  followerCount: 123,
  onTap: () => handleTap(),
);
```

### Enforcement Guidelines

#### Code Review Checklist
- [ ] Widget constructors use explicit primitive/simple types
- [ ] No direct GraphQL generated class parameters in widget constructors
- [ ] Factory constructor `fromFragment()` exists for GraphQL integration
- [ ] Factory constructor maps GraphQL fields to explicit parameters
- [ ] Widget tests use direct constructor, not `fromFragment()`

#### Refactoring Steps

When you find widgets that violate this rule:

1. **Identify GraphQL Dependencies**: Look for parameters with types starting with `G` (e.g., `GUserCardFragment`)

2. **Extract Required Fields**: Analyze the `build()` method to see which fields are actually needed

3. **Create Explicit Parameters**: Replace GraphQL parameter with individual typed fields

4. **Add Factory Constructor**: Create `fromFragment()` method to map GraphQL data to explicit fields

5. **Update Usage**: Replace direct constructor calls with `fromFragment()` where GraphQL data is used

6. **Update Tests**: Use direct constructor in tests for better isolation

### Testing Pattern

```dart
// Test the widget directly without GraphQL dependencies
testWidgets('should display user information correctly', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: UserCard(
          login: 'testuser',
          name: 'Test User',
          bio: 'Test bio',
          avatarUrl: 'https://example.com/avatar.jpg',
          repositoryCount: 42,
          followerCount: 123,
        ),
      ),
    ),
  );

  expect(find.text('Test User'), findsOneWidget);
  expect(find.text('@testuser'), findsOneWidget);
  expect(find.text('Test bio'), findsOneWidget);
});
```

## Rule Violations

**Any PR that introduces widgets directly using GraphQL generated classes will be rejected.**

If you find existing code that violates this rule, it should be refactored as part of your changes or in a separate refactoring PR.

## Questions?

If you're unsure about how to apply this rule to a specific case:

1. Check existing widget implementations (`lib/src/widgets/`) for examples
2. Look at the pattern documentation in `structure.md`
3. Ask for clarification in code review

---

*This rule is based on lessons learned from maintaining large Flutter applications and ensures our codebase remains scalable and maintainable.*