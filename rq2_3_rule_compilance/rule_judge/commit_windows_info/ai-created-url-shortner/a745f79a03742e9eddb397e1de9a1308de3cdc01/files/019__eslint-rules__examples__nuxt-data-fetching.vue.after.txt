<!-- eslint-disable -->
<!--Remove comment above to see all violations-->
<script setup>
// ❌ BAD: Using $fetch() in script setup root level
// Should use useFetch() or useAsyncData() instead
const _users = await $fetch("/api/users");

// ❌ BAD: Using fetch() in script setup root level
// Should use useFetch() or useAsyncData() instead
const response1 = await fetch("/api/data");
const _data1 = await response1.json();

// ❌ BAD: Using useAsyncData when useFetch would be simpler
const { data: _comments } = await useAsyncData("comments", () =>
  $fetch("/api/comments")
);

// Functions and event handlers
function handleSubmit() {
  // ❌ BAD: Using fetch() in function - should use $fetch()
  fetch("/api/submit", {
    method: "POST",
    body: JSON.stringify({}),
  }).then((response) => response.json());
}

async function loadData() {
  // ❌ BAD: Using useFetch() in function - should use $fetch()
  const { data: _result } = await useFetch("/api/function-data");
  return _result;
}

const onClick = async () => {
  // ❌ BAD: Using fetch() in arrow function - should use $fetch()
  const response = await fetch("/api/click-event");
  const _data = await response.json();

  // ❌ BAD: Using useAsyncData() in event handler - should use $fetch()
  const { data: _moreData } = await useAsyncData("clickData", () =>
    $fetch("/api/more")
  );
};

// Lifecycle hooks
onMounted(async () => {
  // ❌ BAD: Using fetch() in lifecycle hook - should use $fetch()
  const response = await fetch("/api/mounted-data");
  const _data = await response.json();

  // ❌ BAD: Using useFetch() in lifecycle hook - should use $fetch()
  const { data: _mountedData } = await useFetch("/api/mounted-fetch");
});

onUpdated(() => {
  // ❌ BAD: Using fetch() in lifecycle hook - should use $fetch()
  fetch("/api/updated").then((r) => r.json());

  // ❌ BAD: Using useAsyncData() in lifecycle hook - should use $fetch()
  useAsyncData("updated", () => $fetch("/api/updated-data"));
});

// Event handlers
const handleFormSubmit = async (event) => {
  // ❌ BAD: Using fetch() in event handler - should use $fetch()
  const _result = await fetch("/api/form-submit", {
    method: "POST",
    body: new FormData(event.target),
  });
};
</script>

<template>
  <div>
    <h1>ESLint Rule Test - Bad Examples</h1>
    <p>This file contains patterns that violate the nuxt-data-fetching rule.</p>
    <p>
      <strong
        >Remove the eslint-disable comment at the top to see all
        violations.</strong
      >
    </p>

    <form @submit="handleFormSubmit">
      <button type="submit">Submit Form</button>
    </form>

    <button @click="onClick">Click Me</button>
    <button @click="loadData">Load Data</button>
    <button @click="handleSubmit">Handle Submit</button>
  </div>
</template>
