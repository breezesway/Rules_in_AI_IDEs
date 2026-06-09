---
to: app/components/<%= name %>/README.md
---
# <%= name %>

{{A Short Description of the component, when to use it, what it does, etc.}}

## Features 

- Feature 1
- Feature 2
- Feature 3

## 🚀 Usage

View Component demo [here](http://localhost:3000/playground/<%= name %>Demo)


### Basic Usage

```vue
<template>
  <<%= name %> />
</template>
```

## 📋 Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `someProp` | `string` | `'someProp'` | The someProp to display |


## 🎯 Events

| Event | Payload | Description |
|-------|---------|-------------|
| `someEvent` | `string` | The someEvent to display |

## 🎨 Slots

| Slot | Description |
|------|-------------|
| `default` | Main content area |


## 🧪 Testing

Run the component tests:

```bash
# Run all tests for this component
npm run test -- app/components/<%= name %>
```

## Other Notes

<!-- Add any other notes here -->