<script setup>
// no need to manually register playground pages, they are automatically registered
const router = useRouter();
const routes = router.getRoutes();
const items = routes.filter((route) => route.path.startsWith("/playground/"));

const getItemName = (path) => {
  return path.split("/").pop();
};

const search = ref("");
const filteredItems = computed(() => {
  const filtered = items.filter((item) =>
    getItemName(item.path).toLowerCase().includes(search.value.toLowerCase())
  );

  return [...filtered].sort((a, b) => {
    return getItemName(a.path).localeCompare(getItemName(b.path));
  });
});
</script>
<template>
  <div>
    <div class="mb-4">
      <h1 class="text-3xl font-bold tracking-tight">Playground</h1>
      <p class="text-muted-foreground mt-2">
        Explore and test different features and components
      </p>
      <div class="flex items-center gap-2 mt-4">
        <Input v-model="search" placeholder="Search" />
      </div>
    </div>

    <div class="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
      <Card
        v-for="item in filteredItems"
        :key="item.name"
        class="hover:shadow-md transition-shadow"
      >
        <CardHeader class="pb-3">
          <CardTitle class="text-lg">
            <NuxtLink
              :to="item.path"
              class="text-primary hover:text-primary/80 transition-colors"
            >
              {{ getItemName(item.path) }}
            </NuxtLink>
          </CardTitle>
          <CardDescription class="text-sm font-mono">
            {{ item.path }}
          </CardDescription>
        </CardHeader>
      </Card>
    </div>
  </div>
</template>
