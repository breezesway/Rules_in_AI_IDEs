---
to: app/components/<%= name %>/<%= name %>Child.vue
---


<script setup lang="ts">

defineProps<{
  /**
   * Always use JSDocs for props
   */
  someProp: string
}>()
</script>

<template>
  <!-- This component is a tightly coupled component that is used in the parent component -->
  <!-- It is not a standalone component -->
  <!-- Components like this are great for breaking complex components into smaller, more manageable pieces -->
  <!-- Use as many of these Child components in this directory as you need to make the parent component easier to understand -->
  <!-- Make sure they are always prefixed with the parent components name -->
  <!-- You can rename this file to make sense for the use case at hand -->
  <!-- Example: Parent is <UserProfile /> and the child is <UserProfileImg /> -->
</template>