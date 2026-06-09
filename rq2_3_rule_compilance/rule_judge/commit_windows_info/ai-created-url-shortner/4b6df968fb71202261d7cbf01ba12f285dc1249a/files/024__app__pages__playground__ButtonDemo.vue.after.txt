<script setup lang="ts">
definePageMeta({
  title: "Button Demo",
  description: "Showcase of all button variants and sizes",
});

const isLoading = ref(false);

const handleAsyncAction = () => {
  isLoading.value = true;
  setTimeout(() => {
    isLoading.value = false;
  }, 2000);
};
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <!-- Header -->
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Button</h1>
      <p class="text-muted-foreground mt-2">
        Displays a button or a component that looks like a button.
      </p>
    </div>

    <!-- Variants -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Variants</h2>
      <div class="flex flex-wrap gap-4">
        <Button>Default</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="destructive">Destructive</Button>
        <Button variant="outline">Outline</Button>
        <Button variant="ghost">Ghost</Button>
        <Button variant="link">Link</Button>
      </div>
    </div>

    <!-- Sizes -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Sizes</h2>
      <div class="flex flex-wrap items-center gap-4">
        <Button size="sm">Small</Button>
        <Button size="default">Default</Button>
        <Button size="lg">Large</Button>
        <Button size="icon">
          <svg
            class="h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            />
          </svg>
        </Button>
      </div>
    </div>

    <!-- With Icons -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">With Icons</h2>
      <div class="flex flex-wrap gap-4">
        <Button>
          <svg
            class="mr-2 h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
            />
          </svg>
          Login with Email
        </Button>
        <Button variant="outline">
          Download
          <svg
            class="ml-2 h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
            />
          </svg>
        </Button>
      </div>
    </div>

    <!-- Loading State -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Loading State</h2>
      <div class="flex flex-wrap gap-4">
        <Button :disabled="isLoading" @click="handleAsyncAction">
          <svg
            v-if="isLoading"
            class="mr-2 h-4 w-4 animate-spin"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            />
            <path
              class="opacity-75"
              fill="currentColor"
              d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          {{ isLoading ? "Please wait..." : "Async Action" }}
        </Button>
      </div>
    </div>

    <!-- Disabled State -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Disabled State</h2>
      <div class="flex flex-wrap gap-4">
        <Button disabled>Disabled</Button>
        <Button variant="secondary" disabled>Disabled Secondary</Button>
        <Button variant="outline" disabled>Disabled Outline</Button>
      </div>
    </div>

    <!-- As Link -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">As Link</h2>
      <div class="flex flex-wrap gap-4">
        <Button as-child>
          <NuxtLink to="/playground">Go to Playground</NuxtLink>
        </Button>
        <Button variant="outline" as-child>
          <a href="https://shadcn-vue.com" target="_blank">External Link</a>
        </Button>
      </div>
    </div>
  </div>
</template>
