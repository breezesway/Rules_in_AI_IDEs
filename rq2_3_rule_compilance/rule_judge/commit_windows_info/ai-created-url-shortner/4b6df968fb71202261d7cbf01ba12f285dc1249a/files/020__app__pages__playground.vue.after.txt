<script setup lang="ts">
definePageMeta({
  middleware: "dev-only",
});
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-4xl mx-auto space-y-8">
      <NuxtPage />
    </div>
  </div>
</template>
