<script setup lang="ts">
definePageMeta({
  title: "Tabs Demo",
  description: "A set of layered sections of content known as tab panels",
});
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Tabs</h1>
      <p class="text-muted-foreground mt-2">
        A set of layered sections of content known as tab panels that are
        displayed one at a time.
      </p>
    </div>

    <!-- Basic Tabs -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Basic Tabs</h2>
      <Tabs default-value="account" class="w-[400px]">
        <TabsList class="grid w-full grid-cols-2">
          <TabsTrigger value="account">Account</TabsTrigger>
          <TabsTrigger value="password">Password</TabsTrigger>
        </TabsList>
        <TabsContent value="account" class="space-y-2">
          <div class="space-y-1">
            <h3 class="text-sm font-medium">Account</h3>
            <p class="text-sm text-muted-foreground">
              Make changes to your account here. Click save when you're done.
            </p>
          </div>
          <div class="space-y-2">
            <div class="space-y-1">
              <Label for="name">Name</Label>
              <Input id="name" value="Pedro Duarte" />
            </div>
            <div class="space-y-1">
              <Label for="username">Username</Label>
              <Input id="username" value="@peduarte" />
            </div>
          </div>
          <Button>Save changes</Button>
        </TabsContent>
        <TabsContent value="password" class="space-y-2">
          <div class="space-y-1">
            <h3 class="text-sm font-medium">Password</h3>
            <p class="text-sm text-muted-foreground">
              Change your password here. After saving, you'll be logged out.
            </p>
          </div>
          <div class="space-y-2">
            <div class="space-y-1">
              <Label for="current">Current password</Label>
              <Input id="current" type="password" />
            </div>
            <div class="space-y-1">
              <Label for="new">New password</Label>
              <Input id="new" type="password" />
            </div>
          </div>
          <Button>Save password</Button>
        </TabsContent>
      </Tabs>
    </div>

    <!-- Dashboard Tabs -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Dashboard Tabs</h2>
      <Tabs default-value="overview" class="w-full">
        <TabsList class="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="reports">Reports</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
        </TabsList>
        <TabsContent value="overview" class="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Overview</CardTitle>
              <CardDescription>
                Your dashboard overview and key metrics.
              </CardDescription>
            </CardHeader>
            <CardContent class="pt-6">
              <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <div class="flex flex-col space-y-2">
                  <span class="text-sm font-medium text-muted-foreground"
                    >Total Users</span
                  >
                  <span class="text-2xl font-bold">1,234</span>
                </div>
                <div class="flex flex-col space-y-2">
                  <span class="text-sm font-medium text-muted-foreground"
                    >Revenue</span
                  >
                  <span class="text-2xl font-bold">$12,345</span>
                </div>
                <div class="flex flex-col space-y-2">
                  <span class="text-sm font-medium text-muted-foreground"
                    >Orders</span
                  >
                  <span class="text-2xl font-bold">456</span>
                </div>
                <div class="flex flex-col space-y-2">
                  <span class="text-sm font-medium text-muted-foreground"
                    >Growth</span
                  >
                  <span class="text-2xl font-bold">+12%</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="analytics" class="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Analytics</CardTitle>
              <CardDescription>
                Detailed analytics and performance metrics.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div class="text-center py-8">
                <p class="text-muted-foreground">
                  Analytics charts and data would be displayed here.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="reports" class="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Reports</CardTitle>
              <CardDescription>
                Generate and view detailed reports.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div class="text-center py-8">
                <p class="text-muted-foreground">
                  Report generation interface would be displayed here.
                </p>
                <Button class="mt-4">Generate Report</Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="notifications" class="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Notifications</CardTitle>
              <CardDescription>
                Manage your notification preferences.
              </CardDescription>
            </CardHeader>
            <CardContent class="space-y-4">
              <div class="flex items-center justify-between">
                <div class="space-y-0.5">
                  <Label class="text-base">Email Notifications</Label>
                  <p class="text-sm text-muted-foreground">
                    Receive notifications via email
                  </p>
                </div>
                <Switch />
              </div>
              <div class="flex items-center justify-between">
                <div class="space-y-0.5">
                  <Label class="text-base">Push Notifications</Label>
                  <p class="text-sm text-muted-foreground">
                    Receive push notifications
                  </p>
                </div>
                <Switch />
              </div>
              <div class="flex items-center justify-between">
                <div class="space-y-0.5">
                  <Label class="text-base">SMS Notifications</Label>
                  <p class="text-sm text-muted-foreground">
                    Receive notifications via SMS
                  </p>
                </div>
                <Switch />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>

    <!-- Vertical Tabs -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Vertical Tabs</h2>
      <div class="flex space-x-6">
        <Tabs default-value="general" orientation="vertical" class="w-full">
          <TabsList class="grid h-auto w-[200px] grid-rows-4">
            <TabsTrigger value="general" class="justify-start"
              >General</TabsTrigger
            >
            <TabsTrigger value="security" class="justify-start"
              >Security</TabsTrigger
            >
            <TabsTrigger value="integrations" class="justify-start"
              >Integrations</TabsTrigger
            >
            <TabsTrigger value="support" class="justify-start"
              >Support</TabsTrigger
            >
          </TabsList>
          <div class="flex-1 ml-6">
            <TabsContent value="general" class="space-y-4">
              <div>
                <h3 class="text-lg font-semibold">General Settings</h3>
                <p class="text-muted-foreground">
                  Manage your general account settings and preferences.
                </p>
              </div>
              <div class="space-y-4">
                <div class="space-y-2">
                  <Label for="company">Company Name</Label>
                  <Input id="company" placeholder="Enter your company name" />
                </div>
                <div class="space-y-2">
                  <Label for="website">Website</Label>
                  <Input
                    id="website"
                    type="url"
                    placeholder="https://example.com"
                  />
                </div>
              </div>
            </TabsContent>
            <TabsContent value="security" class="space-y-4">
              <div>
                <h3 class="text-lg font-semibold">Security Settings</h3>
                <p class="text-muted-foreground">
                  Manage your security and privacy settings.
                </p>
              </div>
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <div>
                    <Label class="text-base">Two-factor Authentication</Label>
                    <p class="text-sm text-muted-foreground">
                      Add an extra layer of security
                    </p>
                  </div>
                  <Switch />
                </div>
              </div>
            </TabsContent>
            <TabsContent value="integrations" class="space-y-4">
              <div>
                <h3 class="text-lg font-semibold">Integrations</h3>
                <p class="text-muted-foreground">
                  Connect with third-party services.
                </p>
              </div>
              <div class="text-center py-8">
                <p class="text-muted-foreground">
                  No integrations configured yet.
                </p>
                <Button class="mt-4">Add Integration</Button>
              </div>
            </TabsContent>
            <TabsContent value="support" class="space-y-4">
              <div>
                <h3 class="text-lg font-semibold">Support</h3>
                <p class="text-muted-foreground">
                  Get help and contact support.
                </p>
              </div>
              <div class="space-y-4">
                <Button variant="outline" class="w-full justify-start">
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
                      d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  Help Center
                </Button>
                <Button variant="outline" class="w-full justify-start">
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
                      d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                    />
                  </svg>
                  Contact Support
                </Button>
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    </div>
  </div>
</template>
