# Material Design Patterns for gh3

## Scrolling App Bar Pattern (User Details Screen)

### Current Implementation
- Fixed app bar with title "The Octocat"
- User card in body also shows "The Octocat" as the main title
- Results in duplicate title display

### Desired Implementation
Following Material Design's large title pattern:

1. **Initial State**
   - App bar title is transparent or shows minimal info
   - Large title is displayed in the scrollable content area
   - User sees the title once in the body card

2. **Scrolling Behavior**
   - As user scrolls up and the body title moves off-screen
   - App bar title fades in smoothly
   - Ensures title is always visible to maintain context

3. **Technical Approach**
   ```dart
   CustomScrollView(
     slivers: [
       SliverAppBar(
         expandedHeight: 200.0,
         floating: false,
         pinned: true,
         flexibleSpace: FlexibleSpaceBar(
           title: Text('The Octocat'),
           fadeInThreshold: 0.7,  // Control when title appears
           fadeOutThreshold: 0.3, // Control when title disappears
         ),
       ),
       SliverList(
         // User details content
       ),
     ],
   )
   ```

4. **Alternative Approach with ScrollController**
   - Monitor scroll position
   - Animate app bar title opacity based on scroll offset
   - More control over transition timing

### Benefits
- Reduces visual redundancy
- Maintains context during scrolling
- Follows Material Design best practices
- Provides smooth, professional user experience

### References
- [Material Design - Top App Bar](https://m3.material.io/components/top-app-bar/overview)
- [Flutter SliverAppBar Documentation](https://api.flutter.dev/flutter/material/SliverAppBar-class.html)