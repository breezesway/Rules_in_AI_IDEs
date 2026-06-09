# Demo-Ready Application Design

## Overview

This design delivers a polished, stakeholder-ready demonstration that showcases all UI system improvements, validates standards compliance, and provides a professional presentation of the complete GitHub mobile experience. The demo serves as both a validation tool and a reference implementation.

## Demo Application Architecture

### Enhanced UAT Navigation Structure

```dart
class DemoNavigationService {
  static final Map<String, DemoSection> sections = {
    'improvements': DemoSection(
      title: 'Key Improvements',
      description: 'Before/after comparisons of major changes',
      routes: [
        DemoRoute('navigation-comparison', 'Navigation Improvements'),
        DemoRoute('spacing-comparison', 'Spacing Standardization'),
        DemoRoute('component-showcase', 'New Components'),
      ],
    ),
    'examples': DemoSection(
      title: 'Example Screens',
      description: 'Complete screen implementations',
      routes: [
        DemoRoute('home-example', 'Home Screen'),
        DemoRoute('user-profile-example', 'User Profile'),
        DemoRoute('repository-example', 'Repository Details'),
        DemoRoute('issues-example', 'Issues & Pull Requests'),
      ],
    ),
    'components': DemoSection(
      title: 'Component Library',
      description: 'Interactive component catalog',
      routes: [
        DemoRoute('design-tokens', 'Design Tokens'),
        DemoRoute('core-components', 'Core Components'),
        DemoRoute('github-widgets', 'GitHub Widgets'),
        DemoRoute('state-components', 'State Management'),
      ],
    ),
  };
}
```

### Before/After Comparison Framework

```dart
class ComparisonScreen extends StatefulWidget {
  final String title;
  final Widget beforeWidget;
  final Widget afterWidget;
  final String beforeDescription;
  final String afterDescription;
  final List<ImprovementHighlight> highlights;

  const ComparisonScreen({
    super.key,
    required this.title,
    required this.beforeWidget,
    required this.afterWidget,
    required this.beforeDescription,
    required this.afterDescription,
    required this.highlights,
  });

  @override
  State<ComparisonScreen> createState() => _ComparisonScreenState();
}

class _ComparisonScreenState extends State<ComparisonScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  
  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return GHScreenTemplate(
      title: widget.title,
      body: Column(
        children: [
          // Improvement highlights
          _buildHighlightsSection(),
          const SizedBox(height: GHTokens.spacing20),
          
          // Before/After tabs
          TabBar(
            controller: _tabController,
            tabs: const [
              Tab(text: 'Before'),
              Tab(text: 'After'),
            ],
          ),
          
          Expanded(
            child: TabBarView(
              controller: _tabController,
              children: [
                _buildBeforeView(),
                _buildAfterView(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHighlightsSection() {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Key Improvements',
            style: GHTokens.titleLarge,
          ),
          const SizedBox(height: GHTokens.spacing12),
          
          ...widget.highlights.map((highlight) => Padding(
            padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Icon(
                  Icons.check_circle,
                  size: 20,
                  color: GHTokens.success,
                ),
                const SizedBox(width: GHTokens.spacing8),
                Expanded(
                  child: Text(
                    highlight.description,
                    style: GHTokens.bodyMedium,
                  ),
                ),
              ],
            ),
          )),
        ],
      ),
    );
  }
}

class ImprovementHighlight {
  final String description;
  final String? details;

  const ImprovementHighlight({
    required this.description,
    this.details,
  });
}
```

## Specific Comparison Implementations

### Navigation Improvement Demo

```dart
class NavigationComparisonScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ComparisonScreen(
      title: 'Navigation Improvements',
      beforeDescription: 'Tab-based navigation with duplicate titles',
      afterDescription: 'Action-based push navigation with scrolling app bar',
      highlights: [
        ImprovementHighlight(
          description: 'Eliminated tab navigation in favor of action lists',
        ),
        ImprovementHighlight(
          description: 'Implemented Material Design scrolling app bar',
        ),
        ImprovementHighlight(
          description: 'Removed duplicate title display',
        ),
        ImprovementHighlight(
          description: 'Consistent push navigation throughout app',
        ),
      ],
      beforeWidget: _buildTabBasedProfile(),
      afterWidget: _buildActionBasedProfile(),
    );
  }

  Widget _buildTabBasedProfile() {
    return MockScreen(
      title: 'The Octocat',
      body: Column(
        children: [
          // User card with title
          _buildUserCardWithTitle(),
          
          // Tab bar (the old way)
          Container(
            height: 48,
            color: Colors.grey[100],
            child: Row(
              children: [
                _buildTab('Repositories', true),
                _buildTab('Starred', false),
                _buildTab('Organizations', false),
              ],
            ),
          ),
          
          // Content area
          Expanded(
            child: Center(
              child: Text('Tab content would be here'),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActionBasedProfile() {
    return MockScreen(
      title: '', // No title initially
      body: CustomScrollView(
        slivers: [
          // Scrolling app bar
          SliverAppBar(
            title: const Text('The Octocat'),
            expandedHeight: 100,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              title: const Text('The Octocat'),
              collapseMode: CollapseMode.fade,
            ),
          ),
          
          SliverToBoxAdapter(
            child: Column(
              children: [
                // User card without title
                _buildUserCardWithoutTitle(),
                const SizedBox(height: GHTokens.spacing20),
                
                // Action list
                _buildActionList(),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

### Spacing Comparison Demo

```dart
class SpacingComparisonScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ComparisonScreen(
      title: 'Spacing Standardization',
      beforeDescription: 'Inconsistent spacing with varying measurements',
      afterDescription: 'Consistent 4dp grid system throughout',
      highlights: [
        ImprovementHighlight(
          description: 'Standardized all spacing to 4dp grid system',
        ),
        ImprovementHighlight(
          description: 'Fixed activity card double padding issues',
        ),
        ImprovementHighlight(
          description: 'Consistent 16dp page margins across all screens',
        ),
        ImprovementHighlight(
          description: 'Professional visual hierarchy with proper spacing',
        ),
      ],
      beforeWidget: _buildInconsistentSpacing(),
      afterWidget: _buildConsistentSpacing(),
    );
  }

  Widget _buildInconsistentSpacing() {
    return MockScreen(
      title: 'Home',
      body: Column(
        children: [
          _buildUserCard(),
          const SizedBox(height: 24), // Wrong spacing
          _buildQuickActions(),
          const SizedBox(height: 16), // Wrong spacing
          _buildActivityWithDoublepadding(),
          const SizedBox(height: 32), // Wrong spacing
          _buildTrending(),
        ],
      ),
    );
  }

  Widget _buildConsistentSpacing() {
    return MockScreen(
      title: 'Home',
      body: Column(
        children: [
          _buildUserCard(),
          const SizedBox(height: GHTokens.spacing20), // Correct
          _buildQuickActions(),
          const SizedBox(height: GHTokens.spacing20), // Correct
          _buildActivityWithCorrectPadding(),
          const SizedBox(height: GHTokens.spacing20), // Correct
          _buildTrending(),
        ],
      ),
    );
  }
}
```

## Interactive Demo Features

### Measurement Overlay

```dart
class MeasurementOverlay extends StatelessWidget {
  final Widget child;
  final bool showMeasurements;

  const MeasurementOverlay({
    super.key,
    required this.child,
    this.showMeasurements = false,
  });

  @override
  Widget build(BuildContext context) {
    if (!showMeasurements) return child;

    return Stack(
      children: [
        child,
        _buildMeasurementLabels(),
      ],
    );
  }

  Widget _buildMeasurementLabels() {
    return Positioned.fill(
      child: CustomPaint(
        painter: SpacingMeasurementPainter(),
      ),
    );
  }
}

class SpacingMeasurementPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.red.withOpacity(0.7)
      ..strokeWidth = 1.0;

    final textPainter = TextPainter(
      textDirection: TextDirection.ltr,
    );

    // Draw measurement lines and labels for key spacing
    _drawMeasurement(canvas, textPainter, 0, 100, '20dp');
    _drawMeasurement(canvas, textPainter, 100, 150, '8dp');
    // Add more measurements as needed
  }

  void _drawMeasurement(
    Canvas canvas,
    TextPainter textPainter,
    double start,
    double end,
    String label,
  ) {
    // Draw measurement line and label
    canvas.drawLine(
      Offset(10, start),
      Offset(10, end),
      Paint()..color = Colors.red,
    );

    textPainter.text = TextSpan(
      text: label,
      style: const TextStyle(
        color: Colors.red,
        fontSize: 12,
        fontWeight: FontWeight.bold,
      ),
    );
    textPainter.layout();
    textPainter.paint(canvas, Offset(15, (start + end) / 2 - 6));
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
```

### Interactive Component Showcase

```dart
class InteractiveComponentShowcase extends StatefulWidget {
  @override
  State<InteractiveComponentShowcase> createState() =>
      _InteractiveComponentShowcaseState();
}

class _InteractiveComponentShowcaseState
    extends State<InteractiveComponentShowcase> {
  bool _showEmptyState = false;
  bool _showErrorState = false;
  bool _showLoadingState = false;

  @override
  Widget build(BuildContext context) {
    return GHScreenTemplate(
      title: 'Interactive Showcase',
      body: Column(
        children: [
          // Controls
          GHCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('State Controls', style: GHTokens.titleMedium),
                const SizedBox(height: GHTokens.spacing12),
                
                Wrap(
                  spacing: GHTokens.spacing8,
                  children: [
                    GHChip(
                      label: 'Empty State',
                      isSelected: _showEmptyState,
                      onTap: () => setState(() => _showEmptyState = !_showEmptyState),
                    ),
                    GHChip(
                      label: 'Error State',
                      isSelected: _showErrorState,
                      onTap: () => setState(() => _showErrorState = !_showErrorState),
                    ),
                    GHChip(
                      label: 'Loading State',
                      isSelected: _showLoadingState,
                      onTap: () => setState(() => _showLoadingState = !_showLoadingState),
                    ),
                  ],
                ),
              ],
            ),
          ),
          
          const SizedBox(height: GHTokens.spacing20),
          
          // Dynamic content area
          Expanded(
            child: _buildDynamicContent(),
          ),
        ],
      ),
    );
  }

  Widget _buildDynamicContent() {
    if (_showLoadingState) {
      return const GHLoadingIndicator(
        message: 'Loading example content...',
      );
    }
    
    if (_showErrorState) {
      return GHErrorState(
        title: 'Example Error',
        message: 'This is how errors are displayed in the system.',
        onRetry: () => setState(() => _showErrorState = false),
      );
    }
    
    if (_showEmptyState) {
      return GHEmptyState(
        icon: Icons.inbox,
        title: 'No Content',
        subtitle: 'This is how empty states appear in the system.',
        action: GHButton(
          label: 'Add Content',
          onPressed: () => setState(() => _showEmptyState = false),
        ),
      );
    }
    
    return _buildNormalContent();
  }

  Widget _buildNormalContent() {
    return ListView.separated(
      itemCount: 5,
      separatorBuilder: (context, index) => 
        const SizedBox(height: GHTokens.spacing12),
      itemBuilder: (context, index) => GHCard(
        child: ListTile(
          title: Text('Example Item ${index + 1}'),
          subtitle: Text('This shows normal content state'),
          trailing: const Icon(Icons.chevron_right),
        ),
      ),
    );
  }
}
```

## Documentation Integration

### Standards Compliance Checker

```dart
class ComplianceChecker {
  static List<ComplianceResult> checkScreen(Widget screen) {
    final results = <ComplianceResult>[];
    
    // Check spacing compliance
    results.addAll(_checkSpacingCompliance(screen));
    
    // Check component usage
    results.addAll(_checkComponentUsage(screen));
    
    // Check accessibility
    results.addAll(_checkAccessibility(screen));
    
    return results;
  }
  
  static List<ComplianceResult> _checkSpacingCompliance(Widget screen) {
    // Implementation to validate spacing follows 4dp grid
    return [];
  }
}

class ComplianceResult {
  final String rule;
  final bool isCompliant;
  final String? issue;
  final String? suggestion;

  const ComplianceResult({
    required this.rule,
    required this.isCompliant,
    this.issue,
    this.suggestion,
  });
}
```

This design ensures the demo application provides comprehensive validation of all improvements while serving as an effective stakeholder presentation tool.