<script setup lang="ts">
definePageMeta({
  title: "Badge Demo",
  description: "Small status indicator for UI elements",
});
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Badge</h1>
      <p class="text-muted-foreground mt-2">
        Displays a badge or a component that looks like a badge.
      </p>
    </div>

    <!-- Default Badges -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Default Badges</h2>
      <div class="flex flex-wrap gap-4">
        <Badge>Default</Badge>
        <Badge variant="secondary">Secondary</Badge>
        <Badge variant="destructive">Destructive</Badge>
        <Badge variant="outline">Outline</Badge>
      </div>
    </div>

    <!-- Status Badges -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Status Badges</h2>
      <div class="flex flex-wrap gap-4">
        <Badge
          class="bg-green-100 text-green-800 hover:bg-green-100 dark:bg-green-900 dark:text-green-300"
        >
          Active
        </Badge>
        <Badge
          class="bg-blue-100 text-blue-800 hover:bg-blue-100 dark:bg-blue-900 dark:text-blue-300"
        >
          Pending
        </Badge>
        <Badge
          class="bg-yellow-100 text-yellow-800 hover:bg-yellow-100 dark:bg-yellow-900 dark:text-yellow-300"
        >
          Warning
        </Badge>
        <Badge variant="destructive"> Error </Badge>
      </div>
    </div>

    <!-- Notification Badges -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Notification Badges</h2>
      <div class="flex flex-wrap gap-6">
        <div class="flex items-center gap-2">
          <span>Messages</span>
          <Badge>3</Badge>
        </div>
        <div class="flex items-center gap-2">
          <span>Notifications</span>
          <Badge class="bg-red-500 text-white hover:bg-red-500">12</Badge>
        </div>
        <div class="flex items-center gap-2">
          <span>Updates</span>
          <Badge variant="outline">New</Badge>
        </div>
      </div>
    </div>

    <!-- Badge with Icons -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Badge with Icons</h2>
      <div class="flex flex-wrap gap-4">
        <Badge class="gap-1">
          <svg
            class="h-3 w-3"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 13l4 4L19 7"
            />
          </svg>
          Verified
        </Badge>
        <Badge variant="secondary" class="gap-1">
          <svg
            class="h-3 w-3"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          Processing
        </Badge>
        <Badge variant="outline" class="gap-1">
          <svg
            class="h-3 w-3"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          Info
        </Badge>
      </div>
    </div>

    <!-- Badges in Lists -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Badges in Lists</h2>
      <div class="space-y-3">
        <div class="flex items-center justify-between p-3 border rounded-lg">
          <div>
            <h3 class="font-medium">Feature Development</h3>
            <p class="text-sm text-muted-foreground">
              Working on new user interface
            </p>
          </div>
          <Badge
            class="bg-blue-100 text-blue-800 hover:bg-blue-100 dark:bg-blue-900 dark:text-blue-300"
          >
            In Progress
          </Badge>
        </div>
        <div class="flex items-center justify-between p-3 border rounded-lg">
          <div>
            <h3 class="font-medium">Bug Fixes</h3>
            <p class="text-sm text-muted-foreground">
              Resolving reported issues
            </p>
          </div>
          <Badge
            class="bg-green-100 text-green-800 hover:bg-green-100 dark:bg-green-900 dark:text-green-300"
          >
            Completed
          </Badge>
        </div>
        <div class="flex items-center justify-between p-3 border rounded-lg">
          <div>
            <h3 class="font-medium">Code Review</h3>
            <p class="text-sm text-muted-foreground">Pending team review</p>
          </div>
          <Badge
            class="bg-yellow-100 text-yellow-800 hover:bg-yellow-100 dark:bg-yellow-900 dark:text-yellow-300"
          >
            Pending
          </Badge>
        </div>
      </div>
    </div>

    <!-- Interactive Badges -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Interactive Badges</h2>
      <div class="flex flex-wrap gap-4">
        <Badge class="cursor-pointer hover:bg-primary/80"> Click me </Badge>
        <Badge variant="outline" class="cursor-pointer hover:bg-accent">
          Hover effect
        </Badge>
        <Badge
          variant="secondary"
          class="gap-1 cursor-pointer hover:bg-secondary/80"
        >
          Remove
          <svg
            class="h-3 w-3"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </Badge>
      </div>
    </div>
  </div>
</template>
