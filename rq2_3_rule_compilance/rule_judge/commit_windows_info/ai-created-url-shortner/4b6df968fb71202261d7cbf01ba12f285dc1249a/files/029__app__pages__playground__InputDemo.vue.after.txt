<script setup lang="ts">
definePageMeta({
  title: "Input Demo",
  description: "Text input field with various configurations",
});

const emailValue = ref("");
const passwordValue = ref("");
const disabledValue = ref("Cannot edit this");
const fileInput = ref(null);
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Input</h1>
      <p class="text-muted-foreground mt-2">
        Displays a form input field or a component that looks like an input
        field.
      </p>
    </div>

    <!-- Basic Input -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Basic Input</h2>
      <div class="grid w-full max-w-sm items-center gap-1.5">
        <Label for="basic">Basic Input</Label>
        <Input id="basic" type="text" placeholder="Enter text here..." />
      </div>
    </div>

    <!-- Input Types -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Input Types</h2>
      <div class="grid gap-4 md:grid-cols-2">
        <div class="grid w-full items-center gap-1.5">
          <Label for="email">Email</Label>
          <Input
            id="email"
            v-model="emailValue"
            type="email"
            placeholder="email@example.com"
          />
        </div>
        <div class="grid w-full items-center gap-1.5">
          <Label for="password">Password</Label>
          <Input
            id="password"
            v-model="passwordValue"
            type="password"
            placeholder="Enter password"
          />
        </div>
        <div class="grid w-full items-center gap-1.5">
          <Label for="number">Number</Label>
          <Input id="number" type="number" placeholder="123" />
        </div>
        <div class="grid w-full items-center gap-1.5">
          <Label for="tel">Phone</Label>
          <Input id="tel" type="tel" placeholder="+1 (555) 123-4567" />
        </div>
        <div class="grid w-full items-center gap-1.5">
          <Label for="url">URL</Label>
          <Input id="url" type="url" placeholder="https://example.com" />
        </div>
        <div class="grid w-full items-center gap-1.5">
          <Label for="search">Search</Label>
          <Input id="search" type="search" placeholder="Search..." />
        </div>
      </div>
    </div>

    <!-- Input States -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Input States</h2>
      <div class="grid gap-4 md:grid-cols-2">
        <div class="grid w-full items-center gap-1.5">
          <Label for="disabled">Disabled</Label>
          <Input id="disabled" v-model="disabledValue" type="text" disabled />
        </div>
        <div class="grid w-full items-center gap-1.5">
          <Label for="readonly">Read Only</Label>
          <Input id="readonly" type="text" value="Read only value" readonly />
        </div>
        <div class="grid w-full items-center gap-1.5">
          <Label for="required">Required</Label>
          <Input
            id="required"
            type="text"
            placeholder="This field is required"
            required
          />
        </div>
        <div class="grid w-full items-center gap-1.5">
          <Label for="error">With Error</Label>
          <Input
            id="error"
            type="text"
            placeholder="Invalid input"
            class="border-red-500 focus:border-red-500 focus:ring-red-500"
          />
          <p class="text-sm text-red-500">This field has an error</p>
        </div>
      </div>
    </div>

    <!-- Input with Icons -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Input with Icons</h2>
      <div class="grid gap-4 md:grid-cols-2">
        <div class="grid w-full items-center gap-1.5">
          <Label for="search-icon">Search with Icon</Label>
          <div class="relative">
            <svg
              class="absolute left-3 top-3 h-4 w-4 text-muted-foreground"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
            <Input
              id="search-icon"
              type="search"
              placeholder="Search..."
              class="pl-10"
            />
          </div>
        </div>
        <div class="grid w-full items-center gap-1.5">
          <Label for="email-icon">Email with Icon</Label>
          <div class="relative">
            <svg
              class="absolute left-3 top-3 h-4 w-4 text-muted-foreground"
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
            <Input
              id="email-icon"
              type="email"
              placeholder="Email"
              class="pl-10"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- File Input -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">File Input</h2>
      <div class="grid w-full max-w-sm items-center gap-1.5">
        <Label for="picture">Picture</Label>
        <Input id="picture" ref="fileInput" type="file" />
      </div>
    </div>

    <!-- Input Sizes -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Input Sizes</h2>
      <div class="space-y-3">
        <div class="grid w-full max-w-sm items-center gap-1.5">
          <Label for="small">Small Input</Label>
          <Input
            id="small"
            type="text"
            placeholder="Small input"
            class="h-8 text-sm"
          />
        </div>
        <div class="grid w-full max-w-sm items-center gap-1.5">
          <Label for="default">Default Input</Label>
          <Input id="default" type="text" placeholder="Default input" />
        </div>
        <div class="grid w-full max-w-sm items-center gap-1.5">
          <Label for="large">Large Input</Label>
          <Input
            id="large"
            type="text"
            placeholder="Large input"
            class="h-12 text-lg"
          />
        </div>
      </div>
    </div>

    <!-- Input with Button -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Input with Button</h2>
      <div class="flex w-full max-w-sm items-center space-x-2">
        <Input type="email" placeholder="Email" />
        <Button type="submit">Subscribe</Button>
      </div>
    </div>
  </div>
</template>
