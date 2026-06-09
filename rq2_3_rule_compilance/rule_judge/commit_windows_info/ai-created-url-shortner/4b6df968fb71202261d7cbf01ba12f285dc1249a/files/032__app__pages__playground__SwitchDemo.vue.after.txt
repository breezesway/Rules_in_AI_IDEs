<script setup lang="ts">
definePageMeta({
  title: "Switch & Toggle Demo",
  description: "Switch and toggle components for binary choices",
});

const airplaneMode = ref(false);
const bluetooth = ref(true);
const wifi = ref(true);
const notifications = ref(false);
const marketing = ref(false);
const darkMode = ref(false);
const autoSave = ref(true);
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Switch & Toggle</h1>
      <p class="text-muted-foreground mt-2">
        Toggle switches for binary on/off choices.
      </p>
    </div>

    <!-- Basic Switch -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Basic Switch</h2>
      <div class="space-y-4">
        <div class="flex items-center space-x-2">
          <Switch id="airplane-mode" v-model:checked="airplaneMode" />
          <Label for="airplane-mode">Airplane Mode</Label>
        </div>
        <div class="flex items-center space-x-2">
          <Switch id="bluetooth" v-model:checked="bluetooth" />
          <Label for="bluetooth">Bluetooth</Label>
        </div>
        <div class="flex items-center space-x-2">
          <Switch id="wifi" v-model:checked="wifi" />
          <Label for="wifi">Wi-Fi</Label>
        </div>
        <div class="text-sm text-muted-foreground">
          Status: Airplane Mode {{ airplaneMode ? "On" : "Off" }}, Bluetooth
          {{ bluetooth ? "On" : "Off" }}, Wi-Fi {{ wifi ? "On" : "Off" }}
        </div>
      </div>
    </div>

    <!-- Switch with Descriptions -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Switch with Descriptions</h2>
      <div class="space-y-6">
        <div class="flex items-center justify-between">
          <div class="space-y-0.5">
            <Label class="text-base">Push Notifications</Label>
            <p class="text-sm text-muted-foreground">
              Receive push notifications on this device
            </p>
          </div>
          <Switch v-model:checked="notifications" />
        </div>
        <div class="flex items-center justify-between">
          <div class="space-y-0.5">
            <Label class="text-base">Marketing Communications</Label>
            <p class="text-sm text-muted-foreground">
              Receive emails about new products and features
            </p>
          </div>
          <Switch v-model:checked="marketing" />
        </div>
        <div class="flex items-center justify-between">
          <div class="space-y-0.5">
            <Label class="text-base">Dark Mode</Label>
            <p class="text-sm text-muted-foreground">
              Use dark theme across the application
            </p>
          </div>
          <Switch v-model:checked="darkMode" />
        </div>
      </div>
    </div>

    <!-- Switch States -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Switch States</h2>
      <div class="grid gap-4 md:grid-cols-2">
        <div class="space-y-4">
          <div class="flex items-center space-x-2">
            <Switch id="default-off" />
            <Label for="default-off">Default (Off)</Label>
          </div>
          <div class="flex items-center space-x-2">
            <Switch id="default-on" checked />
            <Label for="default-on">Default (On)</Label>
          </div>
          <div class="flex items-center space-x-2">
            <Switch id="disabled-off" disabled />
            <Label for="disabled-off" class="text-muted-foreground"
              >Disabled (Off)</Label
            >
          </div>
          <div class="flex items-center space-x-2">
            <Switch id="disabled-on" disabled checked />
            <Label for="disabled-on" class="text-muted-foreground"
              >Disabled (On)</Label
            >
          </div>
        </div>
        <div class="space-y-4">
          <div class="flex items-center space-x-2">
            <Switch id="small" class="scale-75" />
            <Label for="small">Small Switch</Label>
          </div>
          <div class="flex items-center space-x-2">
            <Switch id="normal" />
            <Label for="normal">Normal Switch</Label>
          </div>
          <div class="flex items-center space-x-2">
            <Switch id="large" class="scale-125" />
            <Label for="large">Large Switch</Label>
          </div>
        </div>
      </div>
    </div>

    <!-- Toggle Button -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Toggle Button</h2>
      <div class="flex flex-wrap gap-4">
        <Toggle>
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
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
            />
          </svg>
        </Toggle>
        <Toggle>
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
              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
            />
          </svg>
        </Toggle>
        <Toggle>
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
              d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
            />
          </svg>
        </Toggle>
      </div>
    </div>

    <!-- Toggle with Text -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Toggle with Text</h2>
      <div class="flex flex-wrap gap-4">
        <Toggle>
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
              d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
            />
          </svg>
          Bold
        </Toggle>
        <Toggle>
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
              d="M10 4v16m8-8a4 4 0 11-8 0"
            />
          </svg>
          Italic
        </Toggle>
        <Toggle>
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
              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
            />
          </svg>
          Underline
        </Toggle>
      </div>
    </div>

    <!-- Toggle Group -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Toggle Group</h2>
      <div class="space-y-4">
        <div>
          <Label class="text-base">Text Alignment</Label>
          <ToggleGroup type="single" class="mt-2">
            <ToggleGroupItem value="left">
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
                  d="M4 6h16M4 12h8m-8 6h16"
                />
              </svg>
            </ToggleGroupItem>
            <ToggleGroupItem value="center">
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
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </ToggleGroupItem>
            <ToggleGroupItem value="right">
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
                  d="M4 6h16M12 12h8M4 18h16"
                />
              </svg>
            </ToggleGroupItem>
          </ToggleGroup>
        </div>
        <div>
          <Label class="text-base">Text Formatting</Label>
          <ToggleGroup type="multiple" class="mt-2">
            <ToggleGroupItem value="bold">
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
                  d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
                />
              </svg>
            </ToggleGroupItem>
            <ToggleGroupItem value="italic">
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
                  d="M10 4v16m8-8a4 4 0 11-8 0"
                />
              </svg>
            </ToggleGroupItem>
            <ToggleGroupItem value="underline">
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
                  d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                />
              </svg>
            </ToggleGroupItem>
          </ToggleGroup>
        </div>
      </div>
    </div>

    <!-- Settings Panel Example -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Settings Panel</h2>
      <Card class="p-6">
        <CardHeader class="px-0 pt-0">
          <CardTitle>Application Settings</CardTitle>
          <CardDescription>
            Configure your application preferences and behavior.
          </CardDescription>
        </CardHeader>
        <CardContent class="px-0 space-y-6">
          <div class="space-y-4">
            <h4 class="text-sm font-medium">Privacy & Security</h4>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div class="space-y-0.5">
                  <Label class="text-sm">Two-factor Authentication</Label>
                  <p class="text-xs text-muted-foreground">
                    Add an extra layer of security to your account
                  </p>
                </div>
                <Switch />
              </div>
              <div class="flex items-center justify-between">
                <div class="space-y-0.5">
                  <Label class="text-sm">Data Analytics</Label>
                  <p class="text-xs text-muted-foreground">
                    Help us improve by sharing anonymous usage data
                  </p>
                </div>
                <Switch />
              </div>
            </div>
          </div>

          <div class="space-y-4">
            <h4 class="text-sm font-medium">Productivity</h4>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div class="space-y-0.5">
                  <Label class="text-sm">Auto-save</Label>
                  <p class="text-xs text-muted-foreground">
                    Automatically save changes as you work
                  </p>
                </div>
                <Switch v-model:checked="autoSave" />
              </div>
              <div class="flex items-center justify-between">
                <div class="space-y-0.5">
                  <Label class="text-sm">Smart Suggestions</Label>
                  <p class="text-xs text-muted-foreground">
                    Show contextual suggestions and shortcuts
                  </p>
                </div>
                <Switch />
              </div>
            </div>
          </div>

          <div class="space-y-4">
            <h4 class="text-sm font-medium">Appearance</h4>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div class="space-y-0.5">
                  <Label class="text-sm">Dark Mode</Label>
                  <p class="text-xs text-muted-foreground">
                    Use dark theme throughout the application
                  </p>
                </div>
                <Switch v-model:checked="darkMode" />
              </div>
              <div class="flex items-center justify-between">
                <div class="space-y-0.5">
                  <Label class="text-sm">Animations</Label>
                  <p class="text-xs text-muted-foreground">
                    Enable smooth animations and transitions
                  </p>
                </div>
                <Switch checked />
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter class="px-0">
          <Button class="w-full">Save Settings</Button>
        </CardFooter>
      </Card>
    </div>
  </div>
</template>
