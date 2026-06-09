import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';
import '../components/gh_card.dart';
import '../components/gh_button.dart';
import '../layouts/gh_screen_template.dart';
import '../utils/spacing_validator.dart';

/// **DEVELOPER GUIDE** - Comprehensive implementation and maintenance documentation
///
/// This screen provides detailed guidance for developers on:
/// - Proper implementation patterns with code examples
/// - 4dp grid system usage with visual examples
/// - Maintenance procedures for consistency
/// - Code quality standards and validation
/// - Common pitfalls and how to avoid them
class DeveloperGuideScreen extends StatefulWidget {
  const DeveloperGuideScreen({super.key});

  @override
  State<DeveloperGuideScreen> createState() => _DeveloperGuideScreenState();
}

class _DeveloperGuideScreenState extends State<DeveloperGuideScreen> {
  int _selectedSection = 0;

  final List<GuideSection> _sections = [
    GuideSection(
      title: 'Implementation Patterns',
      icon: Icons.code,
      content: ImplementationPatternsContent(),
    ),
    GuideSection(
      title: '4dp Grid System',
      icon: Icons.grid_4x4,
      content: GridSystemContent(),
    ),
    GuideSection(
      title: 'Code Quality Standards',
      icon: Icons.verified,
      content: CodeQualityContent(),
    ),
    GuideSection(
      title: 'Maintenance Procedures',
      icon: Icons.build_circle,
      content: MaintenanceProceduresContent(),
    ),
    GuideSection(
      title: 'Common Pitfalls',
      icon: Icons.warning,
      content: CommonPitfallsContent(),
    ),
    GuideSection(
      title: 'Migration Guide',
      icon: Icons.upload,
      content: MigrationGuideContent(),
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return GHScreenTemplate(
      title: 'Developer Guide',
      body: Row(
        children: [
          // Sidebar navigation
          Container(
            width: 280,
            decoration: BoxDecoration(
              border: Border(
                right: BorderSide(
                  color: Theme.of(
                    context,
                  ).colorScheme.outline.withValues(alpha: 0.2),
                  width: 1,
                ),
              ),
            ),
            child: Column(
              children: [
                Padding(
                  padding: const EdgeInsets.all(GHTokens.spacing16),
                  child: Text(
                    'Developer Guide Sections',
                    style: GHTokens.titleMedium,
                  ),
                ),
                Expanded(
                  child: ListView.builder(
                    itemCount: _sections.length,
                    itemBuilder: (context, index) {
                      final section = _sections[index];
                      final isSelected = index == _selectedSection;

                      return Container(
                        margin: const EdgeInsets.symmetric(
                          horizontal: GHTokens.spacing8,
                          vertical: GHTokens.spacing4,
                        ),
                        decoration: BoxDecoration(
                          color: isSelected
                              ? Theme.of(context).colorScheme.primaryContainer
                              : null,
                          borderRadius: BorderRadius.circular(GHTokens.radius8),
                        ),
                        child: ListTile(
                          leading: Icon(
                            section.icon,
                            color: isSelected
                                ? Theme.of(
                                    context,
                                  ).colorScheme.onPrimaryContainer
                                : Theme.of(
                                    context,
                                  ).colorScheme.onSurfaceVariant,
                          ),
                          title: Text(
                            section.title,
                            style: GHTokens.bodyMedium.copyWith(
                              color: isSelected
                                  ? Theme.of(
                                      context,
                                    ).colorScheme.onPrimaryContainer
                                  : null,
                              fontWeight: isSelected ? FontWeight.w600 : null,
                            ),
                          ),
                          onTap: () {
                            setState(() {
                              _selectedSection = index;
                            });
                          },
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
          ),

          // Content area
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(GHTokens.spacing24),
              child: _sections[_selectedSection].content,
            ),
          ),
        ],
      ),
    );
  }
}

class GuideSection {
  final String title;
  final IconData icon;
  final Widget content;

  GuideSection({
    required this.title,
    required this.icon,
    required this.content,
  });
}

class ImplementationPatternsContent extends StatelessWidget {
  const ImplementationPatternsContent({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Implementation Patterns & Best Practices',
          style: GHTokens.headlineMedium,
        ),
        const SizedBox(height: GHTokens.spacing16),

        Text(
          'Follow these proven patterns to ensure consistent, maintainable, and scalable implementations.',
          style: GHTokens.bodyLarge,
        ),
        const SizedBox(height: GHTokens.spacing24),

        _buildPatternSection(
          context,
          'Screen Structure Pattern',
          'Every screen should use GHScreenTemplate for consistency',
          '''// ✅ CORRECT - Use GHScreenTemplate
return GHScreenTemplate(
  title: 'Screen Title',
  actions: [
    IconButton(
      icon: const Icon(Icons.share),
      onPressed: () => shareContent(),
    ),
  ],
  body: SingleChildScrollView(
    padding: const EdgeInsets.all(GHTokens.spacing16),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Your content here
      ],
    ),
  ),
);

// ❌ INCORRECT - Raw Scaffold
return Scaffold(
  appBar: AppBar(title: Text('Screen Title')),
  body: Container(
    padding: EdgeInsets.all(16), // Magic number!
    child: Column(children: [...]),
  ),
);''',
        ),

        _buildPatternSection(
          context,
          'Spacing Usage Pattern',
          'Always use GHTokens spacing constants, never magic numbers',
          '''// ✅ CORRECT - Use spacing tokens
Column(
  children: [
    Text('Title', style: GHTokens.titleMedium),
    const SizedBox(height: GHTokens.spacing8),
    Text('Subtitle', style: GHTokens.bodyMedium),
    const SizedBox(height: GHTokens.spacing16),
    _buildContent(),
    const SizedBox(height: GHTokens.spacing24),
  ],
)

// ❌ INCORRECT - Magic numbers
Column(
  children: [
    Text('Title'),
    SizedBox(height: 10), // Not on 4dp grid
    Text('Subtitle'),
    SizedBox(height: 18), // Not standardized
    _buildContent(),
    SizedBox(height: 25), // Inconsistent
  ],
)''',
        ),

        _buildPatternSection(
          context,
          'State Management Pattern',
          'Handle loading, empty, and error states consistently',
          '''// ✅ CORRECT - Comprehensive state handling
Widget build(BuildContext context) {
  if (isLoading) {
    return const Center(child: GHLoadingIndicator());
  }
  
  if (hasError) {
    return Center(
      child: GHErrorState(
        title: 'Failed to Load Data',
        message: 'Please check your connection and try again.',
        onRetry: () => _loadData(),
      ),
    );
  }
  
  if (items.isEmpty) {
    return Center(
      child: GHEmptyState(
        icon: Icons.inbox_outlined,
        title: 'No Items Found',
        subtitle: 'Items will appear here when available.',
      ),
    );
  }
  
  return ListView.builder(
    itemCount: items.length,
    itemBuilder: (context, index) => _buildItem(items[index]),
  );
}

// ❌ INCORRECT - Missing state handling
Widget build(BuildContext context) {
  return ListView.builder(
    itemCount: items.length, // Could be null/empty!
    itemBuilder: (context, index) => _buildItem(items[index]),
  );
}''',
        ),

        _buildPatternSection(
          context,
          'Component Usage Pattern',
          'Use appropriate components for their intended purpose',
          '''// ✅ CORRECT - Proper component usage
GHCard(
  onTap: () => _handleTap(),
  child: Padding(
    padding: const EdgeInsets.all(GHTokens.spacing16),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Card Title', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing8),
        Text('Card description', style: GHTokens.bodyMedium),
      ],
    ),
  ),
)

// ❌ INCORRECT - Manual styling
Container(
  decoration: BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(8),
    boxShadow: [BoxShadow(...)], // Inconsistent elevation
  ),
  padding: EdgeInsets.all(16),
  child: Column(...), // No proper gesture handling
)''',
        ),

        _buildPatternSection(
          context,
          'Color Usage Pattern',
          'Use theme colors for consistency and accessibility',
          '''// ✅ CORRECT - Theme-based colors
Container(
  color: Theme.of(context).colorScheme.primary,
  child: Text(
    'Primary Text',
    style: GHTokens.bodyMedium.copyWith(
      color: Theme.of(context).colorScheme.onPrimary,
    ),
  ),
)

// Success state with semantic color
Container(
  decoration: BoxDecoration(
    color: GHTokens.success,
    borderRadius: BorderRadius.circular(GHTokens.radius8),
  ),
  child: Text(
    'Success Message',
    style: GHTokens.bodyMedium.copyWith(color: Colors.white),
  ),
)

// ❌ INCORRECT - Hard-coded colors
Container(
  color: Color(0xFF0969DA), // Hard-coded primary
  child: Text(
    'Primary Text',
    style: TextStyle(color: Colors.white), // Won't adapt to themes
  ),
)''',
        ),
      ],
    );
  }

  Widget _buildPatternSection(
    BuildContext context,
    String title,
    String description,
    String code,
  ) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: GHTokens.titleLarge),
          const SizedBox(height: GHTokens.spacing8),
          Text(description, style: GHTokens.bodyMedium),
          const SizedBox(height: GHTokens.spacing16),

          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(GHTokens.spacing16),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Text(
                code,
                style: GHTokens.bodySmall.copyWith(fontFamily: 'monospace'),
              ),
            ),
          ),
          const SizedBox(height: GHTokens.spacing24),
        ],
      ),
    );
  }
}

class GridSystemContent extends StatelessWidget {
  const GridSystemContent({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '4dp Grid System Implementation Guide',
          style: GHTokens.headlineMedium,
        ),
        const SizedBox(height: GHTokens.spacing16),

        Text(
          'The 4dp grid system ensures visual consistency and proper alignment across all components. '
          'This system is based on Material Design principles and provides optimal touch targets.',
          style: GHTokens.bodyLarge,
        ),
        const SizedBox(height: GHTokens.spacing24),

        _buildGridSection(
          context,
          'Available Spacing Values',
          'Use only these predefined spacing constants:',
          Column(
            children: [
              _buildSpacingRow(
                context,
                'GHTokens.spacing4',
                '4dp',
                'Micro spacing - icon gaps, minimal separations',
                GHTokens.spacing4,
              ),
              _buildSpacingRow(
                context,
                'GHTokens.spacing8',
                '8dp',
                'Small spacing - chip gaps, tight layouts',
                GHTokens.spacing8,
              ),
              _buildSpacingRow(
                context,
                'GHTokens.spacing12',
                '12dp',
                'Medium spacing - compact padding',
                GHTokens.spacing12,
              ),
              _buildSpacingRow(
                context,
                'GHTokens.spacing16',
                '16dp',
                'Standard spacing - default card padding',
                GHTokens.spacing16,
              ),
              _buildSpacingRow(
                context,
                'GHTokens.spacing20',
                '20dp',
                'Large spacing - section margins',
                GHTokens.spacing20,
              ),
              _buildSpacingRow(
                context,
                'GHTokens.spacing24',
                '24dp',
                'XL spacing - screen padding',
                GHTokens.spacing24,
              ),
              _buildSpacingRow(
                context,
                'GHTokens.spacing32',
                '32dp',
                'XXL spacing - major section separations',
                GHTokens.spacing32,
              ),
            ],
          ),
        ),

        _buildGridSection(
          context,
          'Practical Usage Examples',
          'Common spacing patterns with real-world applications:',
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildUsageExample(context, 'Card Layout', '''GHCard(
  child: Padding(
    padding: const EdgeInsets.all(GHTokens.spacing16), // Standard card padding
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Card Title', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing8), // Title to subtitle gap
        Text('Card subtitle', style: GHTokens.bodyMedium),
        const SizedBox(height: GHTokens.spacing16), // Subtitle to content gap
        _buildCardContent(),
      ],
    ),
  ),
)'''),

              _buildUsageExample(context, 'Screen Layout', '''GHScreenTemplate(
  title: 'Screen Title',
  body: SingleChildScrollView(
    padding: const EdgeInsets.all(GHTokens.spacing16), // Screen edge padding
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildHeader(),
        const SizedBox(height: GHTokens.spacing24), // Header to content
        _buildContent(),
        const SizedBox(height: GHTokens.spacing32), // Major section separation
        _buildFooter(),
      ],
    ),
  ),
)'''),

              _buildUsageExample(context, 'Form Layout', '''Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    Text('Form Label', style: GHTokens.labelLarge),
    const SizedBox(height: GHTokens.spacing8), // Label to field
    TextField(...),
    const SizedBox(height: GHTokens.spacing4), // Field to help text
    Text('Help text', style: GHTokens.bodySmall),
    const SizedBox(height: GHTokens.spacing20), // Field group separation
    
    // Next field group
    Text('Next Label', style: GHTokens.labelLarge),
    const SizedBox(height: GHTokens.spacing8),
    TextField(...),
  ],
)'''),
            ],
          ),
        ),

        _buildGridSection(
          context,
          'Validation Tools',
          'Use these utilities to ensure grid compliance:',
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                padding: const EdgeInsets.all(GHTokens.spacing16),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.surfaceContainerHighest,
                  borderRadius: BorderRadius.circular(GHTokens.radius8),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'SpacingValidator Utility',
                      style: GHTokens.titleMedium,
                    ),
                    const SizedBox(height: GHTokens.spacing8),
                    Text(
                      '// Check if a spacing value is valid\n'
                      'final isValid = SpacingValidator.isValidSpacing(16.0); // true\n'
                      'final isInvalid = SpacingValidator.isValidSpacing(15.0); // false\n\n'
                      '// Get nearest valid spacing\n'
                      'final nearest = 28.0.toValidSpacing(); // returns 24.0\n\n'
                      '// Validate and get suggestions\n'
                      'final validation = SpacingValidator.validateSpacing(15.0);\n'
                      'print(validation.suggestion); // "Use 16.0 instead"',
                      style: GHTokens.bodySmall.copyWith(
                        fontFamily: 'monospace',
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: GHTokens.spacing16),

              GHButton(
                label: 'Test Spacing: 28.0 → ${28.0.toValidSpacing()}',
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(
                        'Nearest valid spacing for 28.0 is: ${28.0.toValidSpacing()}dp\n'
                        'Validation: ${SpacingValidator.validateSpacing(28.0)}',
                      ),
                    ),
                  );
                },
              ),
            ],
          ),
        ),

        _buildGridSection(
          context,
          'Common Violations',
          'Avoid these common spacing mistakes:',
          Column(
            children: [
              _buildViolationExample(
                'Magic Numbers',
                'SizedBox(height: 15)',
                'Use GHTokens.spacing16',
              ),
              _buildViolationExample(
                'Inconsistent Padding',
                'padding: EdgeInsets.all(18)',
                'Use GHTokens.spacing16 or spacing20',
              ),
              _buildViolationExample(
                'Non-Grid Values',
                'margin: EdgeInsets.only(top: 22)',
                'Use GHTokens.spacing24',
              ),
              _buildViolationExample(
                'Mixed Units',
                'height: 14, width: 16',
                'Use consistent GHTokens values',
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildGridSection(
    BuildContext context,
    String title,
    String description,
    Widget content,
  ) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: GHTokens.titleLarge),
          const SizedBox(height: GHTokens.spacing8),
          Text(description, style: GHTokens.bodyMedium),
          const SizedBox(height: GHTokens.spacing16),
          content,
        ],
      ),
    );
  }

  Widget _buildSpacingRow(
    BuildContext context,
    String token,
    String value,
    String usage,
    double spacing,
  ) {
    return Padding(
      padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
      child: Row(
        children: [
          Container(
            width: spacing,
            height: 16,
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.primary,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          const SizedBox(width: GHTokens.spacing16),
          Flexible(
            flex: 3,
            child: Text(
              token,
              style: GHTokens.labelLarge.copyWith(fontFamily: 'monospace'),
            ),
          ),
          const SizedBox(width: GHTokens.spacing8),
          Flexible(flex: 1, child: Text(value, style: GHTokens.bodyMedium)),
          const SizedBox(width: GHTokens.spacing8),
          Flexible(flex: 4, child: Text(usage, style: GHTokens.bodySmall)),
        ],
      ),
    );
  }

  Widget _buildUsageExample(BuildContext context, String title, String code) {
    return Container(
      margin: const EdgeInsets.only(bottom: GHTokens.spacing16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing8),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(GHTokens.spacing12),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Text(
                code,
                style: GHTokens.bodySmall.copyWith(fontFamily: 'monospace'),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildViolationExample(
    String violation,
    String incorrect,
    String correct,
  ) {
    return Container(
      margin: const EdgeInsets.only(bottom: GHTokens.spacing8),
      padding: const EdgeInsets.all(GHTokens.spacing12),
      decoration: BoxDecoration(
        border: Border.all(color: GHTokens.error.withValues(alpha: 0.3)),
        borderRadius: BorderRadius.circular(GHTokens.radius8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(violation, style: GHTokens.labelLarge),
          const SizedBox(height: GHTokens.spacing4),
          Row(
            children: [
              const Icon(Icons.close, color: GHTokens.error, size: 16),
              const SizedBox(width: GHTokens.spacing4),
              Expanded(
                child: Text(
                  incorrect,
                  style: GHTokens.bodySmall.copyWith(fontFamily: 'monospace'),
                ),
              ),
            ],
          ),
          const SizedBox(height: GHTokens.spacing4),
          Row(
            children: [
              const Icon(Icons.check, color: GHTokens.success, size: 16),
              const SizedBox(width: GHTokens.spacing4),
              Expanded(
                child: Text(
                  correct,
                  style: GHTokens.bodySmall.copyWith(fontFamily: 'monospace'),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class CodeQualityContent extends StatelessWidget {
  const CodeQualityContent({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Code Quality Standards & Validation',
          style: GHTokens.headlineMedium,
        ),
        const SizedBox(height: GHTokens.spacing16),

        Text(
          'Maintain high code quality through automated checks, consistent patterns, and proper testing.',
          style: GHTokens.bodyLarge,
        ),
        const SizedBox(height: GHTokens.spacing24),

        _buildQualitySection(
          context,
          'Pre-Commit Checklist',
          'Run these commands before every commit:',
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildCommandItem(
                context,
                'dart format .',
                'Format all Dart code consistently',
                'Ensures consistent code formatting across the project',
              ),
              _buildCommandItem(
                context,
                'flutter analyze --fatal-infos --fatal-warnings',
                'Static analysis with zero tolerance',
                'Catches potential issues, ensures no warnings or info messages',
              ),
              _buildCommandItem(
                context,
                'flutter test',
                'Run all unit and widget tests',
                'Verifies all functionality works as expected',
              ),
            ],
          ),
        ),

        _buildQualitySection(
          context,
          'Code Standards',
          'Follow these coding standards for consistency:',
          Column(
            children: [
              _buildStandardItem(
                context,
                'Widget Architecture',
                'Use StatelessWidget when possible, implement const constructors',
                '''// ✅ CORRECT
class MyWidget extends StatelessWidget {
  const MyWidget({super.key, required this.title});
  
  final String title;
  
  @override
  Widget build(BuildContext context) {
    return GHCard(
      child: Text(title, style: GHTokens.titleMedium),
    );
  }
}''',
              ),

              _buildStandardItem(
                context,
                'Error Handling',
                'Always handle async operations and potential failures',
                '''// ✅ CORRECT
Future<void> _loadData() async {
  setState(() => isLoading = true);
  
  try {
    final data = await apiService.fetchData();
    setState(() {
      items = data;
      hasError = false;
    });
  } catch (e) {
    setState(() {
      hasError = true;
      errorMessage = e.toString();
    });
  } finally {
    setState(() => isLoading = false);
  }
}''',
              ),

              _buildStandardItem(
                context,
                'Documentation',
                'Document all public classes and methods with clear examples',
                '''/// **COMPONENT NAME** - Brief description
///
/// This component provides [functionality] and demonstrates:
/// - Key feature 1
/// - Key feature 2
/// - Usage patterns
///
/// **Usage Example:**
/// ```dart
/// ComponentName(
///   parameter: value,
///   onCallback: () => handleAction(),
/// )
/// ```
class ComponentName extends StatelessWidget {
  /// Brief description of the parameter
  final String parameter;
  
  /// Callback description with expected behavior
  final VoidCallback? onCallback;
}''',
              ),
            ],
          ),
        ),

        _buildQualitySection(
          context,
          'Testing Requirements',
          'Ensure comprehensive test coverage:',
          Column(
            children: [
              _buildTestRequirement(
                context,
                'Unit Tests',
                'Test all business logic and utility functions',
                '''// Test utility functions
test('SpacingValidator.isValidSpacing returns correct validation', () {
  expect(SpacingValidator.isValidSpacing(16.0), true);
  expect(SpacingValidator.isValidSpacing(15.0), false);
});

// Test extension methods
test('double.toValidSpacing returns nearest valid spacing', () {
  expect(28.0.toValidSpacing(), 24.0);
  expect(30.0.toValidSpacing(), 32.0);
});''',
              ),

              _buildTestRequirement(
                context,
                'Widget Tests',
                'Test UI components and user interactions',
                '''testWidgets('GHCard displays content and handles tap', (tester) async {
  bool tapped = false;
  
  await tester.pumpWidget(
    MaterialApp(
      home: GHCard(
        onTap: () => tapped = true,
        child: const Text('Card Content'),
      ),
    ),
  );
  
  expect(find.text('Card Content'), findsOneWidget);
  
  await tester.tap(find.byType(GHCard));
  expect(tapped, true);
});''',
              ),

              _buildTestRequirement(
                context,
                'Integration Tests',
                'Test complete user flows and navigation',
                '''testWidgets('Navigation flow works correctly', (tester) async {
  await tester.pumpWidget(const MyApp());
  
  // Navigate to component catalog
  await tester.tap(find.text('Component Catalog'));
  await tester.pumpAndSettle();
  
  expect(find.text('Component Catalog'), findsOneWidget);
  
  // Test back navigation
  await tester.tap(find.byType(BackButton));
  await tester.pumpAndSettle();
  
  expect(find.text('GH3 Design System - UAT'), findsOneWidget);
});''',
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildQualitySection(
    BuildContext context,
    String title,
    String description,
    Widget content,
  ) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: GHTokens.titleLarge),
          const SizedBox(height: GHTokens.spacing8),
          Text(description, style: GHTokens.bodyMedium),
          const SizedBox(height: GHTokens.spacing16),
          content,
        ],
      ),
    );
  }

  Widget _buildCommandItem(
    BuildContext context,
    String command,
    String title,
    String description,
  ) {
    return Container(
      margin: const EdgeInsets.only(bottom: GHTokens.spacing12),
      padding: const EdgeInsets.all(GHTokens.spacing12),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(GHTokens.radius8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                Icons.terminal,
                size: 16,
                color: Theme.of(context).colorScheme.primary,
              ),
              const SizedBox(width: GHTokens.spacing8),
              Expanded(
                child: Text(
                  command,
                  style: GHTokens.titleSmall.copyWith(fontFamily: 'monospace'),
                ),
              ),
            ],
          ),
          const SizedBox(height: GHTokens.spacing4),
          Text(title, style: GHTokens.bodyMedium),
          const SizedBox(height: GHTokens.spacing4),
          Text(description, style: GHTokens.bodySmall),
        ],
      ),
    );
  }

  Widget _buildStandardItem(
    BuildContext context,
    String title,
    String description,
    String code,
  ) {
    return Container(
      margin: const EdgeInsets.only(bottom: GHTokens.spacing16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing4),
          Text(description, style: GHTokens.bodyMedium),
          const SizedBox(height: GHTokens.spacing8),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(GHTokens.spacing12),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Text(
                code,
                style: GHTokens.bodySmall.copyWith(fontFamily: 'monospace'),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTestRequirement(
    BuildContext context,
    String type,
    String description,
    String code,
  ) {
    return Container(
      margin: const EdgeInsets.only(bottom: GHTokens.spacing16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: GHTokens.spacing8,
                  vertical: GHTokens.spacing4,
                ),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.primaryContainer,
                  borderRadius: BorderRadius.circular(GHTokens.radius4),
                ),
                child: Text(
                  type,
                  style: GHTokens.labelMedium.copyWith(
                    color: Theme.of(context).colorScheme.onPrimaryContainer,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: GHTokens.spacing8),
          Text(description, style: GHTokens.bodyMedium),
          const SizedBox(height: GHTokens.spacing8),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(GHTokens.spacing12),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Text(
                code,
                style: GHTokens.bodySmall.copyWith(fontFamily: 'monospace'),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class MaintenanceProceduresContent extends StatelessWidget {
  const MaintenanceProceduresContent({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Maintenance Procedures & Guidelines',
          style: GHTokens.headlineMedium,
        ),
        const SizedBox(height: GHTokens.spacing16),

        Text(
          'Follow these procedures to maintain consistency and quality over time.',
          style: GHTokens.bodyLarge,
        ),
        const SizedBox(height: GHTokens.spacing24),

        _buildProcedureSection(
          context,
          'Adding New Components',
          'Follow this process when creating new components:',
          [
            'Review existing components for similar functionality',
            'Follow the component architecture patterns',
            'Use GHTokens for all styling values',
            'Implement comprehensive error handling',
            'Create corresponding unit and widget tests',
            'Add component to catalog screen for demonstration',
            'Update documentation with usage examples',
            'Run all quality checks before committing',
          ],
        ),

        _buildProcedureSection(
          context,
          'Modifying Existing Components',
          'When updating components, ensure backward compatibility:',
          [
            'Assess impact on existing implementations',
            'Maintain existing API where possible',
            'Add deprecation warnings for removed features',
            'Update all example usages',
            'Test thoroughly across all platforms',
            'Update tests to reflect changes',
            'Document breaking changes clearly',
            'Coordinate with team on migration timeline',
          ],
        ),

        _buildProcedureSection(
          context,
          'Design Token Updates',
          'Changes to design tokens require careful coordination:',
          [
            'Evaluate impact across all components',
            'Test with both light and dark themes',
            'Verify accessibility contrast ratios',
            'Update all affected components simultaneously',
            'Run visual regression tests',
            'Update documentation examples',
            'Coordinate with design team on changes',
            'Plan rollout strategy for large changes',
          ],
        ),

        _buildProcedureSection(
          context,
          'Quality Monitoring',
          'Regular maintenance activities to ensure system health:',
          [
            'Weekly: Run full test suite and analyze failures',
            'Weekly: Review component usage patterns',
            'Monthly: Audit for design token compliance',
            'Monthly: Update dependencies and fix deprecations',
            'Quarterly: Performance analysis and optimization',
            'Quarterly: Accessibility audit with screen readers',
            'Semi-annually: Design system metrics review',
            'Annually: Major version planning and migration',
          ],
        ),

        _buildMaintenanceCard(
          context,
          'Release Checklist',
          'Use this checklist for every release:',
          [
            '□ All tests passing (unit, widget, integration)',
            '□ Code analysis passes with zero warnings',
            '□ All example screens function correctly',
            '□ Theme switching works across all components',
            '□ Accessibility tests pass',
            '□ Performance meets benchmarks',
            '□ Documentation is up to date',
            '□ Breaking changes are documented',
            '□ Migration guide is provided (if needed)',
            '□ Stakeholder approval received',
          ],
        ),

        _buildMaintenanceCard(
          context,
          'Component Health Metrics',
          'Monitor these metrics for component ecosystem health:',
          [
            'Component usage frequency across screens',
            'Number of custom implementations vs design system usage',
            'Performance metrics (build time, runtime performance)',
            'Accessibility compliance scores',
            'Developer satisfaction surveys',
            'Bug reports per component',
            'Time to resolve issues',
            'Test coverage percentages',
          ],
        ),
      ],
    );
  }

  Widget _buildProcedureSection(
    BuildContext context,
    String title,
    String description,
    List<String> steps,
  ) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: GHTokens.titleLarge),
          const SizedBox(height: GHTokens.spacing8),
          Text(description, style: GHTokens.bodyMedium),
          const SizedBox(height: GHTokens.spacing16),

          ...steps.asMap().entries.map((entry) {
            final index = entry.key;
            final step = entry.value;

            return Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    width: 24,
                    height: 24,
                    decoration: BoxDecoration(
                      color: Theme.of(context).colorScheme.primary,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Center(
                      child: Text(
                        '${index + 1}',
                        style: GHTokens.labelSmall.copyWith(
                          color: Theme.of(context).colorScheme.onPrimary,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: GHTokens.spacing12),
                  Expanded(child: Text(step, style: GHTokens.bodyMedium)),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }

  Widget _buildMaintenanceCard(
    BuildContext context,
    String title,
    String description,
    List<String> items,
  ) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: GHTokens.titleLarge),
          const SizedBox(height: GHTokens.spacing8),
          Text(description, style: GHTokens.bodyMedium),
          const SizedBox(height: GHTokens.spacing16),

          ...items.map(
            (item) => Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing4),
              child: Text(item, style: GHTokens.bodyMedium),
            ),
          ),
        ],
      ),
    );
  }
}

class CommonPitfallsContent extends StatelessWidget {
  const CommonPitfallsContent({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Common Pitfalls & How to Avoid Them',
          style: GHTokens.headlineMedium,
        ),
        const SizedBox(height: GHTokens.spacing16),

        Text(
          'Learn from common mistakes to maintain high-quality implementations.',
          style: GHTokens.bodyLarge,
        ),
        const SizedBox(height: GHTokens.spacing24),

        _buildPitfallCard(
          context,
          'Magic Numbers in Spacing',
          'Using hard-coded numbers instead of design tokens',
          'SizedBox(height: 15), padding: EdgeInsets.all(18)',
          'const SizedBox(height: GHTokens.spacing16)\npadding: const EdgeInsets.all(GHTokens.spacing16)',
          'Always use GHTokens spacing constants. They ensure consistency and make global spacing changes easier.',
        ),

        _buildPitfallCard(
          context,
          'Inconsistent State Management',
          'Not handling all possible states (loading, empty, error)',
          '''// Missing loading and error states
Widget build(BuildContext context) {
  return ListView.builder(
    itemCount: items.length,
    itemBuilder: (context, index) => ItemWidget(items[index]),
  );
}''',
          '''// Comprehensive state handling
Widget build(BuildContext context) {
  if (isLoading) return const GHLoadingIndicator();
  if (hasError) return GHErrorState(onRetry: _retry);
  if (items.isEmpty) return const GHEmptyState(...);
  
  return ListView.builder(
    itemCount: items.length,
    itemBuilder: (context, index) => ItemWidget(items[index]),
  );
}''',
          'Always handle loading, empty, and error states to provide better user experience.',
        ),

        _buildPitfallCard(
          context,
          'Hard-coded Colors',
          'Using specific color values instead of theme colors',
          'Container(color: Color(0xFF0969DA))\nText("Hello", style: TextStyle(color: Colors.blue))',
          'Container(color: Theme.of(context).colorScheme.primary)\nText("Hello", style: GHTokens.bodyMedium)',
          'Use theme colors to support light/dark modes and maintain brand consistency.',
        ),

        _buildPitfallCard(
          context,
          'Custom Component Creation',
          'Building custom widgets instead of using design system components',
          '''Container(
  decoration: BoxDecoration(
    borderRadius: BorderRadius.circular(8),
    boxShadow: [BoxShadow(...)],
  ),
  child: InkWell(
    onTap: onTap,
    child: content,
  ),
)''',
          '''GHCard(
  onTap: onTap,
  child: content,
)''',
          'Use existing components when possible. They provide consistent styling and behavior.',
        ),

        _buildPitfallCard(
          context,
          'Missing Accessibility',
          'Not providing proper touch targets and semantic labels',
          '''IconButton(
  iconSize: 16, // Too small
  onPressed: onPressed,
  icon: Icon(Icons.star),
)''',
          '''IconButton(
  iconSize: 24, // Proper size for 48dp touch target
  onPressed: onPressed,
  tooltip: 'Star repository', // Accessibility label
  icon: const Icon(Icons.star),
)''',
          'Ensure minimum 48dp touch targets and provide semantic labels for screen readers.',
        ),

        _buildPitfallCard(
          context,
          'Improper Error Handling',
          'Not handling async operations safely',
          '''Future<void> _loadData() async {
  final data = await api.fetchData(); // Can throw
  setState(() => items = data);
}''',
          '''Future<void> _loadData() async {
  setState(() => isLoading = true);
  
  try {
    final data = await api.fetchData();
    setState(() {
      items = data;
      hasError = false;
    });
  } catch (e) {
    setState(() {
      hasError = true;
      errorMessage = e.toString();
    });
  } finally {
    setState(() => isLoading = false);
  }
}''',
          'Always wrap async operations in try-catch blocks and update UI state appropriately.',
        ),

        _buildPitfallCard(
          context,
          'Inconsistent Typography',
          'Using custom text styles instead of design tokens',
          'Text("Title", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold))',
          'Text("Title", style: GHTokens.titleMedium)',
          'Use GHTokens typography styles to maintain consistency and enable theme changes.',
        ),

        _buildWarningCard(
          context,
          'Code Quality Checks',
          'Always run these checks before committing:',
          [
            'dart format . (fix formatting)',
            'flutter analyze --fatal-infos --fatal-warnings (zero warnings)',
            'flutter test (all tests passing)',
            'Review changed files for design token usage',
            'Test on both light and dark themes',
          ],
        ),
      ],
    );
  }

  Widget _buildPitfallCard(
    BuildContext context,
    String title,
    String description,
    String incorrect,
    String correct,
    String explanation,
  ) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.warning, color: GHTokens.warning, size: 20),
              const SizedBox(width: GHTokens.spacing8),
              Expanded(child: Text(title, style: GHTokens.titleMedium)),
            ],
          ),
          const SizedBox(height: GHTokens.spacing8),
          Text(description, style: GHTokens.bodyMedium),
          const SizedBox(height: GHTokens.spacing16),

          // Incorrect example
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(GHTokens.spacing12),
            decoration: BoxDecoration(
              color: GHTokens.error.withValues(alpha: 0.1),
              border: Border.all(color: GHTokens.error.withValues(alpha: 0.3)),
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    const Icon(Icons.close, color: GHTokens.error, size: 16),
                    const SizedBox(width: GHTokens.spacing4),
                    Text(
                      'Incorrect',
                      style: GHTokens.labelMedium.copyWith(
                        color: GHTokens.error,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: GHTokens.spacing8),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Text(
                    incorrect,
                    style: GHTokens.bodySmall.copyWith(fontFamily: 'monospace'),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: GHTokens.spacing8),

          // Correct example
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(GHTokens.spacing12),
            decoration: BoxDecoration(
              color: GHTokens.success.withValues(alpha: 0.1),
              border: Border.all(
                color: GHTokens.success.withValues(alpha: 0.3),
              ),
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    const Icon(Icons.check, color: GHTokens.success, size: 16),
                    const SizedBox(width: GHTokens.spacing4),
                    Text(
                      'Correct',
                      style: GHTokens.labelMedium.copyWith(
                        color: GHTokens.success,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: GHTokens.spacing8),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Text(
                    correct,
                    style: GHTokens.bodySmall.copyWith(fontFamily: 'monospace'),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: GHTokens.spacing12),
          Container(
            padding: const EdgeInsets.all(GHTokens.spacing12),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Icon(
                  Icons.lightbulb,
                  color: Theme.of(context).colorScheme.primary,
                  size: 16,
                ),
                const SizedBox(width: GHTokens.spacing8),
                Expanded(child: Text(explanation, style: GHTokens.bodySmall)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildWarningCard(
    BuildContext context,
    String title,
    String description,
    List<String> items,
  ) {
    return Container(
      padding: const EdgeInsets.all(GHTokens.spacing16),
      decoration: BoxDecoration(
        color: GHTokens.warning.withValues(alpha: 0.1),
        border: Border.all(color: GHTokens.warning.withValues(alpha: 0.3)),
        borderRadius: BorderRadius.circular(GHTokens.radius8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.priority_high, color: GHTokens.warning, size: 20),
              const SizedBox(width: GHTokens.spacing8),
              Text(title, style: GHTokens.titleMedium),
            ],
          ),
          const SizedBox(height: GHTokens.spacing8),
          Text(description, style: GHTokens.bodyMedium),
          const SizedBox(height: GHTokens.spacing12),

          ...items.map(
            (item) => Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing4),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    '• ',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  Expanded(child: Text(item, style: GHTokens.bodyMedium)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class MigrationGuideContent extends StatelessWidget {
  const MigrationGuideContent({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Migration Guide for Existing Code',
          style: GHTokens.headlineMedium,
        ),
        const SizedBox(height: GHTokens.spacing16),

        Text(
          'Guide for migrating existing code to use the new design system.',
          style: GHTokens.bodyLarge,
        ),
        const SizedBox(height: GHTokens.spacing24),

        _buildMigrationSection(
          context,
          'Migration Strategy',
          'Follow this phased approach for safe migration:',
          [
            'Phase 1: Update design tokens and colors',
            'Phase 2: Replace custom widgets with design system components',
            'Phase 3: Standardize spacing and typography',
            'Phase 4: Implement proper state management',
            'Phase 5: Add comprehensive testing',
          ],
        ),

        _buildMigrationSection(
          context,
          'Color Migration',
          'Replace hard-coded colors with theme colors:',
          [
            'Find: Color(0xFF0969DA) → Replace: Theme.of(context).colorScheme.primary',
            'Find: Colors.green → Replace: GHTokens.success',
            'Find: Colors.red → Replace: GHTokens.error',
            'Find: Colors.grey → Replace: Theme.of(context).colorScheme.onSurfaceVariant',
          ],
        ),

        _buildMigrationSection(
          context,
          'Spacing Migration',
          'Replace magic numbers with spacing tokens:',
          [
            'Find: SizedBox(height: 8) → Replace: SizedBox(height: GHTokens.spacing8)',
            'Find: EdgeInsets.all(16) → Replace: EdgeInsets.all(GHTokens.spacing16)',
            'Find: margin: EdgeInsets.only(top: 24) → Replace: EdgeInsets.only(top: GHTokens.spacing24)',
          ],
        ),

        _buildMigrationExample(
          context,
          'Widget Migration Example',
          'Custom Card → GHCard',
          '''// Before: Custom card implementation
Container(
  margin: EdgeInsets.all(8),
  padding: EdgeInsets.all(16),
  decoration: BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(8),
    boxShadow: [
      BoxShadow(
        offset: Offset(0, 2),
        blurRadius: 4,
        color: Colors.black26,
      ),
    ],
  ),
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text(
        'Card Title',
        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
      ),
      SizedBox(height: 8),
      Text(
        'Card content goes here',
        style: TextStyle(fontSize: 14),
      ),
    ],
  ),
)''',
          '''// After: Using GHCard
GHCard(
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text('Card Title', style: GHTokens.titleMedium),
      const SizedBox(height: GHTokens.spacing8),
      Text('Card content goes here', style: GHTokens.bodyMedium),
    ],
  ),
)''',
        ),

        _buildMigrationChecklist(context, 'Migration Checklist', [
          '□ Replace hard-coded colors with theme colors',
          '□ Update spacing to use GHTokens constants',
          '□ Replace custom widgets with design system components',
          '□ Update typography to use GHTokens text styles',
          '□ Add proper state management (loading, empty, error)',
          '□ Ensure accessibility compliance (48dp touch targets)',
          '□ Add comprehensive tests',
          '□ Run code quality checks',
          '□ Test on both light and dark themes',
          '□ Update documentation',
        ]),
      ],
    );
  }

  Widget _buildMigrationSection(
    BuildContext context,
    String title,
    String description,
    List<String> items,
  ) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: GHTokens.titleLarge),
          const SizedBox(height: GHTokens.spacing8),
          Text(description, style: GHTokens.bodyMedium),
          const SizedBox(height: GHTokens.spacing16),

          ...items.map(
            (item) => Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    width: 6,
                    height: 6,
                    margin: const EdgeInsets.only(top: 6),
                    decoration: BoxDecoration(
                      color: Theme.of(context).colorScheme.primary,
                      shape: BoxShape.circle,
                    ),
                  ),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(child: Text(item, style: GHTokens.bodyMedium)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMigrationExample(
    BuildContext context,
    String title,
    String subtitle,
    String before,
    String after,
  ) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: GHTokens.titleLarge),
          const SizedBox(height: GHTokens.spacing4),
          Text(subtitle, style: GHTokens.bodyMedium),
          const SizedBox(height: GHTokens.spacing16),

          // Before
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(GHTokens.spacing12),
            decoration: BoxDecoration(
              color: GHTokens.error.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Before',
                  style: GHTokens.labelMedium.copyWith(color: GHTokens.error),
                ),
                const SizedBox(height: GHTokens.spacing8),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Text(
                    before,
                    style: GHTokens.bodySmall.copyWith(fontFamily: 'monospace'),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: GHTokens.spacing12),

          // After
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(GHTokens.spacing12),
            decoration: BoxDecoration(
              color: GHTokens.success.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'After',
                  style: GHTokens.labelMedium.copyWith(color: GHTokens.success),
                ),
                const SizedBox(height: GHTokens.spacing8),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Text(
                    after,
                    style: GHTokens.bodySmall.copyWith(fontFamily: 'monospace'),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMigrationChecklist(
    BuildContext context,
    String title,
    List<String> items,
  ) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: GHTokens.titleLarge),
          const SizedBox(height: GHTokens.spacing16),

          ...items.map(
            (item) => Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
              child: Text(item, style: GHTokens.bodyMedium),
            ),
          ),
        ],
      ),
    );
  }
}
