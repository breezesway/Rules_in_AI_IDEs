---
to: app/pages/playground/<%= name %>Demo.vue
---
<script setup lang="ts">

definePageMeta({
  title: "<%= name %> Demo",
});


</script>

<template>
  <!-- DO NOT ADD DOCS HERE, ADD THEM TO README.MD -->
  <!-- This file is for examples and demos only -->
  <div class="max-w-4xl mx-auto space-y-8">
    <!-- Header -->
    <div>
      <h1 class="text-3xl font-bold mb-4">Chat Widget Demo</h1>
      <p class="text-muted-foreground mb-6">
        [shortDescription]
      </p>
      <Button
        variant="outline"
        @click.prevent.stop="openReadme('app/components/<%= name %>/README.md')"
      >
        <Icon name="lucide:file-text" class="w-4 h-4 mr-2" />
        View README
      </Button>
    </div>

    <!-- Example 1 -->
    <div class="space-y-4">
      <h2 id="example-1" class="text-2xl font-semibold">Example 1</h2>
      <div><!-- Example 1 Goes Here --></div>
    </div>
  
    <!-- More Examples -->

    
  </div>
  
</template>

