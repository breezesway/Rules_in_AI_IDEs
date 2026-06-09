import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';
import '../components/gh_search_bar.dart';
import '../state_widgets/gh_empty_state.dart';
import '../state_widgets/gh_loading_indicator.dart';

/// A GitHub-styled list template with search, filters, and pull-to-refresh.
///
/// This template provides a standard list layout with optional search bar,
/// filter chips, pull-to-refresh functionality, and infinite scroll support.
/// It handles empty states and loading indicators automatically.
class GHListTemplate extends StatefulWidget {
  /// Hint text for the search bar
  final String? searchHint;

  /// List of filter widgets to display horizontally
  final List<Widget>? filters;

  /// List of child widgets to display in the list
  final List<Widget> children;

  /// Callback for pull-to-refresh functionality
  final Future<void> Function()? onRefresh;

  /// Callback when user scrolls near the bottom for infinite scroll
  final VoidCallback? onLoadMore;

  /// Callback when search text changes
  final Function(String)? onSearch;

  /// Whether the list is currently loading more items
  final bool isLoading;

  /// Custom empty state widget
  final Widget? emptyState;

  /// Whether to show the search bar
  final bool showSearch;

  /// Whether to enable pull-to-refresh
  final bool enableRefresh;

  /// Custom scroll controller
  final ScrollController? scrollController;

  /// Padding around the list content
  final EdgeInsetsGeometry? padding;

  /// Separator builder for list items
  final Widget Function(BuildContext, int)? separatorBuilder;

  const GHListTemplate({
    super.key,
    this.searchHint,
    this.filters,
    required this.children,
    this.onRefresh,
    this.onLoadMore,
    this.onSearch,
    this.isLoading = false,
    this.emptyState,
    this.showSearch = true,
    this.enableRefresh = true,
    this.scrollController,
    this.padding,
    this.separatorBuilder,
  });

  @override
  State<GHListTemplate> createState() => _GHListTemplateState();
}

class _GHListTemplateState extends State<GHListTemplate> {
  late final ScrollController _scrollController;
  final TextEditingController _searchController = TextEditingController();
  bool _isNearBottom = false;

  @override
  void initState() {
    super.initState();
    _scrollController = widget.scrollController ?? ScrollController();
    _scrollController.addListener(_onScroll);
  }

  @override
  void dispose() {
    if (widget.scrollController == null) {
      _scrollController.dispose();
    } else {
      _scrollController.removeListener(_onScroll);
    }
    _searchController.dispose();
    super.dispose();
  }

  void _onScroll() {
    if (_scrollController.position.pixels >=
        _scrollController.position.maxScrollExtent - 200) {
      if (!_isNearBottom) {
        _isNearBottom = true;
        widget.onLoadMore?.call();
        // Reset the flag after a short delay to prevent multiple calls
        Future.delayed(const Duration(milliseconds: 500), () {
          if (mounted) {
            _isNearBottom = false;
          }
        });
      }
    }
  }

  void _onSearchChanged(String query) {
    widget.onSearch?.call(query);
  }

  Widget _buildSearchBar() {
    if (!widget.showSearch || widget.searchHint == null) {
      return const SizedBox.shrink();
    }

    return Padding(
      padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
      child: SizedBox(
        height: GHTokens.minTouchTarget,
        child: GHSearchBar(
          hintText: widget.searchHint!,
          onChanged: _onSearchChanged,
        ),
      ),
    );
  }

  Widget _buildFilterBar() {
    if (widget.filters == null || widget.filters!.isEmpty) {
      return const SizedBox.shrink();
    }

    return Column(
      children: [
        SizedBox(
          height: 48,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: GHTokens.spacing4),
            itemCount: widget.filters!.length,
            separatorBuilder: (context, index) =>
                const SizedBox(width: GHTokens.spacing8),
            itemBuilder: (context, index) => widget.filters![index],
          ),
        ),
        const SizedBox(height: GHTokens.spacing8),
      ],
    );
  }

  Widget _buildEmptyState() {
    return widget.emptyState ??
        const GHEmptyState(
          icon: Icons.inbox_outlined,
          title: 'No items found',
          subtitle: 'Try adjusting your search or filters',
        );
  }

  Widget _buildListContent() {
    if (widget.children.isEmpty && !widget.isLoading) {
      return SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        child: SizedBox(
          height: MediaQuery.of(context).size.height * 0.6,
          child: Center(child: _buildEmptyState()),
        ),
      );
    }

    final itemCount = widget.children.length + (widget.isLoading ? 1 : 0);

    return ListView.separated(
      controller: _scrollController,
      physics: const AlwaysScrollableScrollPhysics(),
      padding: widget.padding ?? EdgeInsets.zero,
      itemCount: itemCount,
      separatorBuilder:
          widget.separatorBuilder ??
          (context, index) => const SizedBox(height: GHTokens.spacing8),
      itemBuilder: (context, index) {
        if (index >= widget.children.length) {
          // Loading indicator at the bottom
          return const Center(
            child: Padding(
              padding: EdgeInsets.all(GHTokens.spacing16),
              child: GHLoadingIndicator(),
            ),
          );
        }
        return widget.children[index];
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _buildSearchBar(),
        _buildFilterBar(),
        Expanded(
          child: widget.enableRefresh && widget.onRefresh != null
              ? RefreshIndicator(
                  onRefresh: widget.onRefresh!,
                  child: _buildListContent(),
                )
              : _buildListContent(),
        ),
      ],
    );
  }
}
