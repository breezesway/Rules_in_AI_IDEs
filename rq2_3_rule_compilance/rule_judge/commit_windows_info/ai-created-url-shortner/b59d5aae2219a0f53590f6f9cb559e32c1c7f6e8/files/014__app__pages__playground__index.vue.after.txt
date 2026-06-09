<script setup>
// no need to manually register playground pages, they are automatically registered
const router = useRouter();
const routes = router.getRoutes();
const items = routes.filter((route) => route.path.startsWith("/playground/"));

const getItemName = (path) => {
  return path.split("/").pop();
};
</script>
<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-4xl mx-auto">
      <div class="mb-8">
        <h1 class="text-3xl font-bold tracking-tight">Playground</h1>
        <p class="text-muted-foreground mt-2">
          Explore and test different features and components
        </p>
      </div>

      <div class="grid gap-4">
        <Card
          v-for="item in items"
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
  </div>
</template>
