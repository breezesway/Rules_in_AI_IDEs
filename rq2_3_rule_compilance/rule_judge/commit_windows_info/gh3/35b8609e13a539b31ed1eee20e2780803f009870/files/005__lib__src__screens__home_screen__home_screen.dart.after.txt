import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'home_viewmodel.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';
import '../../widgets/user_card/user_card.dart';

class HomeScreen extends StatefulWidget {
  final AuthViewModel authViewModel;
  final HomeViewModel homeViewModel;

  const HomeScreen({
    super.key,
    required this.authViewModel,
    required this.homeViewModel,
  });

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late HomeViewModel _homeViewModel;
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();

    _homeViewModel = widget.homeViewModel;
    _homeViewModel.addListener(_onHomeViewModelChanged);
    _scrollController.addListener(_onScroll);

    // Load initial data
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _homeViewModel.loadFollowingUsers();
    });
  }

  @override
  void dispose() {
    _homeViewModel.removeListener(_onHomeViewModelChanged);
    _scrollController.removeListener(_onScroll);
    _scrollController.dispose();
    _homeViewModel.dispose();
    super.dispose();
  }

  void _onHomeViewModelChanged() {
    if (mounted) {
      setState(() {});
    }
  }

  void _onScroll() {
    if (_scrollController.position.pixels >=
        _scrollController.position.maxScrollExtent - 200) {
      _homeViewModel.loadMoreFollowingUsers();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await widget.authViewModel.logout();
            },
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _homeViewModel.refreshFollowingUsers,
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Welcome Section
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Row(
                    children: [
                      const Icon(
                        Icons.waving_hand,
                        size: 32,
                        color: Colors.amber,
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Welcome back!',
                              style: Theme.of(context).textTheme.titleLarge
                                  ?.copyWith(fontWeight: FontWeight.bold),
                            ),
                            Text(
                              'Discover repositories from people you follow',
                              style: TextStyle(color: Colors.grey[600]),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),

              // Following Section Header
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Following',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  if (_homeViewModel.isLoading && _homeViewModel.isEmpty)
                    const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    ),
                ],
              ),
              const SizedBox(height: 12),

              // Error Message
              if (_homeViewModel.error != null)
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12),
                  margin: const EdgeInsets.only(bottom: 12),
                  decoration: BoxDecoration(
                    color: Colors.red.shade50,
                    border: Border.all(color: Colors.red.shade200),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.error_outline, color: Colors.red.shade600),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          _homeViewModel.error!,
                          style: TextStyle(color: Colors.red.shade700),
                        ),
                      ),
                      TextButton(
                        onPressed: _homeViewModel.clearError,
                        child: const Text('Dismiss'),
                      ),
                    ],
                  ),
                ),

              // Following Users List
              Expanded(child: _buildFollowingList()),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildFollowingList() {
    if (_homeViewModel.isEmpty && !_homeViewModel.isLoading) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.people_outline, size: 64, color: Colors.grey[400]),
            const SizedBox(height: 16),
            Text(
              'No following users found',
              style: Theme.of(
                context,
              ).textTheme.titleMedium?.copyWith(color: Colors.grey[600]),
            ),
            const SizedBox(height: 8),
            Text(
              'Start following users on GitHub to see them here',
              style: TextStyle(color: Colors.grey[500]),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: _homeViewModel.loadFollowingUsers,
              icon: const Icon(Icons.refresh),
              label: const Text('Retry'),
            ),
          ],
        ),
      );
    }

    final users = _homeViewModel.followingUsers;

    return ListView.builder(
      controller: _scrollController,
      itemCount: users.length + (_homeViewModel.isLoading ? 1 : 0),
      itemBuilder: (context, index) {
        // Loading indicator at the end
        if (index >= users.length) {
          return const Padding(
            padding: EdgeInsets.all(16.0),
            child: Center(child: CircularProgressIndicator()),
          );
        }

        final user = users[index];

        // Use UserCard widget with GraphQL fragment data
        return UserCard.fromFragment(
          user,
          onTap: () {
            context.push('/${user.login}');
          },
        );
      },
    );
  }
}
