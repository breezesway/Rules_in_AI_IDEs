<script setup lang="ts">
definePageMeta({
  title: "Select Demo",
  description: "Select component with various configurations",
});

const frameworks = [
  { value: "next", label: "Next.js" },
  { value: "sveltekit", label: "SvelteKit" },
  { value: "nuxt", label: "Nuxt.js" },
  { value: "remix", label: "Remix" },
  { value: "astro", label: "Astro" },
];

const countries = [
  { value: "us", label: "United States", flag: "🇺🇸" },
  { value: "ca", label: "Canada", flag: "🇨🇦" },
  { value: "gb", label: "United Kingdom", flag: "🇬🇧" },
  { value: "de", label: "Germany", flag: "🇩🇪" },
  { value: "fr", label: "France", flag: "🇫🇷" },
  { value: "jp", label: "Japan", flag: "🇯🇵" },
  { value: "au", label: "Australia", flag: "🇦🇺" },
];

const selectedFramework = ref("");
const selectedCountry = ref("");
const selectedPriority = ref("");
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Select</h1>
      <p class="text-muted-foreground mt-2">
        Displays a list of options for the user to pick from—triggered by a
        button.
      </p>
    </div>

    <!-- Basic Select -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Basic Select</h2>
      <div class="grid gap-4 md:grid-cols-2">
        <div class="space-y-2">
          <Label for="framework">Framework</Label>
          <Select v-model="selectedFramework">
            <SelectTrigger id="framework">
              <SelectValue placeholder="Select a framework" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem
                v-for="framework in frameworks"
                :key="framework.value"
                :value="framework.value"
              >
                {{ framework.label }}
              </SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div class="space-y-2">
          <Label for="country">Country</Label>
          <Select v-model="selectedCountry">
            <SelectTrigger id="country">
              <SelectValue placeholder="Select a country" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem
                v-for="country in countries"
                :key="country.value"
                :value="country.value"
              >
                <div class="flex items-center gap-2">
                  <span>{{ country.flag }}</span>
                  <span>{{ country.label }}</span>
                </div>
              </SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
      <div class="text-sm text-muted-foreground">
        Selected Framework: {{ selectedFramework || "None" }} | Selected
        Country: {{ selectedCountry || "None" }}
      </div>
    </div>

    <!-- Select with Groups -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Select with Groups</h2>
      <div class="max-w-sm space-y-2">
        <Label for="timezone">Timezone</Label>
        <Select>
          <SelectTrigger id="timezone">
            <SelectValue placeholder="Select a timezone" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectLabel>North America</SelectLabel>
              <SelectItem value="est">Eastern Standard Time (EST)</SelectItem>
              <SelectItem value="cst">Central Standard Time (CST)</SelectItem>
              <SelectItem value="mst">Mountain Standard Time (MST)</SelectItem>
              <SelectItem value="pst">Pacific Standard Time (PST)</SelectItem>
            </SelectGroup>
            <SelectSeparator />
            <SelectGroup>
              <SelectLabel>Europe</SelectLabel>
              <SelectItem value="gmt">Greenwich Mean Time (GMT)</SelectItem>
              <SelectItem value="cet">Central European Time (CET)</SelectItem>
              <SelectItem value="eet">Eastern European Time (EET)</SelectItem>
            </SelectGroup>
            <SelectSeparator />
            <SelectGroup>
              <SelectLabel>Asia</SelectLabel>
              <SelectItem value="jst">Japan Standard Time (JST)</SelectItem>
              <SelectItem value="kst">Korea Standard Time (KST)</SelectItem>
              <SelectItem value="ist">India Standard Time (IST)</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>
    </div>

    <!-- Select Variants -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Select Variants</h2>
      <div class="grid gap-4 md:grid-cols-3">
        <div class="space-y-2">
          <Label for="default-select">Default</Label>
          <Select>
            <SelectTrigger id="default-select">
              <SelectValue placeholder="Default select" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="option1">Option 1</SelectItem>
              <SelectItem value="option2">Option 2</SelectItem>
              <SelectItem value="option3">Option 3</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div class="space-y-2">
          <Label for="disabled-select">Disabled</Label>
          <Select disabled>
            <SelectTrigger id="disabled-select">
              <SelectValue placeholder="Disabled select" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="option1">Option 1</SelectItem>
              <SelectItem value="option2">Option 2</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div class="space-y-2">
          <Label for="error-select">With Error</Label>
          <Select>
            <SelectTrigger
              id="error-select"
              class="border-red-500 focus:border-red-500 focus:ring-red-500"
            >
              <SelectValue placeholder="Select with error" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="option1">Option 1</SelectItem>
              <SelectItem value="option2">Option 2</SelectItem>
            </SelectContent>
          </Select>
          <p class="text-sm text-red-500">This field is required</p>
        </div>
      </div>
    </div>

    <!-- Priority Select -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Priority Select</h2>
      <div class="max-w-sm space-y-2">
        <Label for="priority">Priority</Label>
        <Select v-model="selectedPriority">
          <SelectTrigger id="priority">
            <SelectValue placeholder="Select priority" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="low">
              <div class="flex items-center gap-2">
                <div class="w-2 h-2 rounded-full bg-blue-500" />
                Low
              </div>
            </SelectItem>
            <SelectItem value="medium">
              <div class="flex items-center gap-2">
                <div class="w-2 h-2 rounded-full bg-yellow-500" />
                Medium
              </div>
            </SelectItem>
            <SelectItem value="high">
              <div class="flex items-center gap-2">
                <div class="w-2 h-2 rounded-full bg-orange-500" />
                High
              </div>
            </SelectItem>
            <SelectItem value="critical">
              <div class="flex items-center gap-2">
                <div class="w-2 h-2 rounded-full bg-red-500" />
                Critical
              </div>
            </SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>

    <!-- Multi-column Select Content -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Select with Rich Content</h2>
      <div class="max-w-sm space-y-2">
        <Label for="user">Assign to User</Label>
        <Select>
          <SelectTrigger id="user">
            <SelectValue placeholder="Select a user" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="john">
              <div class="flex items-center gap-3">
                <div
                  class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-medium"
                >
                  JD
                </div>
                <div>
                  <div class="font-medium">John Doe</div>
                  <div class="text-sm text-muted-foreground">
                    john@example.com
                  </div>
                </div>
              </div>
            </SelectItem>
            <SelectItem value="jane">
              <div class="flex items-center gap-3">
                <div
                  class="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white text-sm font-medium"
                >
                  JS
                </div>
                <div>
                  <div class="font-medium">Jane Smith</div>
                  <div class="text-sm text-muted-foreground">
                    jane@example.com
                  </div>
                </div>
              </div>
            </SelectItem>
            <SelectItem value="bob">
              <div class="flex items-center gap-3">
                <div
                  class="w-8 h-8 rounded-full bg-purple-500 flex items-center justify-center text-white text-sm font-medium"
                >
                  BJ
                </div>
                <div>
                  <div class="font-medium">Bob Johnson</div>
                  <div class="text-sm text-muted-foreground">
                    bob@example.com
                  </div>
                </div>
              </div>
            </SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>

    <!-- Select Sizes -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Select Sizes</h2>
      <div class="space-y-3">
        <div class="space-y-2">
          <Label for="small-select">Small</Label>
          <Select>
            <SelectTrigger id="small-select" class="h-8 text-sm">
              <SelectValue placeholder="Small select" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="option1">Option 1</SelectItem>
              <SelectItem value="option2">Option 2</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div class="space-y-2">
          <Label for="default-size">Default</Label>
          <Select>
            <SelectTrigger id="default-size">
              <SelectValue placeholder="Default select" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="option1">Option 1</SelectItem>
              <SelectItem value="option2">Option 2</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div class="space-y-2">
          <Label for="large-select">Large</Label>
          <Select>
            <SelectTrigger id="large-select" class="h-12 text-lg">
              <SelectValue placeholder="Large select" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="option1">Option 1</SelectItem>
              <SelectItem value="option2">Option 2</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
    </div>

    <!-- Form Example -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Form Example</h2>
      <Card class="p-6">
        <CardHeader class="px-0 pt-0">
          <CardTitle>Create Account</CardTitle>
          <CardDescription>
            Fill in the information below to create your account.
          </CardDescription>
        </CardHeader>
        <CardContent class="px-0 space-y-4">
          <div class="grid gap-4 md:grid-cols-2">
            <div class="space-y-2">
              <Label for="account-type">Account Type</Label>
              <Select>
                <SelectTrigger id="account-type">
                  <SelectValue placeholder="Select account type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="personal">Personal</SelectItem>
                  <SelectItem value="business">Business</SelectItem>
                  <SelectItem value="organization">Organization</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div class="space-y-2">
              <Label for="plan">Plan</Label>
              <Select>
                <SelectTrigger id="plan">
                  <SelectValue placeholder="Select a plan" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="free">Free</SelectItem>
                  <SelectItem value="pro">Pro - $9/month</SelectItem>
                  <SelectItem value="team">Team - $29/month</SelectItem>
                  <SelectItem value="enterprise"
                    >Enterprise - Contact us</SelectItem
                  >
                </SelectContent>
              </Select>
            </div>
            <div class="space-y-2">
              <Label for="region">Region</Label>
              <Select>
                <SelectTrigger id="region">
                  <SelectValue placeholder="Select region" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="us-east">US East</SelectItem>
                  <SelectItem value="us-west">US West</SelectItem>
                  <SelectItem value="eu-west">EU West</SelectItem>
                  <SelectItem value="ap-southeast">AP Southeast</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div class="space-y-2">
              <Label for="notifications">Email Notifications</Label>
              <Select>
                <SelectTrigger id="notifications">
                  <SelectValue placeholder="Select frequency" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="never">Never</SelectItem>
                  <SelectItem value="weekly">Weekly</SelectItem>
                  <SelectItem value="daily">Daily</SelectItem>
                  <SelectItem value="realtime">Real-time</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
        <CardFooter class="px-0">
          <Button class="w-full">Create Account</Button>
        </CardFooter>
      </Card>
    </div>
  </div>
</template>
