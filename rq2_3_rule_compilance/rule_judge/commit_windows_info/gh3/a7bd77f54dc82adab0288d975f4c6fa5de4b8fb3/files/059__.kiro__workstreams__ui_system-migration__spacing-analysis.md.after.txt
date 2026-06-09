# Spacing Analysis and Guidelines

## Current Issues

### 1. Page Padding Inconsistency
- Different screens use different horizontal padding
- Some screens use 16dp, others use 12dp or custom values
- Vertical padding also varies

### 2. Card Padding Issues
- Standard GHCard uses 16dp padding (might be too much for compact content)
- Activity cards with ListTile already have internal padding, creating double padding
- No variant for compact cards with less padding

### 3. Inter-Card Spacing
- Inconsistent spacing between cards (some use 8dp, others 12dp, 16dp, or 20dp)
- No clear principle for when to use which spacing

## Recommended Spacing System

### Base Unit: 4dp Grid
Following Material Design principles, all spacing should be multiples of 4dp:
- 4dp - Tight spacing (rarely used)
- 8dp - Compact spacing (between related items)
- 12dp - Default spacing (between cards)
- 16dp - Comfortable spacing (page margins)
- 20dp - Section spacing (between major sections)
- 24dp - Large spacing (between unrelated sections)
- 32dp - Extra large spacing (major breaks)

### Page Layout Standards

```dart
// Standard page padding
const pageHorizontalPadding = 16.0; // GHTokens.spacing16
const pageVerticalPadding = 16.0;   // GHTokens.spacing16

// Section spacing
const sectionSpacing = 20.0;         // GHTokens.spacing20
const cardSpacing = 12.0;            // GHTokens.spacing12
```

### Card Padding Variants

1. **Standard Card** (GHCard)
   - Padding: 16dp all sides
   - Use for: Primary content, forms, detailed information

2. **Compact Card** (GHCard.compact) - TO BE IMPLEMENTED
   - Padding: 12dp all sides
   - Use for: Lists, activity items, secondary content

3. **Tight Card** (GHCard.tight) - TO BE IMPLEMENTED
   - Padding: 8dp all sides
   - Use for: Dense lists, minimal content

4. **No Padding Card** (GHCard with padding: EdgeInsets.zero)
   - Use for: Content that manages its own padding (like ListTile)

### Specific Recommendations

#### Home Screen
- Page padding: 16dp horizontal (via GHScreenTemplate)
- User card to quick actions: 20dp (section break)
- Quick actions to activity: 20dp (section break)
- Activity items spacing: 8dp (related items)
- Activity to trending: 20dp (section break)

#### Activity Cards
- Use GHCard with zero padding + ListTile
- OR create custom activity card component
- ListTile already provides appropriate internal padding

#### Repository Cards
- Keep current 16dp padding (appropriate for rich content)
- 12dp spacing between repository cards

## Implementation Priority

1. **High Priority**
   - Standardize page padding via GHScreenTemplate
   - Fix activity card double padding
   - Consistent card spacing (12dp default)

2. **Medium Priority**
   - Implement GHCard variants (compact, tight)
   - Create spacing documentation
   - Update all screens to follow guidelines

3. **Low Priority**
   - Fine-tune specific component spacing
   - Add spacing visualization to design tokens screen

## Material Design References
- [Material Design - Layout](https://m3.material.io/foundations/layout/understanding-layout/overview)
- [Material Design - Spacing](https://m3.material.io/foundations/layout/applying-layout/spacing)