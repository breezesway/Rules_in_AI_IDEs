<script setup lang="ts">
definePageMeta({
  title: "Checkbox & Radio Demo",
  description: "Checkbox and radio button form controls",
});

const terms = ref(false);
const marketing = ref(true);
const notifications = ref(false);
const privacy = ref(false);

const paymentMethod = ref("card");
const plan = ref("");
const contactMethod = ref("email");
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Checkbox & Radio</h1>
      <p class="text-muted-foreground mt-2">
        Form controls for selecting options and making choices.
      </p>
    </div>

    <!-- Basic Checkbox -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Basic Checkbox</h2>
      <div class="space-y-4">
        <div class="flex items-center space-x-2">
          <Checkbox id="terms" v-model:checked="terms" />
          <Label
            for="terms"
            class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          >
            Accept terms and conditions
          </Label>
        </div>
        <div class="flex items-center space-x-2">
          <Checkbox id="marketing" v-model:checked="marketing" />
          <Label
            for="marketing"
            class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          >
            Send me marketing emails
          </Label>
        </div>
        <div class="flex items-center space-x-2">
          <Checkbox id="notifications" v-model:checked="notifications" />
          <Label
            for="notifications"
            class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          >
            Send me notifications
          </Label>
        </div>
        <div class="text-sm text-muted-foreground">
          Selected:
          {{
            [
              terms && "Terms",
              marketing && "Marketing",
              notifications && "Notifications",
            ]
              .filter(Boolean)
              .join(", ") || "None"
          }}
        </div>
      </div>
    </div>

    <!-- Checkbox States -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Checkbox States</h2>
      <div class="grid gap-4 md:grid-cols-2">
        <div class="space-y-4">
          <div class="flex items-center space-x-2">
            <Checkbox id="default" />
            <Label for="default">Default</Label>
          </div>
          <div class="flex items-center space-x-2">
            <Checkbox id="checked" checked />
            <Label for="checked">Checked</Label>
          </div>
          <div class="flex items-center space-x-2">
            <Checkbox id="disabled" disabled />
            <Label for="disabled" class="text-muted-foreground">Disabled</Label>
          </div>
          <div class="flex items-center space-x-2">
            <Checkbox id="disabled-checked" disabled checked />
            <Label for="disabled-checked" class="text-muted-foreground"
              >Disabled + Checked</Label
            >
          </div>
        </div>
        <div class="space-y-4">
          <div class="flex items-start space-x-2">
            <Checkbox id="privacy" v-model:checked="privacy" class="mt-1" />
            <div class="grid gap-1.5 leading-none">
              <Label
                for="privacy"
                class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                Privacy Policy
              </Label>
              <p class="text-xs text-muted-foreground">
                I agree to the privacy policy and data processing terms.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Radio Groups -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Radio Groups</h2>
      <div class="space-y-6">
        <div class="space-y-3">
          <Label class="text-base font-medium">Payment Method</Label>
          <RadioGroup v-model="paymentMethod" class="flex flex-col space-y-2">
            <div class="flex items-center space-x-2">
              <RadioGroupItem id="card" value="card" />
              <Label for="card">Credit Card</Label>
            </div>
            <div class="flex items-center space-x-2">
              <RadioGroupItem id="paypal" value="paypal" />
              <Label for="paypal">PayPal</Label>
            </div>
            <div class="flex items-center space-x-2">
              <RadioGroupItem id="apple" value="apple" />
              <Label for="apple">Apple Pay</Label>
            </div>
            <div class="flex items-center space-x-2">
              <RadioGroupItem id="google" value="google" />
              <Label for="google">Google Pay</Label>
            </div>
          </RadioGroup>
          <div class="text-sm text-muted-foreground">
            Selected: {{ paymentMethod }}
          </div>
        </div>

        <div class="space-y-3">
          <Label class="text-base font-medium">Subscription Plan</Label>
          <RadioGroup v-model="plan" class="flex flex-col space-y-2">
            <div class="flex items-center space-x-2">
              <RadioGroupItem id="free" value="free" />
              <div class="grid gap-1.5 leading-none">
                <Label for="free" class="text-sm font-medium">Free</Label>
                <p class="text-xs text-muted-foreground">
                  Basic features for personal use
                </p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <RadioGroupItem id="pro" value="pro" />
              <div class="grid gap-1.5 leading-none">
                <Label for="pro" class="text-sm font-medium"
                  >Pro - $9/month</Label
                >
                <p class="text-xs text-muted-foreground">
                  Advanced features for professionals
                </p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <RadioGroupItem id="team" value="team" />
              <div class="grid gap-1.5 leading-none">
                <Label for="team" class="text-sm font-medium"
                  >Team - $29/month</Label
                >
                <p class="text-xs text-muted-foreground">
                  Collaboration tools for teams
                </p>
              </div>
            </div>
          </RadioGroup>
          <div class="text-sm text-muted-foreground">
            Selected plan: {{ plan || "None" }}
          </div>
        </div>
      </div>
    </div>

    <!-- Inline Radio -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Inline Radio</h2>
      <div class="space-y-3">
        <Label class="text-base font-medium">Preferred Contact Method</Label>
        <RadioGroup v-model="contactMethod" class="flex flex-wrap gap-6">
          <div class="flex items-center space-x-2">
            <RadioGroupItem id="contact-email" value="email" />
            <Label for="contact-email">Email</Label>
          </div>
          <div class="flex items-center space-x-2">
            <RadioGroupItem id="contact-phone" value="phone" />
            <Label for="contact-phone">Phone</Label>
          </div>
          <div class="flex items-center space-x-2">
            <RadioGroupItem id="contact-sms" value="sms" />
            <Label for="contact-sms">SMS</Label>
          </div>
          <div class="flex items-center space-x-2">
            <RadioGroupItem id="contact-none" value="none" />
            <Label for="contact-none">No contact</Label>
          </div>
        </RadioGroup>
      </div>
    </div>

    <!-- Form Example -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Form Example</h2>
      <Card class="p-6">
        <CardHeader class="px-0 pt-0">
          <CardTitle>Account Preferences</CardTitle>
          <CardDescription>
            Configure your account settings and preferences.
          </CardDescription>
        </CardHeader>
        <CardContent class="px-0 space-y-6">
          <div class="space-y-3">
            <Label class="text-base font-medium">Email Preferences</Label>
            <div class="space-y-3">
              <div class="flex items-center space-x-2">
                <Checkbox id="newsletter" />
                <Label for="newsletter" class="text-sm"
                  >Newsletter updates</Label
                >
              </div>
              <div class="flex items-center space-x-2">
                <Checkbox id="product-updates" />
                <Label for="product-updates" class="text-sm"
                  >Product updates</Label
                >
              </div>
              <div class="flex items-center space-x-2">
                <Checkbox id="security-alerts" checked />
                <Label for="security-alerts" class="text-sm"
                  >Security alerts (required)</Label
                >
              </div>
            </div>
          </div>

          <div class="space-y-3">
            <Label class="text-base font-medium">Theme Preference</Label>
            <RadioGroup default-value="system" class="flex flex-col space-y-2">
              <div class="flex items-center space-x-2">
                <RadioGroupItem id="theme-light" value="light" />
                <Label for="theme-light">Light</Label>
              </div>
              <div class="flex items-center space-x-2">
                <RadioGroupItem id="theme-dark" value="dark" />
                <Label for="theme-dark">Dark</Label>
              </div>
              <div class="flex items-center space-x-2">
                <RadioGroupItem id="theme-system" value="system" />
                <Label for="theme-system">System</Label>
              </div>
            </RadioGroup>
          </div>

          <div class="space-y-3">
            <Label class="text-base font-medium">Data Usage</Label>
            <RadioGroup
              default-value="necessary"
              class="flex flex-col space-y-2"
            >
              <div class="flex items-start space-x-2">
                <RadioGroupItem id="data-all" value="all" class="mt-1" />
                <div class="grid gap-1.5 leading-none">
                  <Label for="data-all" class="text-sm font-medium"
                    >All data</Label
                  >
                  <p class="text-xs text-muted-foreground">
                    Use all data for analytics and personalization
                  </p>
                </div>
              </div>
              <div class="flex items-start space-x-2">
                <RadioGroupItem
                  id="data-necessary"
                  value="necessary"
                  class="mt-1"
                />
                <div class="grid gap-1.5 leading-none">
                  <Label for="data-necessary" class="text-sm font-medium"
                    >Necessary only</Label
                  >
                  <p class="text-xs text-muted-foreground">
                    Only use data necessary for core functionality
                  </p>
                </div>
              </div>
            </RadioGroup>
          </div>
        </CardContent>
        <CardFooter class="px-0">
          <Button class="w-full">Save Preferences</Button>
        </CardFooter>
      </Card>
    </div>
  </div>
</template>
