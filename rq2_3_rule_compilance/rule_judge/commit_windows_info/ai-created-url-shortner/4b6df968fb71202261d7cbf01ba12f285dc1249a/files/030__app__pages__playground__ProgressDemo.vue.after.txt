<script setup lang="ts">
definePageMeta({
  title: "Progress Demo",
  description: "Progress indicators and loading states",
});

const progressValue = ref(33);
const animatedProgress = ref(0);
const uploadProgress = ref(0);
const isUploading = ref(false);

// Animated progress simulation
const startAnimation = () => {
  animatedProgress.value = 0;
  const interval = setInterval(() => {
    animatedProgress.value += 1;
    if (animatedProgress.value >= 100) {
      clearInterval(interval);
    }
  }, 50);
};

// Upload simulation
const simulateUpload = () => {
  isUploading.value = true;
  uploadProgress.value = 0;
  const interval = setInterval(() => {
    uploadProgress.value += Math.random() * 10;
    if (uploadProgress.value >= 100) {
      uploadProgress.value = 100;
      isUploading.value = false;
      clearInterval(interval);
    }
  }, 200);
};

const steps = [
  {
    id: 1,
    title: "Account Setup",
    description: "Create your account",
    completed: true,
  },
  {
    id: 2,
    title: "Profile Information",
    description: "Add your details",
    completed: true,
  },
  {
    id: 3,
    title: "Verification",
    description: "Verify your email",
    completed: false,
    current: true,
  },
  { id: 4, title: "Complete", description: "Setup complete", completed: false },
];

// Start animation on mount
onMounted(() => {
  startAnimation();
});
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Progress</h1>
      <p class="text-muted-foreground mt-2">
        Displays an indicator showing the completion progress of a task.
      </p>
    </div>

    <!-- Basic Progress -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Basic Progress</h2>
      <div class="space-y-4">
        <div class="space-y-2">
          <div class="flex justify-between text-sm">
            <span>Progress</span>
            <span>{{ progressValue }}%</span>
          </div>
          <Progress :model-value="progressValue" class="w-full" />
        </div>
        <div class="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            @click="progressValue = Math.max(0, progressValue - 10)"
          >
            -10%
          </Button>
          <Button
            variant="outline"
            size="sm"
            @click="progressValue = Math.min(100, progressValue + 10)"
          >
            +10%
          </Button>
          <Button variant="outline" size="sm" @click="progressValue = 0">
            Reset
          </Button>
        </div>
      </div>
    </div>

    <!-- Progress Variants -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Progress Variants</h2>
      <div class="space-y-6">
        <div class="space-y-2">
          <Label>Default (33%)</Label>
          <Progress :model-value="33" class="w-full" />
        </div>
        <div class="space-y-2">
          <Label>Success (75%)</Label>
          <Progress :model-value="75" class="w-full [&>div]:bg-green-500" />
        </div>
        <div class="space-y-2">
          <Label>Warning (50%)</Label>
          <Progress :model-value="50" class="w-full [&>div]:bg-yellow-500" />
        </div>
        <div class="space-y-2">
          <Label>Danger (25%)</Label>
          <Progress :model-value="25" class="w-full [&>div]:bg-red-500" />
        </div>
      </div>
    </div>

    <!-- Animated Progress -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Animated Progress</h2>
      <div class="space-y-4">
        <div class="space-y-2">
          <div class="flex justify-between text-sm">
            <span>Loading Animation</span>
            <span>{{ Math.round(animatedProgress) }}%</span>
          </div>
          <Progress :model-value="animatedProgress" class="w-full" />
        </div>
        <Button variant="outline" @click="startAnimation">
          Restart Animation
        </Button>
      </div>
    </div>

    <!-- File Upload Progress -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">File Upload Progress</h2>
      <Card class="p-6">
        <div class="space-y-4">
          <div class="flex items-center gap-4">
            <div class="flex-1">
              <div class="flex items-center gap-2">
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
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
                <span class="font-medium">document.pdf</span>
                <span class="text-sm text-muted-foreground">(2.4 MB)</span>
              </div>
              <div class="mt-2 space-y-1">
                <Progress :model-value="uploadProgress" class="w-full" />
                <div class="flex justify-between text-xs text-muted-foreground">
                  <span>{{ Math.round(uploadProgress) }}% complete</span>
                  <span v-if="isUploading">Uploading...</span>
                  <span v-else-if="uploadProgress === 100">Complete!</span>
                  <span v-else>Ready to upload</span>
                </div>
              </div>
            </div>
            <Button
              :disabled="isUploading"
              variant="outline"
              size="sm"
              @click="simulateUpload"
            >
              {{ isUploading ? "Uploading..." : "Upload" }}
            </Button>
          </div>
        </div>
      </Card>
    </div>

    <!-- Progress with Steps -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Step Progress</h2>
      <Card class="p-6">
        <div class="space-y-6">
          <div class="space-y-2">
            <div class="flex justify-between text-sm">
              <span>Setup Progress</span>
              <span>Step 3 of 4</span>
            </div>
            <Progress :model-value="75" class="w-full" />
          </div>
          <div class="space-y-4">
            <div
              v-for="step in steps"
              :key="step.id"
              class="flex items-center gap-4"
            >
              <div
                class="flex items-center justify-center w-8 h-8 rounded-full border-2"
                :class="{
                  'bg-primary border-primary text-primary-foreground':
                    step.completed,
                  'border-primary bg-primary/10':
                    step.current && !step.completed,
                  'border-muted-foreground/30':
                    !step.completed && !step.current,
                }"
              >
                <svg
                  v-if="step.completed"
                  class="h-4 w-4"
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
                <span v-else class="text-sm font-medium">{{ step.id }}</span>
              </div>
              <div class="flex-1">
                <h4
                  class="font-medium"
                  :class="{
                    'text-primary': step.current,
                    'text-muted-foreground': !step.completed && !step.current,
                  }"
                >
                  {{ step.title }}
                </h4>
                <p class="text-sm text-muted-foreground">
                  {{ step.description }}
                </p>
              </div>
              <Badge
                v-if="step.completed"
                variant="secondary"
                class="bg-green-100 text-green-800 hover:bg-green-100 dark:bg-green-900 dark:text-green-300"
              >
                Complete
              </Badge>
              <Badge
                v-else-if="step.current"
                class="bg-blue-100 text-blue-800 hover:bg-blue-100 dark:bg-blue-900 dark:text-blue-300"
              >
                In Progress
              </Badge>
            </div>
          </div>
        </div>
      </Card>
    </div>

    <!-- Progress Sizes -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Progress Sizes</h2>
      <div class="space-y-4">
        <div class="space-y-2">
          <Label>Small</Label>
          <Progress :model-value="60" class="w-full h-1" />
        </div>
        <div class="space-y-2">
          <Label>Default</Label>
          <Progress :model-value="60" class="w-full" />
        </div>
        <div class="space-y-2">
          <Label>Large</Label>
          <Progress :model-value="60" class="w-full h-3" />
        </div>
      </div>
    </div>

    <!-- Indeterminate Progress -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Indeterminate Progress</h2>
      <div class="space-y-4">
        <div class="space-y-2">
          <Label>Loading...</Label>
          <div class="w-full h-2 bg-muted rounded-full overflow-hidden">
            <div class="h-full bg-primary animate-pulse" />
          </div>
        </div>
        <div class="space-y-2">
          <Label>Processing...</Label>
          <div class="w-full h-2 bg-muted rounded-full overflow-hidden">
            <div class="h-full w-1/3 bg-primary animate-bounce" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
