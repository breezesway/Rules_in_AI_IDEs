---
to: app/components/<%= name %>/<%= name %>.vue
---
<script setup lang="ts">
// vueuse composables are auto-imported and can be used in the component
// Other project components are auto-imported and can be used in the component
// This component is documented in ./README.md (do not remove this comment)


defineProps<{
  /**
   * Always use JSDocs for props
   */
  someProp: string
}>()

</script>

<template>
  <!-- Shadcn and Tailwind can be used to make a great looking component -->
  <!-- NuxtImg is a great way to display images -->
  <!-- The <Icon> component from NuxtIcon is a great way to display icons -->
</template>
