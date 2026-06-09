# Custom Nuxt Data Fetching ESLint Rule

## Rule: `nuxt-custom/nuxt-data-fetching`

This ESLint rule enforces proper Nuxt data fetching patterns to ensure optimal performance and consistency across your application.

## What it enforces

### 1. Use `useFetch()` in script setup root level

- **Problem**: Using native `fetch()` or `$fetch()` in `<script setup>` root level
- **Solution**: Replace with `useFetch()` or `useAsyncData()`
- **Auto-fix**: ⚠️ **Partial** - `fetch()` auto-fixes, `$fetch()` does NOT (different return types)

```vue
<!-- ❌ Bad -->
<script setup>
const data1 = await fetch("/api/users"); // Auto-fixable to useFetch()
const data2 = await $fetch("/api/users"); // ERROR: Manual fix required
</script>

<!-- ✅ Good -->
<script setup>
const { data: users } = await useFetch("/api/users");
</script>
```

### 2. Use `$fetch()` in functions, event handlers, and lifecycle hooks

- **Problem**: Using native `fetch()` in reactive contexts
- **Solution**: Replace with `$fetch()`
- **Auto-fix**: ✅ Yes

```vue
<!-- ❌ Bad -->
<script setup>
async function createUser(user) {
  const result = await fetch("/api/users", {
    method: "POST",
    body: JSON.stringify(user),
  });
}

const onClick = async () => {
  await fetch("/api/action");
};

onMounted(async () => {
  await fetch("/api/mount-data");
});
</script>

<!-- ✅ Good -->
<script setup>
async function createUser(user) {
  const result = await $fetch("/api/users", {
    method: "POST",
    body: user, // $fetch handles JSON serialization
  });
}

const onClick = async () => {
  await $fetch("/api/action");
};

onMounted(async () => {
  await $fetch("/api/mount-data");
});
</script>
```

### 3. Prefer `useFetch()` over `useAsyncData()` for simple HTTP requests

- **Problem**: Using `useAsyncData()` with simple `$fetch()` calls
- **Solution**: Use `useFetch()` directly
- **Auto-fix**: 💡 Suggestion only

```vue
<!-- ❌ Less optimal -->
<script setup>
const { data } = await useAsyncData("users", () => $fetch("/api/users"));
</script>

<!-- ✅ Better -->
<script setup>
const { data } = await useFetch("/api/users");
</script>
```

### 4. Consider page-level data fetching

- **Problem**: Fetching data in components instead of pages
- **Solution**: Move data fetching to page level and pass via props
- **Auto-fix**: 💡 Suggestion only (architectural decision)

## Configuration

Enable the rule in your `eslint.config.mjs`:

```javascript
export default withNuxt({
  plugins: {
    "nuxt-custom": customRules,
  },
  rules: {
    "nuxt-custom/nuxt-data-fetching": "warn",
  },
});
```

### Options

```javascript
rules: {
  'nuxt-custom/nuxt-data-fetching': ['warn', {
    enforcePageLevelFetching: true // Default: true
  }]
}
```

- `enforcePageLevelFetching`: When `false`, disables suggestions about moving data fetching to page level

## Benefits

1. **Performance**: Ensures data is fetched at the optimal time (SSR vs CSR)
2. **Consistency**: Enforces consistent patterns across your codebase
3. **Type Safety**: `useFetch()` provides better TypeScript integration
4. **Error Handling**: Nuxt composables provide built-in error handling
5. **Caching**: Automatic request deduplication and caching

## Examples

### Complete Example

```vue
<script setup lang="ts">
// ✅ Initial data loading
const { data: users, status, error, refresh } = await useFetch("/api/users");

// ✅ Reactive operations
async function createUser(newUser: User) {
  const createdUser = await $fetch("/api/users", {
    method: "POST",
    body: newUser,
  });

  // Refresh the users list
  await refresh();
}

// ✅ Event handlers
const onDelete = async (id: string) => {
  await $fetch(`/api/users/${id}`, { method: "DELETE" });
  await refresh();
};
</script>
```
